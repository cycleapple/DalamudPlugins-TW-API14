"""Snapshot both API13 catalogs and prepare API14 branches without switching checkouts.

Requires Python 3.11+, git and authenticated gh. Run once with --workspace; reruns
preserve existing API14 branches. Only cycleapple repositories are writable.
"""
import argparse
import base64
import concurrent.futures
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER = "cycleapple"
TARGET = "api14-tw"


def run(*args, cwd=None):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if p.returncode:
        raise RuntimeError(f"{' '.join(map(str, args))}: {p.stderr.strip()}")
    return p.stdout.strip()


def api(path, method="GET", **fields):
    args = ["gh", "api", path, "--method", method]
    for key, value in fields.items():
        args.extend(["-f", f"{key}={value}"])
    return json.loads(run(*args))


def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def local_sources(workspace):
    paths = []
    for parent in [workspace / "api13-work/plugins", workspace / "api13-extended-work/sources"]:
        paths.extend(p for p in parent.iterdir() if p.is_dir() and (p / ".git").exists())
    for name in ["MouseLock-API13", "MaskOfKefka-API13", "Facade-API13", "PocketRecorder-API13", "VFXEditor-API13", "PlayerWatchlist"]:
        p = workspace / name
        if (p / ".git").exists():
            paths.append(p)
    result = []
    for p in paths:
        branch = run("git", "branch", "--show-current", cwd=p)
        if not branch.startswith("api13") and p.name != "XivTreasureParty":
            continue
        remotes = run("git", "remote", "-v", cwd=p)
        owned = re.findall(r"github.com[/:](cycleapple/[^\s]+?)(?:\.git)?\s", remotes)
        upstream = run("git", "config", "--get", "remote.origin.url", cwd=p)
        result.append({"path": str(p), "branch": branch,
                       "commit": run("git", "rev-parse", "HEAD", cwd=p),
                       "trackedChanges": run("git", "status", "--porcelain", "--untracked-files=no", cwd=p).splitlines(),
                       "repository": owned[0] if owned else None, "origin": upstream})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--create-branches", action="store_true")
    args = parser.parse_args()
    catalogs = {}
    snapshots = []
    for repo in ["DalamudPlugins-TW", "DalamudPlugins-TW-API13-Extended"]:
        commit = api(f"repos/{OWNER}/{repo}/commits/main")["sha"]
        content = api(f"repos/{OWNER}/{repo}/contents/repo.json?ref={commit}")
        entries = json.loads(base64.b64decode(content["content"]))
        save(ROOT / f"migration/baselines/{repo}.json", entries)
        snapshots.append({"repository": f"{OWNER}/{repo}", "commit": commit})
        for entry in entries:
            catalogs.setdefault(entry["InternalName"], []).append({"catalog": repo, "manifest": entry})
    sources = local_sources(args.workspace.resolve())
    save(ROOT / "migration/local-sources.json", sources)
    save(ROOT / "migration/baselines/snapshots.json", snapshots)
    projects = {}
    plugins = []
    for internal, variants in sorted(catalogs.items()):
        # Compare numeric assembly versions; prefer Extended on a tie.
        chosen = max(variants, key=lambda x: tuple(int(n) for n in x["manifest"]["AssemblyVersion"].split(".")))
        manifest = chosen["manifest"]
        url = manifest.get("RepoUrl", "")
        m = re.search(r"github.com/(cycleapple/[^/#?]+)(?:/tree/([^?#]+))?", url)
        repository = m[1].removesuffix(".git") if m else None
        source_branch = m[2] if m and m[2] else None
        plugin = {"internalName": internal, "name": manifest["Name"], "repository": repository,
                  "api13Version": manifest["AssemblyVersion"], "baselineCatalog": chosen["catalog"],
                  "variants": [{"catalog": v["catalog"], "version": v["manifest"]["AssemblyVersion"]} for v in variants],
                  "status": "queued", "build": "not-run", "runtime": "not-run"}
        plugins.append(plugin)
        if repository:
            project = projects.setdefault(repository, {"repository": repository, "kind": "plugin", "plugins": [], "preferredBranches": []})
            project["plugins"].append(internal)
            if source_branch and source_branch not in project["preferredBranches"]:
                project["preferredBranches"].append(source_branch)
    # Resolve legacy manifests that still point at an upstream author.
    for src in sources:
        repo = src["repository"]
        if repo and repo not in projects:
            projects[repo] = {"repository": repo, "kind": "plugin", "plugins": [], "preferredBranches": [src["branch"]]}
    for name in ["ECommons", "OtterGui", "Penumbra.GameData", "CriticalCommonLib", "KamiToolKit", "AutoRetainerAPI", "Dalamud", "FFXIVClientStructs"]:
        repository = f"{OWNER}/{name}"
        projects.setdefault(repository, {"repository": repository, "kind": "dependency", "plugins": [], "preferredBranches": []})
    aliases = {"BDTHPlugin": "BDTHPlugin", "IINACT": "IINACT", "Raphael.Dalamud": "Raphael.Dalamud",
               "SomethingNeedDoing": "SomethingNeedDoing", "TextAdvance": "TextAdvance", "YesAlready": "YesAlready"}
    for plugin in plugins:
        if not plugin["repository"] and plugin["internalName"] in aliases:
            repository = f"{OWNER}/{aliases[plugin['internalName']]}"
            plugin["repository"] = repository
            project = projects[repository]
            if plugin["internalName"] not in project["plugins"]:
                project["plugins"].append(plugin["internalName"])

    def prepare(project):
        repo = project["repository"]
        try:
            refs = api(f"repos/{repo}/git/matching-refs/heads/")
            branches = {r["ref"].removeprefix("refs/heads/"): r["object"]["sha"] for r in refs}
            local = [s for s in sources if s["repository"] and s["repository"].lower() == repo.lower()]
            preferences = project.pop("preferredBranches")
            preferences += [s["branch"] for s in local if s["branch"] not in preferences]
            preferences += [b for b in branches if b.startswith("api13") and b not in preferences]
            if project["kind"] == "dependency":
                preferences += [b for b in ["TC-BASE", "tw-client", "tc/api13_net9", "master", "main"] if b in branches]
            baseline = next((b for b in preferences if b in branches), None)
            if not baseline:
                project.update(status="needs-baseline-review", availableBranches=list(branches))
                return project
            sha = branches[baseline]
            project.update(sourceBranch=baseline, sourceCommit=sha, targetBranch=TARGET,
                           status="branch-exists" if TARGET in branches else "planned")
            if TARGET not in branches and args.create_branches:
                api(f"repos/{repo}/git/refs", "POST", ref=f"refs/heads/{TARGET}", sha=sha)
                project["status"] = "branch-created"
                branches[TARGET] = sha
            if TARGET in branches:
                project["targetCommit"] = branches[TARGET]
            for src in local:
                p = src["path"]
                target_sha = branches.get(TARGET)
                if target_sha:
                    exists = subprocess.run(["git", "show-ref", "--verify", "--quiet", f"refs/heads/{TARGET}"], cwd=p).returncode == 0
                    if not exists:
                        known = subprocess.run(["git", "cat-file", "-e", target_sha], cwd=p, capture_output=True).returncode == 0
                        if not known:
                            run("git", "fetch", f"https://github.com/{repo}.git", f"refs/heads/{TARGET}", cwd=p)
                        run("git", "branch", TARGET, target_sha, cwd=p)
            project["localCheckouts"] = [s["path"] for s in local]
        except Exception as exc:
            project["status"] = "error"
            project["error"] = str(exc)
        print(f"{repo}: {project['status']}", flush=True)
        return project

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        prepared = list(pool.map(prepare, projects.values()))
    save(ROOT / "migration/projects.json", sorted(prepared, key=lambda p: p["repository"].lower()))
    previous_path = ROOT / "migration/plugins.json"
    if previous_path.exists():
        previous = {p["internalName"]: p for p in json.loads(previous_path.read_text(encoding="utf-8"))}
        generated = {"internalName", "name", "repository", "api13Version", "baselineCatalog", "variants"}
        for plugin in plugins:
            plugin.update({k: v for k, v in previous.get(plugin["internalName"], {}).items() if k not in generated})
    save(ROOT / "migration/plugins.json", plugins)
    print(f"Prepared {len(plugins)} plugins, {len(prepared)} repositories; "
          f"{sum(len(p['variants']) > 1 for p in plugins)} duplicate catalog entries.")
    if any(p["status"] in ["error", "needs-baseline-review"] for p in prepared):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
