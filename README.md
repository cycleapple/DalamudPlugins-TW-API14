# DalamudPlugins-TW-API14

台服 Dalamud API14 統一插件庫，整合原本的外觀庫
[DalamudPlugins-TW](https://github.com/cycleapple/DalamudPlugins-TW) 與
[API13-Extended](https://github.com/cycleapple/DalamudPlugins-TW-API13-Extended)。

目前為移植準備階段，`repo.json` 保持空清單。建立 `api14-tw` 分支只代表
已保留 API13 台服修正與繁中翻譯基線，不代表插件已相容 API14。
兩個 API13 發布庫繼續獨立維護，API14 不覆蓋其安裝網址或正式套件。

## 未來的統一安裝網址

```text
https://raw.githubusercontent.com/cycleapple/DalamudPlugins-TW-API14/main/repo.json
```

只有完成 API14 編譯與台服遊戲內驗證的套件才會加入清單。目前加入此網址不會提供插件。

## 移植資料

- [移植流程與順序](MIGRATION.md)
- [125 個插件的移植進度表](STATUS.md)
- [合併後的插件進度](migration/plugins.json)：以 `InternalName` 去重，保留兩庫原始版本與來源。
- [來源分支與精確 commit](migration/projects.json)：插件及共用依賴的 `api14-tw` 分支。
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
