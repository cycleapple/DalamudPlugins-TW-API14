"""Locate an upstream API14 boundary from actual project history, retaining evidence."""
import concurrent.futures
import json
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'migration/upstream-review'
CACHE = ROOT.parent / 'references/upstream-review'
CACHE.mkdir(parents=True, exist_ok=True)


def api(path):
    return json.loads(subprocess.check_output(['gh', 'api', path], encoding='utf-8', stderr=subprocess.PIPE))


def raw(repo, ref, path):
    url = f'https://raw.githubusercontent.com/{repo}/{ref}/{urllib.parse.quote(path)}'
    try:
        return urllib.request.urlopen(url, timeout=35).read().decode('utf-8-sig')
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return ''
        raise


def major(text):
    matches = re.findall(r'Dalamud\.(?:CN\.)?NET\.Sdk["\s/=]+(\d+)\.', text, re.I)
    if not matches:
        matches = re.findall(r'(?:DalamudApiLevel>\s*|"DalamudApiLevel"\s*:\s*)(\d+)', text)
    if not matches:
        matches = re.findall(r'DalamudPackager["\s]+Version="(\d+)\.', text, re.I)
    return int(matches[0]) if matches else None


def review(project):
    name = project['repository'].split('/')[1]
    file = OUT / (name + '.json')
    data = json.loads(file.read_text(encoding='utf-8'))
    if data.get('reviewVersion') == 1:
        return name, data.get('upstreamStatus')
    data['reviewVersion'] = 1
    parent = data['parent']['full_name']
    # These maintained derivatives intentionally differ from their original fork roots.
    canonical = {'Artisan': 'PunishXIV/Artisan', 'WrathCombo': 'PunishXIV/WrathCombo', 'IINACT': 'marzent/IINACT'}
    repo = canonical.get(name, parent)
    data['upstreamRepository'] = repo
    if not repo:
        data['upstreamStatus'] = 'self-maintained-or-unresolved'
        file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        return name, data['upstreamStatus']
    try:
        info = api('repos/' + repo)
        branch = info['default_branch']
        head = api('repos/' + repo + '/commits/' + urllib.parse.quote(branch, safe=''))
        ref = head['sha']
        data.update(upstreamDefaultBranch=branch, upstreamHead=ref)
        batch = ROOT / 'migration/batches' / (name + '.json')
        paths = []
        if batch.exists():
            paths = [r['project'] for r in json.loads(batch.read_text(encoding='utf-8'))['results'] if r.get('project')]
        if not paths:
            paths = [name + '.csproj', name + '/' + name + '.csproj']
        probe = []
        for path in paths:
            for p in [path, str(Path(path).parent / 'Directory.Build.props').replace('\\', '/'), 'Directory.Build.props']:
                if p not in probe:
                    probe.append(p)
        selected = None
        for path in probe:
            text = raw(repo, ref, path)
            if major(text):
                selected = path
                break
        if not selected:
            tree = api('repos/' + repo + '/git/trees/' + ref + '?recursive=1')['tree']
            candidates = [x['path'] for x in tree if x['path'].endswith('.csproj') and not any(w in x['path'].lower() for w in ['test', 'mock', 'vendor', 'submodule'])]
            candidates += [x['path'] for x in tree if x['path'].endswith('Directory.Build.props')]
            for path in candidates[:12]:
                text = raw(repo, ref, path)
                if major(text):
                    selected = path
                    break
        if not selected:
            data.update(upstreamStatus='manual-reference-project-needs-review')
        else:
            data['apiMarkerPath'] = selected
            data['headApiLevel'] = major(text)
            if major(text) == 14:
                chosen = ref
                evidence = text
                data['upstreamStatus'] = 'api14-head-confirmed'
            else:
                history = api('repos/' + repo + '/commits?path=' + urllib.parse.quote(selected) + '&per_page=100')
                chosen = None
                previous = None
                for entry in history:
                    contents = raw(repo, entry['sha'], selected)
                    level = major(contents)
                    if level == 14:
                        chosen = entry['sha']
                        evidence = contents
                        # The parent of the next project change captures intervening fixes,
                        # rather than merely the last csproj edit.
                        if previous and previous.get('parents'):
                            boundary = previous['parents'][0]['sha']
                            candidate = raw(repo, boundary, selected)
                            if major(candidate) == 14:
                                chosen, evidence = boundary, candidate
                                data['nextApiCommit'] = previous['sha']
                        data['upstreamStatus'] = 'last-api14-before-project-upgrade'
                        break
                    previous = entry
                if not chosen:
                    data['upstreamStatus'] = 'no-api14-project-history-found'
            if chosen:
                detail = api('repos/' + repo + '/commits/' + chosen)
                data.update(api14Commit=chosen, api14Date=detail['commit']['committer']['date'], api14Message=detail['commit']['message'].splitlines()[0], api14Url=f'https://github.com/{repo}/commit/{chosen}')
                folder = CACHE / name
                folder.mkdir(exist_ok=True)
                (folder / 'project-marker.txt').write_text(evidence, encoding='utf-8')
    except Exception as exc:
        data.update(upstreamStatus='lookup-error', error=str(exc)[:600])
    file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return name, data.get('upstreamStatus')


if __name__ == '__main__':
    projects = json.loads((ROOT / 'migration/projects.json').read_text(encoding='utf-8'))
    with concurrent.futures.ThreadPoolExecutor(6) as pool:
        for name, status in pool.map(review, projects):
            print(name, status, flush=True)
