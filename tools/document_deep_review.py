"""Render evidence-based upstream cards; do not infer runtime success from static checks."""
import json
from collections import Counter
from pathlib import Path
from port_batch import ROOT, WORK


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def main():
    miss = read('../sources/MissFisher/.api14/artifacts/verification.json')
    miss.update(officialVersion='1.9.20.0', officialCommit='225828c5f5d980515d0e025ebcf962ff9a23fc25',
                officialArchiveSha256='f3d7ce58e5414730b5fde79e4976d9132801cb91c8a7b6a169964833a7d10966',
                officialDalamudVersion='14.0.4.5', build='official-api14-localized', tcRuntime='pending',
                negativeCheckApi13='passed-previous-recipe-same-patcher',
                retainedTranslations=981, newOpenCCConversions=26,
                excludedPreview=dict(version='1.9.21.0', commit='72f22ff2130a8d3ac4a84577b58d838f8dd7dd2f',
                                     reason='Preview release; references 14.0.5.2, newer than pinned last stable 14.0.5.1.'),
                packagePath=str(WORK / 'sources/MissFisher/.api14/artifacts/MissFisher-1.9.20.1.zip'))
    (ROOT / 'migration/evidence/MissFisher.json').write_text(json.dumps(miss, indent=2) + '\n', encoding='utf-8')
    file = ROOT / 'migration/upstream-review/MissFisher.json'
    data = json.loads(file.read_text(encoding='utf-8'))
    data.update(api14Commit=miss['officialCommit'], api14Date='2026-04-10', upstreamStatus='official-api14-binary-confirmed',
                api14Url='https://github.com/QianChangUwU/MissFisher/commit/' + miss['officialCommit'],
                provenance='Official author release preserved by mirror; actual DLL reference and archive hash checked.')
    file.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (WORK / 'sources/MissFisher/API14_PORT.md').write_text('''# MissFisher API14 localization port

The main plugin is closed source. This branch localizes a real official API14 binary.

- Stable upstream 1.9.20.0, author MistyDai; preserved mirror commit `225828c5f5d980515d0e025ebcf962ff9a23fc25` (2026-04-10).
- [Pinned archive](https://raw.githubusercontent.com/QianChangUwU/MissFisher/225828c5f5d980515d0e025ebcf962ff9a23fc25/latest.zip)
- SHA256 `f3d7ce58e5414730b5fde79e4976d9132801cb91c8a7b6a169964833a7d10966`.
- Actual references: Dalamud 14.0.4.5, System.Runtime 10.0.0.0.
- Localized 1.9.20.1: 1007/1007 keys, 981 retained translations and 26 new OpenCC s2twp conversions. Converted wording still needs review.
- The later 1.9.21.0 is a preview requiring Dalamud 14.0.5.2; it is not used with the pinned final stable 14.0.5.1 SDK.

Build: `./tools/Build-Api14.ps1 -DalamudHome C:/path/to/api14 -Dotnet C:/path/to/dotnet.exe`.
The recipe verifies the input archive hash and actual API14/.NET10 references, and verifies that method bodies and all nine non-language resources remain unchanged. Output and verification are in `.api14/artifacts/`.
Legacy root API13 archives/resources are not inputs to this recipe. TC runtime verification remains pending; no public feed entry is enabled.
''', encoding='utf-8')
    reviews = {p.stem: json.loads(p.read_text(encoding='utf-8')) for p in (ROOT / 'migration/upstream-review').glob('*.json')}
    plugins = read('migration/plugins.json')
    for plugin in plugins:
        name = plugin['repository'].split('/')[1]
        review = reviews[name]
        plugin.update(upstreamApi14Commit=review.get('api14Commit'), upstreamReviewStatus=review['upstreamStatus'],
                      deepReviewEvidence='UPSTREAM_REVIEW.md', runtime='pending')
    (ROOT / 'migration/plugins.json').write_text(json.dumps(plugins, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for name, review in reviews.items():
        if name in ['Dalamud', 'FFXIVClientStructs', 'PocketRecorder']:
            continue
        top = WORK / 'sources' / name
        if not top.exists():
            top = WORK / 'dependencies' / name
        if not top.exists():
            continue
        folder = top / '.api14'
        folder.mkdir(exist_ok=True)
        proof = f"[Pinned upstream API14 evidence]({review['api14Url']})" if review.get('api14Commit') else 'No independently confirmed upstream API14 revision; date-only candidates are not API14 proof.'
        (folder / 'REVIEW.md').write_text(f'''# API14 deep review — {name}

2026-11-06. Upstream status: `{review['upstreamStatus']}`.
{proof}

Build reference: official stable Dalamud 14.0.5.1, distribution commit `6fb2b12018922bddeef009edd26082f068f8c602`.
This branch preserves TC features/resources and selectively ports compatibility changes; it does not claim complete feature parity with a newer upstream release.

The [central review](https://github.com/cycleapple/DalamudPlugins-TW-API14/blob/main/UPSTREAM_REVIEW.md) records source/delegate/layout/schema/SDK resolution/package/native-asset checks and their scope. Source declarations and successful compilation cannot prove scan signatures, IPC semantics, game data or native behavior in the TC client. TC API14 runtime validation remains pending.
''', encoding='utf-8')
    counts = Counter(r['upstreamStatus'] for r in reviews.values())
    lines = ['# API14 上游與實質移植複查', '', '2026-11-06；範圍：兩個 API13 正式清單去重後 125 個插件、124 個插件來源庫、6 個共用依賴及 2 個平台追蹤庫。', '',
             '## 基線選擇', '',
             '以實際仍宣告 API14 的上游來源、穩定發行包及 DLL 參照為準，優先選 API15 升級前最後的 API14 穩定版；日期只用於搜尋。不同插件有獨立 API14 分支、預覽版或在 API15 後才建立，不能假設每個插件都存在 API14 上游。', '',
             '官方 [v14 說明](https://dalamud.dev/versions/v14/) 的 August 6, 2025 與 [版本歷史](https://dalamud.dev/versions/) 記載的 API14 首次提交 2025-12-20 不一致；後者列 API15 為 2026-05-01。這些日期不是本次相容性判定依據。', '',
             '固定最後一份官方 stable API14 發行 DLL：14.0.5.1，2026-04-12，commit `6fb2b12018922bddeef009edd26082f068f8c602`。ZIP SHA256：`6a9f9aee19af4280f2d61680bbff960ae48e5dcaad70707baad857da2f9d8e48`。[下載及版本證據](migration/evidence/api14-final-sdk.json)。', '',
             'MissFisher 改採官方穩定 1.9.20.0 → 繁中 1.9.20.1；實際參照 14.0.4.5。更晚的 1.9.21.0 是預覽版且要求 14.0.5.2，因此未採用。[二進位與語系驗證](migration/evidence/MissFisher.json)。', '',
             '## 本輪查出並修正的實質問題', '',
             '- Splatoon、兩個 BossMod、JobBars、NecroLens、RotationSolver：ActorControl 原生轉呼叫補上 p7/p8；17 份 ECommons 來源（含共用庫）補齊 DirectorUpdate 原生 9 參數。',
             '- Penumbra Atch hook 回傳型別、Glamourer 武器 hook 尾端參數、NoClippy 動作／動畫鎖後端及 AllaganMarket 已失效的封包 hook。',
             '- Ktisis／VFXEditor 角色偏移、GatherBuddy 釣魚偏移、Artisan 配方、AutoRetainer 飛空艇、Housemate／ReMakePlace 房屋及 TitleEdit 移動欄位。',
             '- Brio 相機 FoV、物理暫停；Brio／Ktisis／VFXEditor 自訂角色建立資料表改用 SDK 型別，避免舊列寬和固定欄位偏移。',
             '- PandorasBox 的原生功能與 SimpleTweaks 的實際 API14 UI／動作列實作；保留繁中與原有功能，未直接照抄上游停用功能的空殼。',
             '- Hyperborea／Orbwalker 移除舊私有 ImGuiWindow 偏移；Craftimizer／MidiBard 改用現行 API14 bindings。',
             '- Aetherment 先前漏建 Rust 核心：現在鎖定 Cargo.lock 完整建置並打包；Raphael 原生 solver DLL 修正為實際進入輸出與 ZIP。',
             '- DozeAnywhere 混用宿主 ImGui 參照、Brio／MidiBard SDK 大小寫漏判、舊 Packager，以及 5 個 ZIP 仍帶 API13 manifest／文字編碼問題。', '',
             '## 驗證範圍與限制', '',
             '- 123 個一般插件專案以固定 14.0.5.1 完成 Release 建置與 MSBuild 實際參照路徑核對；PocketRecorder 的 C++／C#／套件另由 Windows CI 驗證。MissFisher 使用已驗證的官方 API14 DLL。',
             '- 125 個主 DLL 檢查實際 API14／.NET10 metadata，所有受檢受控輸出不得有其他 major 的 Dalamud 參照。[DLL](migration/assembly-audit.json)、[相依 DLL](migration/dependency-audit.json)、[參照解析](migration/reference-resolution.json)。',
             '- 針對已修正的 40 項高風險原生 ABI／layout，以編譯後 DLL metadata 比對 SDK／上游原生宣告；不是遊戲內執行測試。[檢查規格](migration/native-contract-expectations.json)。',
             '- 19 個自訂 Sheet 宣告中，18 個與 SDK schema hash 相符；1 個 Deliveroo 自訂對話表無 SDK schema 可比。[資料表](migration/schema-review.json)。',
             '- 122 個本機 ZIP 驗證 manifest14、主 DLL 與本次建置一致、未夾帶 Dalamud 等宿主 DLL。Brio／Penumbra 原建置設定不產 ZIP；PocketRecorder 套件由 Windows CI 檢查。[封裝](migration/package-review.json)。',
             '- Aetherment／Raphael 驗證 AMD64 原生 DLL、必要 exports 與 ZIP 內位元組一致；沒有載入原生程式執行 GPU／遊戲操作。[原生資產](migration/evidence/native-assets.json)。',
             '- 三方來源掃描涵蓋來源庫與共用依賴，產生原生敏感差異清單；差異可能是格式、功能版本或台服保留，不代表每個差異都已證明語意相容。[三方差異](migration/compatibility-surfaces.json)、[同名原生契約差異與處理說明](migration/native-contract-review.json)。',
             '- **仍未完成：台服 API14 實機載入、登入／切區／卸載、核心功能、Signature 掃描、IPC 互通及台服資料布局驗證。不能據此宣稱零遺漏或全部可正式使用。`repo.json` 仍為空。**', '',
             '## 上游證據分類（132 個相關庫）', '', '| 分類 | 數量 |', '|---|---:|']
    lines += [f'| `{key}` | {value} |' for key, value in sorted(counts.items())]
    lines += ['', '「API14 來源宣告」只能確認選定提交的建置目標，沒有等同遊戲執行驗證。日期候選不升格為 API14 已驗證。平台追蹤庫也不當成插件移植成功。', '', '## 125 個插件逐項記錄', '', '| 插件 | 上游 API14 證據 | 檢查狀態 |', '|---|---|---|']
    for plugin in plugins:
        name = plugin['repository'].split('/')[1]
        r = reviews[name]
        evidence = f"[{r['api14Commit'][:12]}]({r['api14Url']})" if r.get('api14Commit') else '未確認獨立 API14 上游'
        lines.append(f"| `{plugin['internalName']}` | {evidence}；`{r['upstreamStatus']}` | [來源分支](https://github.com/{plugin['repository']}/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |")
    (ROOT / 'UPSTREAM_REVIEW.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('Rendered 125 plugin review rows and source evidence cards.')


if __name__ == '__main__':
    main()
