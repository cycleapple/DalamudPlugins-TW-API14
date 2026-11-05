"""Save reproducible submodule patches and build commands on API14 branches.

Pinned upstream submodules stay pinned. Consumer-specific API14 patches are
versioned with the plugin and applied idempotently by .api14/build.ps1.
"""
import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path
from port_batch import ROOT, WORK, run, targets

BUILD = r'''param(
    [Parameter(Mandatory = $true)][string]$DalamudHome,
    [switch]$ManagedOnly,
    [string]$Dotnet = 'dotnet'
)
$ErrorActionPreference = 'Stop'
$refDir = (Resolve-Path -LiteralPath $DalamudHome).Path
$identity = [System.Reflection.AssemblyName]::GetAssemblyName((Join-Path $refDir 'Dalamud.dll'))
if ($identity.Version.Major -ne 14) { throw "Expected Dalamud API14; found $($identity.Version)." }
$env:DALAMUD_HOME = $refDir
$env:DOTNET_ROLL_FORWARD = 'Major'
$env:DOTNET_CLI_UI_LANGUAGE = 'en-US'
$dotnetExe = (Get-Command $Dotnet -ErrorAction Stop).Source
$env:PATH = (Split-Path -Parent $dotnetExe) + [IO.Path]::PathSeparator + $env:PATH
$env:DOTNET_ROOT = Split-Path -Parent $dotnetExe
$sdkVersion = & $dotnetExe --version
if ([version]$sdkVersion -lt [version]'10.0.101') { throw "Requires .NET SDK 10.0.101 or newer; found $sdkVersion." }
Push-Location (Join-Path $PSScriptRoot '..')
try {
    git submodule update --init --recursive
    if ($LASTEXITCODE -ne 0) { throw 'Submodule initialization failed.' }
    $plan = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'dependencies.json') -Raw | ConvertFrom-Json
    foreach ($dependency in $plan) {
        $patch = Join-Path $PSScriptRoot $dependency.patch
        $hash = (Get-FileHash -LiteralPath $patch -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($hash -ne $dependency.sha256) { throw "Patch hash mismatch: $patch" }
        git -C $dependency.path apply --check $patch 2>$null
        if ($LASTEXITCODE -eq 0) {
            git -C $dependency.path apply $patch
            if ($LASTEXITCODE -ne 0) { throw "Failed to apply $patch" }
        } else {
            git -C $dependency.path apply --reverse --check $patch 2>$null
            if ($LASTEXITCODE -ne 0) { throw "Dependency differs from its pinned API14 patch: $($dependency.path)" }
        }
    }
    $prebuild = Join-Path $PSScriptRoot 'prebuild.ps1'
    if ((Test-Path -LiteralPath $prebuild) -and !$ManagedOnly) {
        & $prebuild
        if ($LASTEXITCODE -ne 0) { throw 'Native prerequisite build failed.' }
    }
    $projects = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'projects.json') -Raw | ConvertFrom-Json
    foreach ($project in $projects) {
        $extra = @()
        if ($ManagedOnly -and $project.internalName -eq 'PocketRecorder') { $extra += '-p:NativeRecorderAutoBuild=false' }
        & $dotnetExe build $project.project -c Release "-p:DalamudLibPath=$refDir/" -p:EnableWindowsTargeting=true -p:RestoreLockedMode=false @extra
        if ($LASTEXITCODE -ne 0) { throw "API14 build failed: $($project.internalName)" }
    }
} finally { Pop-Location }
'''


