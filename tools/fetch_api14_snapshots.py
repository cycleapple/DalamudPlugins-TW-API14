"""Download only text/code from confirmed API14 commits, never the current API15 tree."""
import concurrent.futures
import io
import json
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT.parent / 'references/upstream-review'


def fetch(file):
    data = json.loads(file.read_text(encoding='utf-8'))
    sha, repo = data.get('api14Commit') or data.get('api14CandidateCommit'), data.get('upstreamRepository')
    if not sha:
        return
    folder = DEST / file.stem / 'source'
    stamp = folder.parent / 'snapshot-commit.txt'
    if stamp.exists() and stamp.read_text() == sha:
        return
    if stamp.exists() and folder.exists():
        assert folder.resolve().is_relative_to(DEST.resolve())
        for old in folder.rglob('*'):
            if old.is_file():
                old.unlink()
    raw = urllib.request.urlopen(f'https://codeload.github.com/{repo}/zip/{sha}', timeout=180).read()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for item in archive.infolist():
            relative = Path(*Path(item.filename).parts[1:])
            if relative.is_absolute() or '..' in relative.parts:
                raise ValueError('Unsafe archive path')
            if item.is_dir() or (relative.suffix.lower() not in ['.cs', '.csproj', '.props', '.targets', '.json', '.toml', '.yml', '.yaml', '.md'] and relative.name != '.gitmodules'):
                continue
            output = folder / relative
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(archive.read(item))
    stamp.write_text(sha)
    print(file.stem, sha[:12], len(raw), flush=True)


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(6) as pool:
        list(pool.map(fetch, (ROOT / 'migration/upstream-review').glob('*.json')))
