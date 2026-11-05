"""Prepare isolated API14 source clones and collect real Release build diagnostics."""
import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT.parent
DOTNET = Path(os.environ.get("API14_DOTNET", str(WORK.parent / "api13-extended-work/tools/dotnet10/dotnet.exe")))
REFS = Path(os.environ.get("DALAMUD_HOME", str(WORK / "references/upstream-api14")))
ALIASES = {"LoporritSync": "MareSynchronos", "PalacePal": "Pal.Client", "PeepingTom": "Peeping Tom", "GatherBuddyReborn": "GatherBuddy"}


def run(args, cwd=None, timeout=300):
    p = subprocess.run([str(a) for a in args], cwd=cwd, capture_output=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    if p.returncode:
        raise RuntimeError(p.stdout[-2000:] + p.stderr[-2000:])
    return p.stdout.strip()


def tracked(path):
    return run(["git", "ls-files"], path).splitlines()


def clone_tree(source, dest, commit=None, remote=None):
    if not (dest / ".git").exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--shared", "--no-checkout", source, dest], timeout=600)
        if remote:
            run(["git", "remote", "set-url", "origin", remote], dest)
        try:
            run(["git", "cat-file", "-e", commit or "origin/api14-tw"], dest)
        except RuntimeError:
            run(["git", "fetch", "origin", commit or "api14-tw"], dest, timeout=600)
        run(["git", "checkout", "-B", "api14-tw", commit or "origin/api14-tw"], dest)
    elif run(["git", "branch", "--show-current"], dest) != "api14-tw":
        # A failed initial checkout can leave an empty no-checkout clone.
        if remote:
            run(["git", "remote", "set-url", "origin", remote], dest)
        try:
            run(["git", "fetch", source, commit or "api14-tw"], dest, timeout=600)
        except RuntimeError:
            run(["git", "fetch", "origin", commit or "api14-tw"], dest, timeout=600)
        run(["git", "checkout", "-B", "api14-tw", commit or "origin/api14-tw"], dest)
    tree = run(["git", "ls-tree", "-r", "HEAD"], dest)
    for line in tree.splitlines():
        if not line.startswith("160000 "):
            continue
        meta, name = line.split("\t", 1)
        sha = meta.split()[2]
        original = Path(source) / name
        target = dest / name
        if (original / ".git").exists():
            clone_tree(original, target, sha)
        elif not (target / ".git").exists():
            run(["git", "submodule", "update", "--init", "--recursive", "--", name], dest, timeout=900)


def migrate(path):
    changed = []
    for name in tracked(path):
        p = path / name
        if not p.is_file():
            continue
        if p.suffix in [".csproj", ".props", ".targets"]:
            text = p.read_text(encoding="utf-8-sig")
            new = re.sub(r"Dalamud\.(?:CN\.)?NET\.Sdk/13\.[\w.\-]+", "Dalamud.NET.Sdk/14.0.1", text)
            new = re.sub(r'(<Sdk\s+Name="Dalamud.NET.Sdk"\s+Version=")13\.[^\"]+', r'\g<1>14.0.1', new)
            new = re.sub(r'((?:Include|Update)="DalamudPackager"\s+Version=")13\.[^\"]+', r'\g<1>14.0.1', new)
            new = re.sub(r'(<DalamudApiLevel>)13(</DalamudApiLevel>)', r'\g<1>14\2', new)
            new = re.sub(r'\bnet9\.0(?=[<;"\-])', 'net10.0', new)
            new = re.sub(r'\bnet9(?=[<;"\-])', 'net10.0', new)
            new = re.sub(r'((?:Include|Update)="[Ee][Cc]ommons"\s+Version=")3\.0\.[^\"]+', r'\g<1>3.1.0.29', new)
            new = new.replace('<Use_Dalamud_CN>true</Use_Dalamud_CN>', '<Use_Dalamud_CN>false</Use_Dalamud_CN>')
            if new != text:
                p.write_text(new, encoding="utf-8")
                changed.append(name)
        elif p.suffix == ".json":
            try:
                text = p.read_text(encoding="utf-8-sig")
                data = json.loads(text)
                if isinstance(data, dict) and data.get("DalamudApiLevel") == 13:
                    new = re.sub(r'("(?:Testing)?DalamudApiLevel"\s*:\s*)13\b', r'\g<1>14', text)
                    p.write_text(new, encoding="utf-8")
                    changed.append(name)
                elif name == "global.json" and str(data.get("sdk", {}).get("version", "")).startswith("9."):
                    data["sdk"]["version"] = "10.0.302"
                    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
                    changed.append(name)
            except (ValueError, UnicodeError):
                pass
    for line in run(["git", "ls-tree", "-r", "HEAD"], path).splitlines():
        if line.startswith("160000 "):
            name = line.split("\t", 1)[1]
            submodule = path / name
            if (submodule / ".git").exists():
                changed.extend(name + "/" + p for p in migrate(submodule))
    return changed


def targets(project, path):
    files = [p for p in tracked(path) if p.endswith(".csproj")]
    chosen = []
    for internal in project["plugins"]:
        target_name = ALIASES.get(internal, internal)
        matching = [p for p in files if Path(p).stem.casefold() == target_name.casefold()]
        if matching:
            chosen.append((internal, matching[0]))
    return chosen


def align_ecommons(path):
    local = path / "ECommons/ECommons/ECommons.csproj"
    if not local.exists():
        return
    for project in path.rglob("*.csproj"):
        if "obj" in project.parts or project == local:
            continue
        text = project.read_text(encoding="utf-8-sig")
        relative = os.path.relpath(local, project.parent).replace(os.sep, "/")
        new = re.sub(r'<PackageReference\s+Include="[Ee][Cc]ommons"\s+Version="[^\"]+"\s*/>',
                     lambda m: f'<ProjectReference Include="{relative}" />', text)
        if new != text:
            project.write_text(new, encoding="utf-8")


def process(project, do_build):
    name = project["repository"].split("/")[1]
    dest = WORK / "sources" / name
    out = {"repository": project["repository"], "path": str(dest), "results": []}
    try:
        locals_ = project["localCheckouts"]
        if locals_:
            locals_ = sorted(locals_, key=lambda p: run(["git", "branch", "--show-current"], p) != project["sourceBranch"])
            clone_tree(locals_[0], dest, project["targetCommit"], f"https://github.com/{project['repository']}.git")
        elif not dest.exists():
            run(["git", "clone", "--branch", "api14-tw", f"https://github.com/{project['repository']}.git", dest], timeout=900)
        out["changed"] = migrate(dest)
        align_ecommons(dest)
        selected = targets(project, dest)
        out["unresolved"] = [p for p in project["plugins"] if p not in [s[0] for s in selected]]
        for internal, csproj in selected:
            result = {"internalName": internal, "project": csproj, "status": "prepared"}
            if do_build:
                logs = ROOT / "logs"
                logs.mkdir(exist_ok=True)
                log = logs / f"{internal}.log"
                env = dict(os.environ, DALAMUD_HOME=str(REFS), DOTNET_ROOT=str(DOTNET.parent),
                           PATH=str(DOTNET.parent) + os.pathsep + os.environ.get("PATH", ""),
                           DOTNET_ROLL_FORWARD="Major", DOTNET_CLI_UI_LANGUAGE="en-US", DOTNET_CLI_TELEMETRY_OPTOUT="1", DOTNET_NOLOGO="1")
                args = [str(DOTNET), "build", csproj, "-c", "Release", "-v", "minimal",
                        "-p:DalamudLibPath=" + str(REFS) + "/", "-p:EnableWindowsTargeting=true", "-p:RestoreLockedMode=false"]
                start = time.monotonic()
                try:
                    with log.open("w", encoding="utf-8") as f:
                        proc = subprocess.run(args, cwd=dest, stdout=f, stderr=subprocess.STDOUT, env=env, timeout=600)
                    result["status"] = "build-passed" if proc.returncode == 0 else "build-failed"
                    text = log.read_text(encoding="utf-8", errors="replace")
                    result["errors"] = list(dict.fromkeys(line.strip() for line in text.splitlines() if ": error " in line))[:35]
                except subprocess.TimeoutExpired:
                    result["status"] = "build-timeout"
                result["seconds"] = round(time.monotonic() - start, 1)
                result["log"] = str(log)
            out["results"].append(result)
        out["status"] = "processed"
    except Exception as exc:
        out["status"] = "error"
        out["error"] = str(exc)
    directory = ROOT / "migration/batches"
    directory.mkdir(exist_ok=True)
    (directory / f"{name}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{name}: {out['status']} " + ", ".join(f"{r['internalName']}={r['status']}" for r in out["results"]), flush=True)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--only", nargs="*")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--failed-only", action="store_true")
    args = parser.parse_args()
    projects = json.loads((ROOT / "migration/projects.json").read_text(encoding="utf-8"))
    projects = [p for p in projects if p["kind"] == "plugin" and (not args.only or p["repository"].split("/")[1] in args.only)]
    if args.failed_only:
        def failed(p):
            previous = ROOT / "migration/batches" / (p["repository"].split("/")[1] + ".json")
            if not previous.exists():
                return True
            data = json.loads(previous.read_text(encoding="utf-8"))
            return data["status"] == "error" or bool(data.get("unresolved")) or any(r["status"] != "build-passed" for r in data["results"])
        projects = [p for p in projects if failed(p)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda p: process(p, args.build), projects))
    summary = {}
    for p in results:
        for r in p["results"]:
            summary[r["status"]] = summary.get(r["status"], 0) + 1
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
