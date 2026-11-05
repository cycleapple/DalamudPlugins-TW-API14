"""Compare native delegate ABIs and explicit field offsets, independently of compilation."""
import json
import re
from pathlib import Path
from port_batch import ROOT, WORK


def contracts(text):
    text = re.sub(r'/\*.*?\*/|//[^\n]*', '', text, flags=re.S)
    delegates = {}
    for m in re.finditer(r'\bdelegate\s+([^;{}]+?)\s+(\w+)\s*\(([^;{}]*)\)\s*;', text):
        ret, name, parameters = m.groups()
        if not re.search(r'(?:Hook|HookFrom\w*|CreateHook)\s*<\s*' + name + r'\s*>', text):
            continue
        types = []
        for param in parameters.split(','):
            param = re.sub(r'\[[^\]]+\]', '', param).split('=')[0].strip()
            if param:
                types.append(' '.join(param.split()[:-1]))
        delegates[name] = dict(returns=' '.join(ret.split()), parameters=types)
    constants = dict(re.findall(r'const\s+(?:u?int|long)\s+(\w+)\s*=\s*(0x[\da-fA-F]+|\d+)\s*;', text))
    fields = {}
    scopes = []
    for declaration in re.finditer(r'\b(?:struct|class)\s+(\w+)[^{;]*\{', text):
        depth = 1
        end = declaration.end()
        while end < len(text) and depth:
            depth += (text[end] == '{') - (text[end] == '}')
            end += 1
        scopes.append((declaration.end(), end, declaration[1]))
    for m in re.finditer(r'\[FieldOffset\(([^)]+)\)\]\s*(?:(?:public|private|internal|protected|unsafe|readonly|static)\s+)+[^;{}=]+?\s+(\w+)\s*[;=]', text):
        expression, name = m.groups()
        for key, value in constants.items():
            expression = re.sub(r'\b' + key + r'\b', value, expression)
        if re.fullmatch(r'[\dxa-fA-F+\s]+', expression):
            try:
                owner = '.'.join(scope[2] for scope in scopes if scope[0] <= m.start() < scope[1])
                fields[owner + '.' + name] = sum(int(part.strip(), 0) for part in expression.split('+'))
            except ValueError:
                pass
    return delegates, fields


def main():
    reviews = json.loads((ROOT / 'migration/compatibility-surfaces.json').read_text(encoding='utf-8'))
    findings = []
    for review in reviews:
        name = review['repository'].split('/')[1]
        top = WORK / 'sources' / name
        if not (top / '.git').exists():
            top = WORK / 'dependencies' / name
        upstream = WORK / 'references/upstream-review' / name / 'source'
        if not upstream.exists():
            continue
        by_name = {}
        for candidate in upstream.rglob('*.cs'):
            by_name.setdefault(candidate.name, []).append(candidate)
        for item in review['files']:
            path = item['path']
            old = top / path
            new = upstream / path
            if not new.exists():
                matches = by_name.get(old.name, [])
                if len(matches) != 1:
                    continue
                new = matches[0]
            left = contracts(old.read_text(encoding='utf-8-sig'))
            right = contracts(new.read_text(encoding='utf-8-sig'))
            for kind, a, b in [('delegate', left[0], right[0]), ('field-offset', left[1], right[1])]:
                for symbol in a.keys() & b.keys():
                    if a[symbol] != b[symbol]:
                        resolution = None
                        if name == 'Ktisis' and symbol == 'CalcBoneModelSpaceDelegate':
                            resolution = 'ABI-equivalent: nint and native pointer return; ref hkaPose and hkaPose* both pass one pointer on x64.'
                        if name == 'Penumbra' and path.endswith('/DebugHook.cs'):
                            resolution = 'Inactive DEBUG-only placeholder with empty signature; not an enabled Release hook.'
                        findings.append(dict(repository=review['repository'], path=path, upstreamPath=new.relative_to(upstream).as_posix(), kind=kind, symbol=symbol, current=a[symbol], upstream=b[symbol], upstreamEvidence=review['upstreamStatus'], resolution=resolution))
    (ROOT / 'migration/native-contract-review.json').write_text(json.dumps(findings, indent=2) + '\n', encoding='utf-8')
    for item in findings:
        print(item)


if __name__ == '__main__':
    main()
