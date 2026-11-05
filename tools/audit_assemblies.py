"""Refresh actual output metadata with the PEReader verifier (not manifest declarations)."""
import json
import subprocess
from pathlib import Path
from port_batch import ROOT, WORK, DOTNET


def main():
    existing = json.loads((ROOT / 'migration/assembly-audit.json').read_text(encoding='utf-8'))
    paths = {item['path'] for item in existing}
    for relative in [
        'ffxiv-bundleoftweaks/ffxiv_bundledtweaks/bin/Release/Automaton.dll',
        'ffxiv_bossmod/BossMod/bin/Release/BossMod.dll',
        'BossmodReborn/BossMod/bin/Release/BossModReborn.dll',
        'SimpleTweaksPlugin/bin/Release/SimpleTweaksPlugin.dll',
        'PocketRecorder/bin/x64/Release/PocketRecorder.dll',
        'MissFisher/.api14/work/package/MissFisher.dll',
    ]:
        paths.add(str(WORK / 'sources' / relative))
    output = ROOT / 'tools/AssemblyVerifier'
    subprocess.run([str(DOTNET), 'build', str(output / 'Verify.csproj'), '-c', 'Release', '-v', 'quiet'], check=True)
    def inspect(selected):
        file = output / 'audit-paths.txt'
        file.write_text('\n'.join(sorted(selected)), encoding='utf-8')
        return json.loads(subprocess.check_output([str(DOTNET), str(output / 'bin/Release/net10.0/Verify.dll'), str(file)]))
    assemblies = inspect(paths)
    expected = {x['internalName'] for x in json.loads((ROOT / 'migration/plugins.json').read_text(encoding='utf-8'))}
    assert {x['name'] for x in assemblies} == expected, 'Assembly coverage mismatch'
    for item in assemblies:
        assert item['references'].get('Dalamud', '').startswith('14.'), item['path']
        assert item['references'].get('System.Runtime', '').startswith('10.'), item['path']
    (ROOT / 'migration/assembly-audit.json').write_text(json.dumps(assemblies, indent=2) + '\n', encoding='utf-8')
    dependencies = inspect({str(dll) for item in assemblies for dll in Path(item['path']).parent.glob('*.dll')})
    for item in dependencies:
        assert not item['references'].get('Dalamud') or item['references']['Dalamud'].startswith('14.'), item['path']
    (ROOT / 'migration/dependency-audit.json').write_text(json.dumps(dependencies, indent=2) + '\n', encoding='utf-8')
    print(f'Passed: {len(assemblies)} main DLLs API14/.NET10; {len(dependencies)} managed outputs have no non-API14 Dalamud references.')


if __name__ == '__main__':
    main()
