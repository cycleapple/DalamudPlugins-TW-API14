"""Three-way review of native-sensitive source against API13 and upstream API14."""
import concurrent.futures
import io
import json
import re
import subprocess
import tarfile
from pathlib import Path
from port_batch import ROOT, WORK

PATTERN = re.compile(r'(?:Signature\(|HookFrom|delegate\b|FieldOffset\(|StructLayout\(|ReadColumn<|Read(?:U?Int\d+|Float|Double)\(|Marshal\.|ScanText\(|ScanStaticAddress\(|GetStaticAddressFromSig\(|\*\)\s*\([^\n]*(?:0x[0-9a-fA-F]+))')


def surface(text):
    return [re.sub(r'\s+', ' ', x.strip()) for x in text.splitlines() if PATTERN.search(x) and not x.lstrip().startswith('//')]


def review(project):
    name = project['repository'].split('/')[1]
    top = WORK / 'sources' / name
    if project['kind'] == 'dependency':
        top = WORK / 'dependencies' / name
    if not (top / '.git').exists():
        return None
    upstream = json.loads((ROOT / 'migration/upstream-review' / (name + '.json')).read_text(encoding='utf-8'))
    source = WORK / 'references/upstream-review' / name / 'source'
    result = dict(repository=project['repository'], plugins=project['plugins'], upstreamStatus=upstream.get('upstreamStatus'), upstreamCommit=upstream.get('api14Commit') or upstream.get('api14CandidateCommit'), files=[], nativeSensitiveFiles=0, sourceFiles=0)
    files = subprocess.check_output(['git', 'ls-files', '-z', '*.cs'], cwd=top).decode('utf-8').split('\0')
    baseline = {}
    try:
        archive = subprocess.check_output(['git', 'archive', project['sourceCommit'], '--', '*.cs'], cwd=top, stderr=subprocess.PIPE)
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            baseline = {x.name: tar.extractfile(x).read().decode('utf-8-sig', errors='replace') for x in tar if x.isfile()}
    except subprocess.CalledProcessError:
        result['baselineArchiveError'] = True
    for path in filter(None, files):
        # Shared dependencies are reviewed separately; generated/logging adapters carry their own provenance.
        if path.startswith('api14-deps/'):
            continue
        text = (top / path).read_text(encoding='utf-8-sig', errors='replace')
        result['sourceFiles'] += 1
        current = surface(text)
        if not current:
            continue
        result['nativeSensitiveFiles'] += 1
        target = source / path
        if not target.exists():
            if source.exists():
                result['files'].append(dict(path=path, status='upstream-file-moved-or-removed', current=current))
            continue
        old, new = surface(baseline.get(path, '')), surface(target.read_text(encoding='utf-8-sig', errors='replace'))
        if current != new:
            result['files'].append(dict(path=path, status='api13-surface-unchanged-upstream-differs' if current == old else 'ported-surface-diverges-upstream', api13=old, current=current, upstream=new))
    return result


if __name__ == '__main__':
    projects = [x for x in json.loads((ROOT / 'migration/projects.json').read_text(encoding='utf-8')) if x['repository'] not in ['cycleapple/Dalamud', 'cycleapple/FFXIVClientStructs']]
    with concurrent.futures.ThreadPoolExecutor(4) as pool:
        results = [x for x in pool.map(review, projects) if x]
    (ROOT / 'migration/compatibility-surfaces.json').write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    for item in results:
        print(item['repository'], item['sourceFiles'], item['nativeSensitiveFiles'], len(item['files']))
