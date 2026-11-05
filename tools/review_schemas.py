"""Compare custom Excel sheet declarations with actual API14 generated schema hashes."""
import concurrent.futures
import json
import re
import subprocess
from pathlib import Path
from port_batch import ROOT, WORK


def main():
    schema = {x['sheet']: x for x in json.loads((WORK / 'references/schema-api14.json').read_text(encoding='utf-8-sig'))}
    def scan(repo):
        items = []
        result = subprocess.run(['git', 'ls-files', '-z', '--recurse-submodules', '*.cs'], cwd=repo, capture_output=True, encoding='utf-8')
        if result.returncode:
            return [dict(repository=repo.name, status='inventory-error', error=result.stderr[:400])]
        for name in filter(None, result.stdout.split('\0')):
            try:
                text = (repo / name).read_text(encoding='utf-8-sig', errors='replace')
            except OSError as exc:
                items.append(dict(repository=repo.name, path=name, status='read-error', error=str(exc)))
                continue
            for match in re.finditer(r'\[Sheet\(\s*"([^"]+)"\s*(?:,\s*(?:columnHash:\s*)?(0x[\da-fA-F]+|\d+)[uU]?)?', text):
                sheet, h = match.groups()
                expected, old = schema.get(sheet), int(h, 0) if h else None
                status = 'hash-mismatch' if old is not None and expected and old != expected['hash'] else 'unhashed-or-custom' if old is None else 'hash-match' if expected else 'not-in-sdk'
                items.append(dict(repository=repo.name, path=name, sheet=sheet, hash=old, api14Hash=expected['hash'] if expected else None, status=status))
        return items
    with concurrent.futures.ThreadPoolExecutor(6) as pool:
        items = [item for group in pool.map(scan, [x for x in (WORK / 'sources').iterdir() if (x / '.git').exists()]) for item in group]
    (ROOT / 'migration/schema-review.json').write_text(json.dumps(items, indent=2) + '\n', encoding='utf-8')
    from collections import Counter
    print(Counter(x['status'] for x in items))
    for item in items:
        if item['status'] in ['hash-mismatch', 'read-error', 'inventory-error']:
            print(item)


if __name__ == '__main__':
    main()
