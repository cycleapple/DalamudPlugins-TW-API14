# API14 移植工作流程

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
