# API14 移植工作流程

## 已完成的預備移植

124 個開源插件已通過上游 API14 建置，其中 PocketRecorder 的完整 C#／原生 C++、測試與打包由 Windows CI 驗證。MissFisher 主程式未開源，使用保留官方歷史的鏡像取得 API14 1.9.20.0，驗證 SHA256 及實際 DLL 參照後移植繁中資源，產生 1.9.20.1；方法內容與非語系資源保持一致。

125 個主 DLL 及 868 個受控輸出已檢查實際參照。六個共用依賴已建置；Dalamud 與 FFXIVClientStructs 的台服分支保留平台追蹤狀態，不能以變更 API 數字替代台服原生結構驗證。所有插件的台服實機驗證仍待 API14 環境。

移植涵蓋 .NET 10、SDK、服務介面、原生型別、Excel row／subrow、UI 與跨插件相依。子模組保留原始固定 commit，API14 差異以 `.api14/patches/` 記錄雜湊並由建置腳本套用；新加入的來源相依同樣固定版本。原 API13 checkout 不切換。

InventoryTools 與 Questionable 的 GitHub 乾淨副本已成功初始化子模組、套用固定修正並完成 Release 建置（Questionable 包含 GatheringPathRenderer）。此項驗證確認修正可重現，不代表原生功能已通過遊戲內測試。

部分資料在上游已移除，例如補充資料庫不再提供地城寶箱座標；移植版保留寶箱識別與副本資訊並移除無效座標顯示。SharpDX 使用明確的私有套件相依，避免依靠 API14 不再隨附的檔案。MissFisher 本輪沿用 981 個既有譯文，另新增 26 個字串由 OpenCC 轉換，仍需人工用語審閱。

第二輪以最後官方 stable 14.0.5.1 複查；已額外修正原生 ABI、欄位偏移、資料表及安裝 ZIP。
Aetherment Rust 核心和 Raphael 原生 solver 均確認包含在套件中；Aetherment、AutoRetainer、SimpleTweaks 的 GitHub 乾淨副本亦可重建。
逐插件上游來源與尚未證明的項目見 [完整複查](UPSTREAM_REVIEW.md)。

## 基線與順序

1. 確認台服 API14 Dalamud、對應 FFXIVClientStructs、Lumina 與 ImGui bindings 的固定版本。
2. 先移植共用依賴：FFXIVClientStructs、ECommons、OtterGui、Penumbra.GameData、CriticalCommonLib、KamiToolKit、AutoRetainerAPI。
3. 外觀鏈：Penumbra → Glamourer → CustomizePlus／SimpleHeels → Brio／Ktisis／LopClient。
4. 自動化鏈：vnavmesh → Lifestream／AutoHook／Artisan → GatherBuddy／Questionable／AutoDuty／ICE；逐一核對 IPC。
5. 其餘插件依 API、Hook、原生資產、跨插件依賴分批處理。

上游 API14 對應 .NET 10。參考
[官方 API14 移植說明](https://dalamud.dev/versions/v14/) 與
[API 版本表](https://dalamud.dev/versions/)。台服 SDK／組件尚未固定前，
上游參考建置與台服可發布建置需分開記錄；禁止用 API13 DLL 宣稱 API14 編譯成功。

## 每個插件

1. 從 `migration/projects.json` 指定的 `api14-tw` 分支建立獨立工作目錄。原 API13 checkout 不切換。
2. 核對來源 commit 與 API13 發布版本；檢視 `local-sources.json` 的未提交修正是否仍需移入。
3. 保留台服語言頁、世界 ID、特徵碼、ClientStructs 差異、功能修正與 zh-TW 資源；不得直接換成上游最新 API15。
4. 使用 API14 SDK／.NET 10 與固定的 API14 依賴，調整服務、結構、渲染與 IPC。修改 manifest 只是其中一步。
5. 完成 Release 編譯，檢查實際 DLL 參考、內嵌語系、原生依賴與 ZIP manifest。
6. 在對應台服版本驗證載入、登入、切區、設定保存及核心功能。依賴型插件需驗證整條 IPC／外觀鏈。
7. 更新 `migration/plugins.json` 的狀態與證據，再建立唯一版本 ZIP、SHA-256 與驗證紀錄。
8. 上傳至本 API14 庫的 release；更新 `repo.json`，執行驗證後發布。

`queued` → `porting` → `build-passed` → `tc-runtime-passed` → `published`。
分支建立不會自動把狀態設成 `porting` 或 `build-passed`。

## 發布驗證紀錄

`validation/<InternalName>.json` 範例（值須由實際產物與檢查填入）：

```json
{
  "internalName": "PluginName",
  "version": "1.0.0.0",
  "apiLevel": 14,
  "sourceCommit": "完整 40 位 commit SHA",
  "dalamudAssemblyVersion": "14.x.x.x",
  "build": "passed",
  "tcRuntime": "passed",
  "buildEvidence": "建置紀錄 URL 或 repo 內路徑，含固定依賴版本",
  "runtimeEvidence": "台服版本、測試日期、測試項目與結果",
  "fileName": "PluginName-1.0.0.0.zip",
  "sha256": "實際 ZIP 的 64 位 SHA-256",
  "downloadUrl": "https://github.com/cycleapple/DalamudPlugins-TW-API14/releases/download/plugins-api14/PluginName-1.0.0.0.zip"
}
```

驗證器檢查紀錄完整性；人工仍須核對證據與實際套件，不能把通過 JSON 檢查當成執行驗證。

## 重新盤點

```powershell
python tools/prepare_migration.py --workspace E:\FFXIV\XIVLauncher --create-branches
```

此指令只在 cycleapple 的相關 repo 建立缺少的 `api14-tw` ref，不覆寫既有分支，
不切換本機 checkout，也不提交未完成修改。重新盤點更新來源與版本資料，
保留既有插件移植狀態與證據；執行後仍應檢視差異再提交。
