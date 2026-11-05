"""Check actual development ZIPs; distinguish absent packaging from verified artifacts."""
import hashlib
import json
import zipfile
from collections import Counter
from pathlib import Path
from port_batch import ROOT, WORK


def main():
    records = []
    for assembly in json.loads((ROOT / 'migration/assembly-audit.json').read_text(encoding='utf-8')):
        path = Path(assembly['path'])
        name = assembly['name']
        record = dict(internalName=name, status='no-local-zip', manifest='missing')
        manifest = path.with_suffix('.json')
        if manifest.exists():
            data = json.loads(manifest.read_text(encoding='utf-8-sig'))
            record['manifest'] = 'passed' if isinstance(data, dict) and data.get('DalamudApiLevel') == 14 else 'failed'
        candidates = list(path.parent.glob('*.zip')) + list(path.parent.glob('*/*.zip'))
        if name == 'MissFisher':
            candidates = [WORK / 'sources/MissFisher/.api14/artifacts/MissFisher-1.9.20.1.zip']
        for candidate in sorted(candidates, key=lambda file: file.stat().st_mtime, reverse=True):
            try:
                with zipfile.ZipFile(candidate) as archive:
                    files = {Path(member.replace('\\', '/')).name: member for member in archive.namelist()}
                    if name + '.dll' not in files or name + '.json' not in files:
                        continue
                    metadata = json.loads(archive.read(files[name + '.json']).decode('utf-8-sig'))
                    same = hashlib.sha256(archive.read(files[name + '.dll'])).digest() == hashlib.sha256(path.read_bytes()).digest()
                    bundled = sorted(set(files) & {'Dalamud.dll', 'FFXIVClientStructs.dll', 'Lumina.dll', 'Lumina.Excel.dll', 'Dalamud.Bindings.ImGui.dll'})
                    record.update(status='passed' if metadata.get('DalamudApiLevel') == 14 and same and not bundled else 'failed', package=str(candidate), matchesBuiltDll=same, bundledHostAssemblies=bundled)
                    break
            except (OSError, ValueError, zipfile.BadZipFile):
                continue
        records.append(record)
    (ROOT / 'migration/package-review.json').write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
    print(Counter(item['status'] for item in records))
    failed = [item for item in records if item['status'] == 'failed' or item['manifest'] == 'failed']
    for item in failed:
        print(item)
    if failed:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
