"""Resolve manual-SDK projects through manifests; explicitly label date-only candidates."""
import concurrent.futures
import json
import urllib.parse
from pathlib import Path
from review_upstream import ROOT, OUT, CACHE, api, raw, major

OVERRIDES = {'BossmodReborn': 'FFXIV-CombatReborn/BossmodReborn', 'MapLinker': 'Bluefissure/MapLinker', 'DP-CustomResolution': '0x0ade/DalamudPlugins'}


def review(file):
    data = json.loads(file.read_text(encoding='utf-8'))
    name = file.stem
    if data.get('api14Commit') or data.get('manualReviewVersion') == 1:
        return
    repo = OVERRIDES.get(name, data.get('upstreamRepository'))
    if not repo or name in ['Dalamud', 'FFXIVClientStructs', 'MissFisher']:
        return
    data['manualReviewVersion'] = 1
    try:
        info = api('repos/' + repo)
        data['upstreamRepository'] = repo
        candidates = api('repos/' + repo + '/commits?until=2026-04-28T23%3A59%3A59Z&per_page=1')
        if not candidates:
            raise ValueError('No pre-API15 history')
        candidate = candidates[0]
        sha = candidate['sha']
        tree = api('repos/' + repo + '/git/trees/' + sha + '?recursive=1')['tree']
        manifests = [x['path'] for x in tree if x['path'].endswith('.json') and not any(w in x['path'].lower() for w in ['resource', 'translat', 'localiz', 'preset', 'config', 'obj/', 'bin/'])]
        manifests.sort(key=lambda x: (not ('manifest' in x.lower() or name.lower() in x.lower()), len(x)))
        chosen = None
        for path in manifests[:14]:
            text = raw(repo, sha, path)
            if 'DalamudApiLevel' not in text:
                continue
            if major(text) == 14:
                chosen = sha
            elif major(text) and major(text) > 14:
                history = api('repos/' + repo + '/commits?path=' + urllib.parse.quote(path) + '&per_page=100')
                previous = None
                for entry in history:
                    if major(raw(repo, entry['sha'], path)) == 14:
                        chosen = entry['sha']
                        if previous and previous['parents']:
                            parent = previous['parents'][0]['sha']
                            if major(raw(repo, parent, path)) == 14:
                                chosen = parent
                                data['nextApiCommit'] = previous['sha']
                        break
                    previous = entry
            if chosen:
                detail = api('repos/' + repo + '/commits/' + chosen)
                data.update(apiMarkerPath=path, api14Commit=chosen, api14Date=detail['commit']['committer']['date'], api14Url=f'https://github.com/{repo}/commit/{chosen}', upstreamStatus='api14-manifest-confirmed')
                break
        if not chosen:
            data.update(api14CandidateCommit=sha, candidateDate=candidate['commit']['committer']['date'], upstreamStatus='date-candidate-requires-api-evidence')
    except Exception as exc:
        data.update(manualReviewError=str(exc)[:300])
    file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(name, data.get('upstreamStatus'), flush=True)


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(6) as pool:
        list(pool.map(review, OUT.glob('*.json')))
