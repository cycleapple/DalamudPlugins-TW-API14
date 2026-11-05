"""Verify the host assemblies MSBuild actually resolves, including native struct definitions."""
import concurrent.futures
import json
import os
import subprocess
from pathlib import Path
from port_batch import ROOT, WORK, DOTNET, REFS


def inspect(task):
    repository, result = task
    name = repository.split('/')[1]
    project = WORK / 'sources' / name / result['project']
    env = dict(os.environ, DALAMUD_HOME=str(REFS), DOTNET_ROOT=str(DOTNET.parent), DOTNET_ROLL_FORWARD='Major')
    command = [str(DOTNET), 'msbuild', str(project), '-t:ResolveReferences', '-getItem:ReferencePath', '-p:Configuration=Release', '-p:DalamudLibPath=' + str(REFS) + '/', '-p:RestoreLockedMode=false', '-v:quiet']
    process = subprocess.run(command, capture_output=True, encoding='utf-8', errors='replace', env=env, timeout=180)
    record = dict(repository=repository, internalName=result['internalName'], project=result['project'], status='passed', hostReferences={})
    try:
        data = json.loads(process.stdout[process.stdout.index('{'):])
        assert process.returncode == 0
        for reference in data['Items']['ReferencePath']:
            if reference['Filename'] in ['Dalamud', 'FFXIVClientStructs', 'Lumina', 'Lumina.Excel', 'Dalamud.Bindings.ImGui']:
                path = Path(reference['FullPath']).resolve()
                assert path.parent == REFS.resolve(), f'Unexpected host reference: {path}'
                record['hostReferences'][reference['Filename']] = str(path)
        assert 'Dalamud' in record['hostReferences']
    except Exception as exc:
        record.update(status='failed', error=str(exc), diagnostics=(process.stdout + process.stderr)[-1800:])
    return record


if __name__ == '__main__':
    tasks = []
    for file in (ROOT / 'migration/batches').glob('*.json'):
        batch = json.loads(file.read_text(encoding='utf-8'))
        tasks += [(batch['repository'], result) for result in batch['results'] if result.get('project')]
    with concurrent.futures.ThreadPoolExecutor(6) as pool:
        records = list(pool.map(inspect, tasks))
    (ROOT / 'migration/reference-resolution.json').write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
    failed = [item for item in records if item['status'] != 'passed']
    print(f'Resolved {len(records)} plugin projects against the pinned SDK; {len(failed)} failures.')
    for item in failed:
        print(item)
    if failed:
        raise SystemExit(1)
