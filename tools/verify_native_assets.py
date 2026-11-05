"""Read native PE exports and ZIP contents without loading plugin/native code."""
import hashlib
import json
import struct
import zipfile
from pathlib import Path
from port_batch import ROOT, WORK


def exports(path):
    data = path.read_bytes()
    u16 = lambda offset: struct.unpack_from('<H', data, offset)[0]
    u32 = lambda offset: struct.unpack_from('<I', data, offset)[0]
    pe = u32(0x3c)
    assert data[pe:pe + 4] == b'PE\0\0'
    assert u16(pe + 4) == 0x8664, 'Native plugin dependency must be x64'
    optional = pe + 24
    assert u16(optional) == 0x20b
    sections = optional + u16(pe + 20)
    def offset(rva):
        for i in range(u16(pe + 6)):
            section = sections + i * 40
            start = u32(section + 12)
            if start <= rva < start + max(u32(section + 8), u32(section + 16)):
                return rva - start + u32(section + 20)
        raise ValueError('Export RVA outside PE sections')
    directory = offset(u32(optional + 112))
    count = u32(directory + 24)
    names = offset(u32(directory + 32))
    result = set()
    for i in range(count):
        name = offset(u32(names + i * 4))
        result.add(data[name:data.index(b'\0', name)].decode('ascii'))
    return result


def main():
    records = []
    for name, folder, dll, symbols, extra in [
        ('Aetherment', 'aetherment/plugin/plugin/bin/Release', 'aetherment_core.dll',
         ['initialize', 'destroy', 'draw', 'command', 'config_plugin_open_on_launch', 'backend_penumbraipc_modchanged'], ['bcryptprimitives.dll']),
        ('Raphael.Dalamud', 'Raphael.Dalamud/Raphael.Dalamud/bin/Release', 'raphael_bindings.dll', ['solve'], ['raphael-cli.exe']),
    ]:
        directory = WORK / 'sources' / folder
        native = directory / dll
        assert set(symbols) <= exports(native), f'Missing native exports: {dll}'
        package = directory / name / 'latest.zip'
        with zipfile.ZipFile(package) as archive:
            for required in [dll, name + '.dll', name + '.json', *extra]:
                assert required in archive.namelist(), f'Missing runtime file: {required}'
                assert archive.read(required) == (directory / required).read_bytes(), f'Stale packaged file: {required}'
            assert json.loads(archive.read(name + '.json'))['DalamudApiLevel'] == 14
        records.append(dict(internalName=name, nativeDll=dll, sha256=hashlib.sha256(native.read_bytes()).hexdigest(),
                            requiredExports=symbols, packageFiles='passed', apiLevel=14, architecture='AMD64',
                            nativeBuild='passed-rust-locked' if name == 'Aetherment' else 'provided-version-independent-solver', tcRuntime='pending'))
    (ROOT / 'migration/evidence/native-assets.json').write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
    print('Passed: native x64 exports, required runtime files, exact packaged DLL bytes and API14 manifests for Aetherment and Raphael.')


if __name__ == '__main__':
    main()
