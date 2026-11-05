"""Verify every published branch against its local source head (platform refs are tracking-only)."""
import concurrent.futures
import json
from port_batch import ROOT, WORK, run


def inspect(project):
    name = project['repository'].split('/')[1]
    top = WORK / ('sources' if project['kind'] == 'plugin' else 'dependencies') / name
    local = run(['git', 'rev-parse', 'HEAD'], top) if (top / '.git').exists() else project['targetCommit']
    remote = json.loads(run(['gh', 'api', 'repos/' + project['repository'] + '/git/ref/heads/api14-tw']))['object']['sha']
    return dict(repository=project['repository'], branch='api14-tw', commit=remote, matchesLocal=remote == local,
                verification='local-git-head' if (top / '.git').exists() else 'platform-tracking-pin')


if __name__ == '__main__':
    projects = json.loads((ROOT / 'migration/projects.json').read_text(encoding='utf-8'))
    with concurrent.futures.ThreadPoolExecutor(6) as pool:
        records = list(pool.map(inspect, projects))
    (ROOT / 'migration/remote-refs.json').write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
    failures = [record for record in records if not record['matchesLocal']]
    print(f"Verified {len(records)} remote branches; {len(failures)} mismatches.")
    if failures:
        print(failures)
        raise SystemExit(1)
