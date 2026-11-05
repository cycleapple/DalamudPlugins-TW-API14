"""Port canonical shared-library branches from the exact baseline used by a verified consumer."""
import hashlib
import json
import os
import subprocess
from pathlib import Path
from port_batch import ROOT, WORK, DOTNET, REFS, clone_tree, migrate, run
from checkpoint_ports import BUILD, dependencies

PROJECTS = {
    "ECommons": "ECommons/ECommons.csproj", "OtterGui": "OtterGui.csproj",
    "Penumbra.GameData": "Penumbra.GameData.csproj", "CriticalCommonLib": "CriticalCommonLib.csproj",
    "KamiToolKit": "KamiToolKit.csproj", "AutoRetainerAPI": "AutoRetainerAPI/AutoRetainerAPI.csproj",
}


def copy_changes(source, dest):
    patch = subprocess.check_output(["git", "diff", "--binary", "--ignore-submodules=all", "HEAD"], cwd=source)
    if patch:
        check = subprocess.run(["git", "apply", "--check", "-"], input=patch, cwd=dest, capture_output=True)
        if check.returncode == 0:
            applied = subprocess.run(["git", "apply", "-"], input=patch, cwd=dest, capture_output=True)
            if applied.returncode:
                raise RuntimeError(applied.stderr.decode(errors="replace"))
        else:
            reverse = subprocess.run(["git", "apply", "--reverse", "--check", "-"], input=patch, cwd=dest, capture_output=True)
            if reverse.returncode:
                raise RuntimeError(check.stderr.decode(errors="replace"))
    for line in run(["git", "ls-tree", "-r", "HEAD"], source).splitlines():
        if line.startswith("160000 "):
            relative = line.split("\t", 1)[1]
            if (source / relative / ".git").exists():
                copy_changes(source / relative, dest / relative)


def main():
    projects = json.loads((ROOT / "migration/projects.json").read_text(encoding="utf-8"))
    candidates = {}
    for folder in (WORK / "sources").iterdir():
        manifest = folder / ".api14/dependencies.json"
        if manifest.exists():
            for item in json.loads(manifest.read_text(encoding="utf-8")):
                candidates[item["baseCommit"]] = folder / item["path"]
    report_file = ROOT / "migration/shared-dependencies.json"
    previous = {x["repository"]: x for x in json.loads(report_file.read_text(encoding="utf-8"))} if report_file.exists() else {}
    reports = []
    for project in projects:
        name = project["repository"].split("/")[1]
        if name not in PROJECTS:
            continue
        if previous.get(project["repository"], {}).get("status") == "build-passed":
            reports.append(previous[project["repository"]])
            continue
        source = candidates[project["sourceCommit"]]
        dest = WORK / "dependencies" / name
        clone_tree(source, dest, project["sourceCommit"], f"https://github.com/{project['repository']}.git")
        copy_changes(source, dest)
        migrate(dest)
        if name == "Penumbra.GameData":
            from add_ported_dependency import add
            csproj = dest / PROJECTS[name]
            text = csproj.read_text(encoding="utf-8-sig")
            for sibling in ["Penumbra.Api", "Penumbra.String", "OtterGui"]:
                add(dest, source.parent / sibling, sibling)
                text = text.replace("..\\" + sibling + "\\", "api14-deps\\" + sibling + "\\")
            text = text.replace("</Project>", '<ItemGroup><Compile Remove="api14-deps/**/*.cs" /><EmbeddedResource Remove="api14-deps/**" /><None Remove="api14-deps/**" /></ItemGroup>\n</Project>')
            csproj.write_text(text, encoding="utf-8")
        folder = dest / ".api14"
        (folder / "patches").mkdir(parents=True, exist_ok=True)
        (folder / ".gitattributes").write_text("patches/*.patch -text\n", encoding="utf-8")
        plan = dependencies(dest, folder)
        (folder / "dependencies.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
        (folder / "projects.json").write_text(json.dumps([{"internalName": name, "project": PROJECTS[name]}], indent=2) + "\n", encoding="utf-8")
        (folder / "build.ps1").write_text(BUILD, encoding="utf-8")
        (dest / "API14_PORT.md").write_text("# API14 shared-library port\n\nMigrated from the exact API13 baseline used by an API14 consumer. "
            "Requires .NET 10 and explicit API14 references. Build with `.api14/build.ps1 -DalamudHome <api14>`. "
            "TC runtime validation is pending. Consumer-specific pinned variants remain in plugin dependency patches.\n", encoding="utf-8")
        log = ROOT / "logs" / ("dependency-" + name + ".log")
        env = dict(os.environ, DALAMUD_HOME=str(REFS), DOTNET_ROOT=str(DOTNET.parent),
                   DOTNET_ROLL_FORWARD="Major", DOTNET_CLI_UI_LANGUAGE="en-US",
                   PATH=str(DOTNET.parent) + os.pathsep + os.environ.get("PATH", ""))
        with log.open("w", encoding="utf-8") as stream:
            proc = subprocess.run([str(DOTNET), "build", PROJECTS[name], "-c", "Release", "-p:DalamudLibPath=" + str(REFS) + "/", "-p:EnableWindowsTargeting=true", "-p:RestoreLockedMode=false", "-v", "minimal"], cwd=dest, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=600)
        record = {"repository": project["repository"], "sourceCommit": project["sourceCommit"], "consumer": str(source),
                  "status": "build-passed" if proc.returncode == 0 else "build-failed", "log": str(log)}
        if proc.returncode == 0:
            run(["git", "add", "-u"], dest)
            run(["git", "add", ".api14", "API14_PORT.md"], dest)
            if (dest / "api14-deps").exists():
                run(["git", "add", "api14-deps"], dest)
            enum = dest / "ECommons/DalamudServices/Legacy/NetworkMessageDirection.cs"
            if enum.exists():
                run(["git", "add", str(enum)], dest)
            if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=dest).returncode:
                run(["git", "commit", "-m", "Port shared dependency to API14 and .NET 10"], dest)
            try:
                run(["git", "push", "origin", "HEAD:refs/heads/api14-tw"], dest, timeout=180)
                record["publishedSource"] = True
            except RuntimeError as exc:
                record.update(publishedSource=False, publishError=str(exc))
            record["targetCommit"] = run(["git", "rev-parse", "HEAD"], dest)
        reports.append(record)
        (ROOT / "migration/shared-dependencies.json").write_text(json.dumps(reports, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(name, record["status"], flush=True)


if __name__ == "__main__":
    main()
