"""Vendor a pinned, source-built dependency as a submodule, preserving port patches."""
import os
from pathlib import Path
from port_batch import run, clone_tree
from port_dependencies import copy_changes


def add(top, source, name):
    top, source = Path(top), Path(source)
    relative = 'api14-deps/' + name
    dest = top / relative
    if not (dest / '.git').exists():
        run(['git', '-c', 'protocol.file.allow=always', 'submodule', 'add', '--force', str(source), relative], top)
    url = run(['git', 'remote', 'get-url', 'origin'], source)
    if not url.startswith('https://'):
        for parent in source.parents:
            manifest = parent / '.gitmodules'
            if not manifest.exists():
                continue
            entries = run(['git', 'config', '-f', str(manifest), '--get-regexp', r'^submodule\..*\.path$'], parent)
            for entry in entries.splitlines():
                key, value = entry.split(None, 1)
                if value.replace('\\', '/') == source.relative_to(parent).as_posix():
                    url = run(['git', 'config', '-f', str(manifest), key[:-5] + '.url'], parent)
                    break
            if url.startswith('https://'):
                break
    if not url.startswith('https://'):
        raise ValueError('Dependency needs a public, reproducible source URL: ' + str(source))
    run(['git', 'config', '-f', '.gitmodules', 'submodule.' + relative + '.url', url], top)
    clone_tree(source, dest, run(['git', 'rev-parse', 'HEAD'], source), run(['git', 'remote', 'get-url', 'origin'], source))
    copy_changes(source, dest)
    return dest


if __name__ == '__main__':
    import sys
    print(add(*sys.argv[1:]))