def dependencies(top, folder):
    result = []
    def walk(path):
        for line in run(["git", "ls-tree", "-r", "HEAD"], path).splitlines():
            if not line.startswith("160000 "):
                continue
            sub = path / line.split("\t", 1)[1]
            if not (sub / ".git").exists():
                continue
            relative = sub.relative_to(top).as_posix()
            walk(sub)
            new_enum = sub / "ECommons/DalamudServices/Legacy/NetworkMessageDirection.cs"
            if new_enum.exists():
                run(["git", "add", "-N", "--", str(new_enum)], sub)
            patch = subprocess.check_output(["git", "diff", "--binary", "--ignore-submodules=all", "HEAD"], cwd=sub)
            if patch:
                name = hashlib.sha256(relative.encode()).hexdigest()[:16] + ".patch"
                (folder / "patches" / name).write_bytes(patch)
                result.append({"path": relative, "baseCommit": run(["git", "rev-parse", "HEAD"], sub),
                               "patch": "patches/" + name, "sha256": hashlib.sha256(patch).hexdigest()})
    walk(top)
    return sorted(result, key=lambda x: (x["path"].count("/"), x["path"]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--passed-only", action="store_true")
    parser.add_argument("--only", nargs="*")
    args = parser.parse_args()
    projects = json.loads((ROOT / "migration/projects.json").read_text(encoding="utf-8"))
    for project in projects:
        name = project["repository"].split("/")[1]
        if project["kind"] != "plugin" or (args.only and name not in args.only):
            continue
        report = ROOT / "migration/batches" / (name + ".json")
        if not report.exists():
            continue
        data = json.loads(report.read_text(encoding="utf-8"))
        passed = bool(data["results"]) and not data.get("unresolved") and all(r["status"] == "build-passed" for r in data["results"])
        if args.passed_only and not passed:
            continue
        top = WORK / "sources" / name
        if not (top / ".git").exists():
            continue
        folder = top / ".api14"
        (folder / "patches").mkdir(parents=True, exist_ok=True)
        (folder / ".gitattributes").write_text("patches/*.patch -text\n", encoding="utf-8")
        plan = dependencies(top, folder)
        (folder / "dependencies.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
        selected = [{"internalName": i, "project": p} for i, p in targets(project, top)]
        (folder / "projects.json").write_text(json.dumps(selected, indent=2) + "\n", encoding="utf-8")
        (folder / "build.ps1").write_text(BUILD, encoding="utf-8")
        status = "Upstream API14 Release build passed." if passed else "API14 migration in progress; see unified repository diagnostics."
        (top / "API14_PORT.md").write_text(
            "# API14 port\n\n" + status + " TC API14 build and in-game verification are pending.\n\n"
            "Requires .NET SDK 10.0.101 or newer. Use `.api14/build.ps1 -DalamudHome <isolated-api14-directory>`. "
            "The script rejects non-14 Dalamud assemblies and applies versioned patches to pinned submodules.\n\n"
            "Reference baseline: upstream Dalamud 14.0.5.1, distribution commit "
            "`6fb2b12018922bddeef009edd26082f068f8c602`, archive SHA-256 "
            "`6a9f9aee19af4280f2d61680bbff960ae48e5dcaad70707baad857da2f9d8e48`.\n\n"
            "Traditional Chinese resources and TC fixes remain in this branch. "
            "Shared dependencies are kept at their existing commits; patch identities are recorded in `.api14/dependencies.json`. "
            "This branch is not a verified TC release.\n", encoding="utf-8")
        run(["git", "add", "-u", "--", "."], top)
        run(["git", "add", "--", ".api14", "API14_PORT.md"], top)
        if (top / "api14-deps").exists():
            run(["git", "add", "--", "api14-deps"], top)
        new_enum = top / "NetworkMessageDirection.cs"
        if new_enum.exists():
            run(["git", "add", "--", "NetworkMessageDirection.cs"], top)
        run(["git", "-c", "core.whitespace=trailing-space,space-before-tab,cr-at-eol", "diff", "--cached", "--check", "--", ".", ":(exclude).api14/patches/**"], top)
        if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=top).returncode:
            run(["git", "commit", "-m", "Port to API14 and .NET 10 with pinned dependency patches"], top)
        if args.publish:
            pushed = False
            for attempt in range(3):
                try:
                    run(["git", "push", "origin", "HEAD:refs/heads/api14-tw"], top, timeout=180)
                    pushed = True
                    break
                except RuntimeError as exc:
                    if attempt == 2:
                        # GitHub can reject commit_refs after receiving the pack.
                        # The REST update still enforces a fast-forward.
                        sha = run(["git", "rev-parse", "HEAD"], top)
                        try:
                            run(["gh", "api", f"repos/{project['repository']}/git/refs/heads/api14-tw", "--method", "PATCH", "-f", f"sha={sha}", "-F", "force=false"])
                            pushed = True
                        except RuntimeError:
                            data["publishError"] = str(exc)
                            print(name, "publish-pending", flush=True)
                    time.sleep(2)
        data["sourceCommit"] = run(["git", "rev-parse", "HEAD"], top)
        data["publishedSource"] = args.publish and pushed
        data["dependencyPatches"] = len(plan)
        report.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(name, "published" if data["publishedSource"] else ("publish-pending" if args.publish else "checkpointed"), len(plan), flush=True)


if __name__ == "__main__":
    main()
