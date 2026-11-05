"""Check merged coverage and fail closed on unverified API14 feed entries."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    plugins = read("migration/plugins.json")
    projects = read("migration/projects.json")
    names = [p["internalName"] for p in plugins]
    require(len(names) == len(set(names)), "Duplicate InternalName in migration inventory")
    expected = set()
    for baseline in ["DalamudPlugins-TW", "DalamudPlugins-TW-API13-Extended"]:
        expected.update(p["InternalName"] for p in read(f"migration/baselines/{baseline}.json"))
    require(set(names) == expected, "Merged inventory does not cover both API13 catalogs")
    for project in projects:
        require(project["repository"].startswith("cycleapple/"), "Unowned repository in branch plan")
        require(project["status"] in ["branch-created", "branch-exists"], f"Branch not ready: {project['repository']}")
        require(project["targetBranch"] == "api14-tw", "Unexpected target branch")
        require(re.fullmatch(r"[a-f0-9]{40}", project["targetCommit"]), "Missing target commit")
    repositories = {p["repository"].lower() for p in projects}
    for plugin in plugins:
        require(plugin.get("repository") and plugin["repository"].lower() in repositories,
                f"Plugin missing source branch: {plugin['internalName']}")
    catalog = read("repo.json")
    ids = [p["InternalName"] for p in catalog]
    require(len(ids) == len(set(ids)), "Duplicate feed InternalName")
    by_name = {p["internalName"]: p for p in plugins}
    for entry in catalog:
        internal = entry["InternalName"]
        require(internal in by_name, f"Plugin missing from inventory: {internal}")
        require(entry["DalamudApiLevel"] == 14 and entry.get("TestingDalamudApiLevel", 14) == 14,
                f"Non-API14 manifest: {internal}")
        attestation = read(f"validation/{internal}.json")
        require(attestation["internalName"] == internal, "Attestation identity mismatch")
        require(attestation["version"] == entry["AssemblyVersion"], "Attestation version mismatch")
        require(attestation["apiLevel"] == 14, "Attestation API mismatch")
        require(attestation["build"] == "passed" and attestation["tcRuntime"] == "passed",
                f"Build/TC runtime verification incomplete: {internal}")
        require(attestation["dalamudAssemblyVersion"].startswith("14."), "Build references must be API14")
        require(re.fullmatch(r"[a-f0-9]{40}", attestation["sourceCommit"]), "Missing source commit")
        require(attestation.get("buildEvidence") and attestation.get("runtimeEvidence"), "Missing verification evidence")
        require(re.fullmatch(r"[a-f0-9]{64}", attestation["sha256"]), "Missing package SHA-256")
        for field in ["DownloadLinkInstall", "DownloadLinkTesting", "DownloadLinkUpdate"]:
            url = entry[field]
            require(url.startswith("https://github.com/cycleapple/DalamudPlugins-TW-API14/releases/download/"),
                    f"Download outside API14 repository: {internal}")
            require("api13" not in url.lower(), "API13 package referenced by API14 feed")
            require(url == attestation["downloadUrl"], "Download URL differs from verified package")
        package = ROOT / "packages" / attestation["fileName"]
        if package.exists():
            require(hashlib.sha256(package.read_bytes()).hexdigest() == attestation["sha256"], "Package SHA-256 mismatch")
    print(f"OK: {len(plugins)} merged plugins, {len(projects)} API14 branches, {len(catalog)} published API14 packages")


if __name__ == "__main__":
    main()
