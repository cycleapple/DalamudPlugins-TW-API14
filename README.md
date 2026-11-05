# DalamudPlugins-TW-API14

台服 Dalamud API14 統一插件庫，整合原本的外觀庫
[DalamudPlugins-TW](https://github.com/cycleapple/DalamudPlugins-TW) 與
[API13-Extended](https://github.com/cycleapple/DalamudPlugins-TW-API13-Extended)。

125 個插件已納入 API14 預備移植與第二輪實質複查：124 個開源插件通過建置，
MissFisher 使用找回的官方 API14 套件完成繁中資源移植與打包。
125 個主 DLL 的實際參照均為 API14／.NET 10；868 個受檢受控輸出沒有非 API14 的 Dalamud 參照。
六個共用依賴已完成建置；132 個相關 repo 均使用 `api14-tw` 分支。

台服 API14 的原生結構、資料表、Hook、IPC 與遊戲內功能尚待實機驗證，
因此 `repo.json` 保持空清單。上游編譯通過不代表已可在台服正式使用。
兩個 API13 發布庫繼續獨立維護，API14 不覆蓋其安裝網址或正式套件。

## 未來的統一安裝網址

```text
https://raw.githubusercontent.com/cycleapple/DalamudPlugins-TW-API14/main/repo.json
```

只有完成 API14 編譯與台服遊戲內驗證的套件才會加入清單。目前加入此網址不會提供插件。

本輪查出並修正原生 Hook ABI、結構與資料表偏移、ImGui bindings、遺漏的原生核心及安裝包宣告。
完整上游來源、例外、檢查結果與實機限制見 [125 個插件實質複查](UPSTREAM_REVIEW.md)。
固定建置基線已更新至最後的官方穩定 API14：Dalamud 14.0.5.1。

## 移植資料

- [移植流程與順序](MIGRATION.md)
- [125 個插件的移植進度表](STATUS.md)
- [合併後的插件進度](migration/plugins.json)：以 `InternalName` 去重，保留兩庫原始版本與來源。
- [來源分支與精確 commit](migration/projects.json)：插件及共用依賴的 `api14-tw` 分支。
- [實際主 DLL 參照](migration/assembly-audit.json)、[受控相依 DLL 檢查](migration/dependency-audit.json)。
- [六個共用依賴建置結果](migration/shared-dependencies.json)、[遠端分支核對](migration/remote-refs.json)。
- [MissFisher 官方 API14 來源與繁中打包證據](migration/evidence/MissFisher.json)。
- [兩個 API13 發布清單快照](migration/baselines/)：以 GitHub 正式庫的固定 commit 為準。
- `migration/local-sources.json`：本機來源與尚未提交的追蹤檔修改；修改不會自動提交或搬到 API14。

本倉庫集中發布與移植追蹤，插件原始碼仍在各自的 GitHub repo，統一使用 `api14-tw` 分支。
相同插件僅保留一筆發布項目；Brio、Glamourer 等重複項目採數值較新的 API13 正式版本作為起點。

## 檢查

```sh
python tools/validate_repo.py
```

檢查兩庫合併覆蓋率、分支準備結果、API level、下載來源及驗證紀錄。
新增正式套件時需同時提交 `validation/<InternalName>.json`，詳見移植流程。

各插件分支提供 `.api14/build.ps1`，會初始化固定子模組並驗證、套用 API14 修正。
MissFisher 使用 `tools/Build-Api14.ps1`；PocketRecorder 另有 Windows CI 驗證原生 C++ 及套件。
統一庫的批次工具可用 `API14_DOTNET` 指定 .NET 10 執行檔、`DALAMUD_HOME` 指定 API14 SDK 目錄。
