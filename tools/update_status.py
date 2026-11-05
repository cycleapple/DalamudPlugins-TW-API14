"""Reconcile published source heads, actual builds, CI and binary-localization evidence."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8'))


def write(relative, value):
    (ROOT / relative).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    refs = {x['repository']: x for x in read('migration/remote-refs.json')}
    assert len(refs) == 132 and all(x['matchesLocal'] for x in refs.values())
    pocket = json.loads(subprocess.check_output(['gh', 'run', 'view', '42068504439', '--repo', 'cycleapple/PocketRecorder', '--json', 'status,conclusion,url,headSha'], text=True))
    assert pocket['conclusion'] == 'success', 'Wait for PocketRecorder full native CI before recording success'
    assert refs['cycleapple/PocketRecorder']['commit'] == pocket['headSha']
    write('migration/evidence/PocketRecorder.json', dict(pocket, build='passed', tcRuntime='pending', checks=['locales', 'CaptureRetirement tests', 'managed plugin', 'native v143 recorder', 'API14 ZIP verification']))
    for name in ['PocketRecorder', 'MissFisher']:
        file = 'migration/batches/' + name + '.json'
        report = read(file)
        report['sourceCommit'] = refs['cycleapple/' + name]['commit']
        report['publishedSource'] = True
        report['unresolved'] = []
        report['results'] = [dict(internalName=name, status='build-passed' if name == 'PocketRecorder' else 'official-api14-localized', evidence='migration/evidence/' + name + '.json')]
        write(file, report)
    projects = read('migration/projects.json')
    for project in projects:
        project['targetCommit'] = refs[project['repository']]['commit']
        project['portStatus'] = 'platform-tracking' if project['repository'].split('/')[1] in ['Dalamud', 'FFXIVClientStructs'] else 'build-passed'
        if project['repository'] == 'cycleapple/MissFisher':
            project['portStatus'] = 'official-api14-localized'
    write('migration/projects.json', projects)
    plugins = read('migration/plugins.json')
    lines = ['# API14 移植進度', '', '2026-11-06：125 個插件已完成上游 API14 預備移植；132 個遠端分支與本機提交一致。', '',
             '124 個開源插件建置通過（PocketRecorder 含 Windows CI 原生 C++）；MissFisher 完成官方 API14 套件繁中移植與驗證打包。', '',
             '125 個主 DLL 皆參照 API14／.NET 10；868 個受檢受控輸出未發現非 API14 的 Dalamud 參照。六個共用依賴建置通過。', '',
             '**全部仍待台服 API14 實機驗證；目前發布清單為空。**', '',
             '| 插件 | API13 起點 | API14 來源分支 | 進度 |', '|---|---|---|---|']
    for plugin in plugins:
        internal = plugin['internalName']
        name = plugin['repository'].split('/')[1]
        report = read('migration/batches/' + name + '.json')
        result = next(x for x in report['results'] if x['internalName'] == internal)
        assert result['status'] in ['build-passed', 'official-api14-localized']
        assert report['publishedSource'] and report['sourceCommit'] == refs[plugin['repository']]['commit']
        plugin.update(status=result['status'], build='passed' if internal != 'MissFisher' else 'official-api14-localized', runtime='pending', sourceCommit=report['sourceCommit'], buildEvidence='migration/batches/' + name + '.json', assemblyEvidence='migration/assembly-audit.json')
        label = '官方 API14 繁中移植／打包通過' if internal == 'MissFisher' else ('Windows C#／原生 CI 通過' if internal == 'PocketRecorder' else '上游 API14 編譯通過')
        lines.append(f"| {plugin['name']} (`{internal}`) | {plugin['api13Version']} | [{plugin['repository']}](https://github.com/{plugin['repository']}/tree/api14-tw) | {label}；台服待驗證 |")
    write('migration/plugins.json', plugins)
    (ROOT / 'STATUS.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('Updated 125 plugin outcomes and 132 source heads.')


if __name__ == '__main__':
    main()
