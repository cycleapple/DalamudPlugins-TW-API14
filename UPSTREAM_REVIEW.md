# API14 上游與實質移植複查

2026-11-06；範圍：兩個 API13 正式清單去重後 125 個插件、124 個插件來源庫、6 個共用依賴及 2 個平台追蹤庫。

## 基線選擇

以實際仍宣告 API14 的上游來源、穩定發行包及 DLL 參照為準，優先選 API15 升級前最後的 API14 穩定版；日期只用於搜尋。不同插件有獨立 API14 分支、預覽版或在 API15 後才建立，不能假設每個插件都存在 API14 上游。

官方 [v14 說明](https://dalamud.dev/versions/v14/) 的 August 6, 2025 與 [版本歷史](https://dalamud.dev/versions/) 記載的 API14 首次提交 2025-12-20 不一致；後者列 API15 為 2026-05-01。這些日期不是本次相容性判定依據。

固定最後一份官方 stable API14 發行 DLL：14.0.5.1，2026-04-12，commit `6fb2b12018922bddeef009edd26082f068f8c602`。ZIP SHA256：`6a9f9aee19af4280f2d61680bbff960ae48e5dcaad70707baad857da2f9d8e48`。[下載及版本證據](migration/evidence/api14-final-sdk.json)。

MissFisher 改採官方穩定 1.9.20.0 → 繁中 1.9.20.1；實際參照 14.0.4.5。更晚的 1.9.21.0 是預覽版且要求 14.0.5.2，因此未採用。[二進位與語系驗證](migration/evidence/MissFisher.json)。

## 本輪查出並修正的實質問題

- Splatoon、兩個 BossMod、JobBars、NecroLens、RotationSolver：ActorControl 原生轉呼叫補上 p7/p8；17 份 ECommons 來源（含共用庫）補齊 DirectorUpdate 原生 9 參數。
- Penumbra Atch hook 回傳型別、Glamourer 武器 hook 尾端參數、NoClippy 動作／動畫鎖後端及 AllaganMarket 已失效的封包 hook。
- Ktisis／VFXEditor 角色偏移、GatherBuddy 釣魚偏移、Artisan 配方、AutoRetainer 飛空艇、Housemate／ReMakePlace 房屋及 TitleEdit 移動欄位。
- Brio 相機 FoV、物理暫停；Brio／Ktisis／VFXEditor 自訂角色建立資料表改用 SDK 型別，避免舊列寬和固定欄位偏移。
- PandorasBox 的原生功能與 SimpleTweaks 的實際 API14 UI／動作列實作；保留繁中與原有功能，未直接照抄上游停用功能的空殼。
- Hyperborea／Orbwalker 移除舊私有 ImGuiWindow 偏移；Craftimizer／MidiBard 改用現行 API14 bindings。
- Aetherment 先前漏建 Rust 核心：現在鎖定 Cargo.lock 完整建置並打包；Raphael 原生 solver DLL 修正為實際進入輸出與 ZIP。
- DozeAnywhere 混用宿主 ImGui 參照、Brio／MidiBard SDK 大小寫漏判、舊 Packager，以及 5 個 ZIP 仍帶 API13 manifest／文字編碼問題。

## 驗證範圍與限制

- 123 個一般插件專案以固定 14.0.5.1 完成 Release 建置與 MSBuild 實際參照路徑核對；PocketRecorder 的 C++／C#／套件另由 Windows CI 驗證。MissFisher 使用已驗證的官方 API14 DLL。
- 125 個主 DLL 檢查實際 API14／.NET10 metadata，所有受檢受控輸出不得有其他 major 的 Dalamud 參照。[DLL](migration/assembly-audit.json)、[相依 DLL](migration/dependency-audit.json)、[參照解析](migration/reference-resolution.json)。
- 針對已修正的 40 項高風險原生 ABI／layout，以編譯後 DLL metadata 比對 SDK／上游原生宣告；不是遊戲內執行測試。[檢查規格](migration/native-contract-expectations.json)。
- 19 個自訂 Sheet 宣告中，18 個與 SDK schema hash 相符；1 個 Deliveroo 自訂對話表無 SDK schema 可比。[資料表](migration/schema-review.json)。
- 122 個本機 ZIP 驗證 manifest14、主 DLL 與本次建置一致、未夾帶 Dalamud 等宿主 DLL。Brio／Penumbra 原建置設定不產 ZIP；PocketRecorder 套件由 Windows CI 檢查。[封裝](migration/package-review.json)。
- Aetherment／Raphael 驗證 AMD64 原生 DLL、必要 exports 與 ZIP 內位元組一致；沒有載入原生程式執行 GPU／遊戲操作。[原生資產](migration/evidence/native-assets.json)。
- 三方來源掃描涵蓋來源庫與共用依賴，產生原生敏感差異清單；差異可能是格式、功能版本或台服保留，不代表每個差異都已證明語意相容。[三方差異](migration/compatibility-surfaces.json)、[同名原生契約差異與處理說明](migration/native-contract-review.json)。
- **仍未完成：台服 API14 實機載入、登入／切區／卸載、核心功能、Signature 掃描、IPC 互通及台服資料布局驗證。不能據此宣稱零遺漏或全部可正式使用。`repo.json` 仍為空。**

GitHub 乾淨副本重建：[Aetherment、AutoRetainer、SimpleTweaks 的精確來源提交與結果](migration/evidence/clean-rebuilds.json)。

## 上游證據分類（132 個相關庫）

| 分類 | 數量 |
|---|---:|
| `api14-cutoff-source-confirmed` | 3 |
| `api14-head-confirmed` | 3 |
| `api14-manifest-confirmed` | 9 |
| `api14-package-source-confirmed` | 1 |
| `date-candidate-requires-api-evidence` | 8 |
| `explicit-api14-branch` | 1 |
| `last-api14-before-project-upgrade` | 96 |
| `manual-reference-project-needs-review` | 3 |
| `no-api14-project-history-found` | 2 |
| `official-api14-binary-confirmed` | 1 |
| `self-maintained-or-unresolved` | 5 |

「API14 來源宣告」只能確認選定提交的建置目標，沒有等同遊戲執行驗證。日期候選不升格為 API14 已驗證。平台追蹤庫也不當成插件移植成功。

## 125 個插件逐項記錄

| 插件 | 上游 API14 證據 | 檢查狀態 |
|---|---|---|
| `ActionTimelineReplacement` | [48ceaee8f61b](https://github.com/papapachin/ActionTimelineReplacement/commit/48ceaee8f61ba53509bd60869d6341774a0def2e)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/ActionTimelineReplacement/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Aetherment` | [f3d4e89590f1](https://github.com/Sevii77/aetherment/commit/f3d4e89590f1da47652b5490885fa0e4a2381517)；`api14-manifest-confirmed` | [來源分支](https://github.com/cycleapple/aetherment/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `AllaganItemSearch` | [09a2331d9227](https://github.com/Critical-Impact/AllaganItemSearch/commit/09a2331d922754923950684d72604de73a4cbc16)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/AllaganItemSearch/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `AllaganMarket` | [2a190e565019](https://github.com/Critical-Impact/AllaganMarket/commit/2a190e565019cc63bf2b0bed19b25b83d831899a)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/AllaganMarket/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `AntiAfkKick-Dalamud` | [f1c17eeb7c88](https://github.com/NightmareXIV/AntiAfkKick/commit/f1c17eeb7c88910312458abb96a0b8f7c95866c1)；`api14-manifest-confirmed` | [來源分支](https://github.com/cycleapple/AntiAfkKick/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Artisan` | [d49905965f30](https://github.com/PunishXIV/Artisan/commit/d49905965f304c285a6f042538706e5c148955e7)；`api14-manifest-confirmed` | [來源分支](https://github.com/cycleapple/Artisan/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `AutoDuty` | [058468a17611](https://github.com/erdelf/AutoDuty/commit/058468a17611ad3d538359cccf9cded4fbbcb277)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/AutoDuty/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `AutoHook` | [b99c2952e6ba](https://github.com/PunishXIV/AutoHook/commit/b99c2952e6baf2094430bbbf8ed5816639e6212c)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/AutoHook/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `AutoMinion` | 未確認獨立 API14 上游；`self-maintained-or-unresolved` | [來源分支](https://github.com/cycleapple/AutoMinion/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `AutoRetainer` | [6dde427e6056](https://github.com/PunishXIV/AutoRetainer/commit/6dde427e6056ee0a69270f2653dd6311c627bcc3)；`api14-manifest-confirmed` | [來源分支](https://github.com/cycleapple/AutoRetainer/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Automaton` | [41a6f46a6bdd](https://github.com/Jaksuhn/ffxiv-bundleoftweaks/commit/41a6f46a6bdd102f3a9db6302e60b1a57ec94e79)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/ffxiv-bundleoftweaks/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Avarice` | [8e47baf10258](https://github.com/PunishXIV/Avarice/commit/8e47baf10258c683ad093ef3147141e4b7d9e9d6)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Avarice/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `BDTHPlugin` | [4b3c734d20a2](https://github.com/LeonBlade/BDTHPlugin/commit/4b3c734d20a27f56b0fa1a908c3871c8c45ed32f)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/BDTHPlugin/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `BOCCHI` | [4dcc51928682](https://github.com/OhKannaDuh/BOCCHI/commit/4dcc519286823519b7105288627590e589911f21)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/BOCCHI/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `BetterMountRoulette` | [f04323fa9383](https://github.com/CMDRNuffin/BetterMountRoulette/commit/f04323fa9383d429130aab6abdf7ad5fcea5fbb9)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/BetterMountRoulette/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `BigPlayerDebuffs` | [3c597e008234](https://github.com/rgd87/BigPlayerDebuffs/commit/3c597e008234dff3a2a6a2d6e40085963df04692)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/BigPlayerDebuffs/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `BossMod` | [e563820e90fa](https://github.com/awgil/ffxiv_bossmod/commit/e563820e90fad4b7281eb838e66c2fbe4421cb56)；`api14-cutoff-source-confirmed` | [來源分支](https://github.com/cycleapple/ffxiv_bossmod/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `BossModReborn` | [e563820e90fa](https://github.com/FFXIV-CombatReborn/BossmodReborn/commit/e563820e90fad4b7281eb838e66c2fbe4421cb56)；`api14-cutoff-source-confirmed` | [來源分支](https://github.com/cycleapple/BossmodReborn/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Brio` | [8697df4724d5](https://github.com/Etheirys/Brio/commit/8697df4724d52fdddae78bece4a1c2fa8b2baf78)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Brio/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Cammy` | [42259f106d8e](https://github.com/UnknownX7/Cammy/commit/42259f106d8ef95d7e43d45b4e26e59769be1bdd)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Cammy/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `ChatCoordinates` | [133e69168cbf](https://github.com/kissorjeyabalan/dalamud-chatcoordinates/commit/133e69168cbf89ff0aac1bb8b015a8958f453e27)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/dalamud-chatcoordinates/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `ChatTwo` | [68810e23c16b](https://github.com/Infiziert90/ChatTwo/commit/68810e23c16b135acb84aa60c7501c53dddda696)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/ChatTwo/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `ChilledLeves` | [01bd8f504747](https://github.com/LeontopodiumNivale14/ChilledLeves/commit/01bd8f5047479d2dc703732c2a31e4d6e9c24256)；`api14-head-confirmed` | [來源分支](https://github.com/cycleapple/ChilledLeves/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Craftimizer` | [106f5017f60f](https://github.com/WorkingRobot/Craftimizer/commit/106f5017f60f1798c73f89fdc52f93b3c8c76d57)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Craftimizer/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `CrossUp` | [99a7e8efdcc1](https://github.com/ItsBexy/CrossUp/commit/99a7e8efdcc10be0aa7bf420c7455b84a556631f)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/CrossUp/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `CustomResolution2782` | 未確認獨立 API14 上游；`self-maintained-or-unresolved` | [來源分支](https://github.com/cycleapple/DP-CustomResolution/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `CustomizePlus` | [9fe6ffd04af2](https://github.com/Aether-Tools/CustomizePlus/commit/9fe6ffd04af26542db0f29c7df67606f399dd490)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/CustomizePlus/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `DailyDuty` | [54dbd5daef37](https://github.com/MidoriKami/DailyDuty/commit/54dbd5daef37b1a482fa0446eb342adc7ced8810)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/DailyDuty/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `DeathRecap` | [fbbefcab1e23](https://github.com/Kouzukii/ffxiv-deathrecap/commit/fbbefcab1e237b19be6f6681dfed4c4c1aec3fdc)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/ffxiv-deathrecap/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `DeepDungeonDex` | [2da08dad012a](https://github.com/wolfcomp/MonsterDex/commit/2da08dad012af855d49069200b1de9ccc18f6e53)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/MonsterDex/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Deliveroo` | [521cb52e677d](https://github.com/VeraNala/Deliveroo/commit/521cb52e677df1b0c5d41438a16545e0b5480819)；`api14-head-confirmed` | [來源分支](https://github.com/cycleapple/Deliveroo/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Distance` | [569a41b039eb](https://github.com/PunishedPineapple/Distance/commit/569a41b039ebc0b27432296271030fc50ae80d67)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Distance/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Doorbell` | [81224e03f23e](https://github.com/Aida-Enna/Doorbell/commit/81224e03f23e4a31b7ae1aec3350a28c699cf2ff)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Doorbell/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `DozeAnywhere` | 未確認獨立 API14 上游；`date-candidate-requires-api-evidence` | [來源分支](https://github.com/cycleapple/DozeAnywhere/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `EasyEyes` | [2820a8718267](https://github.com/0ceal0t/EasyEyes/commit/2820a8718267febbf67a323401585dc8a268595e)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/EasyEyes/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `EnemyListDebuffs` | 未確認獨立 API14 上游；`date-candidate-requires-api-evidence` | [來源分支](https://github.com/cycleapple/EnemyListDebuffs/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `EngageTimer` | [1e73f25dda63](https://github.com/xorus/EngageTimer/commit/1e73f25dda631df78569b837d4c5dfe7b192c0ec)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/EngageTimer/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `EnmityHp` | [765bc30fe234](https://github.com/NightmareXIV/EnmityHp/commit/765bc30fe234dec1e5909f07ce23f7c95d423731)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/EnmityHp/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `EurekaTrackerAutoPopper` | [726ed292e2ac](https://github.com/Infiziert90/EurekaTrackerAutoPopper/commit/726ed292e2ac6bdfba7226255d0134c9798eef59)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/EurekaTrackerAutoPopper/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `ExplorersIcebox` | [a1732715e50d](https://github.com/LeontopodiumNivale14/Explorers-Icebox/commit/a1732715e50d3cb30c8af99b19a3b8d74ead579a)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Explorers-Icebox/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `FPSPlugin` | [7304a4534418](https://github.com/Caraxi/FPSPlugin/commit/7304a4534418c7fea4f075d414f034c29101f1d9)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/FPSPlugin/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Facade` | [99084c0689a0](https://github.com/keifufu/Facade/commit/99084c0689a06d6ea8cc54468ee2fa8d597566a6)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Facade/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `FlashOnTell` | [3f8c68cde0f2](https://github.com/reiichi001/Dalamud-FlashOnTellPlugin/commit/3f8c68cde0f26b7734e3000e69e3a9bf56cfb2b7)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Dalamud-FlashOnTellPlugin/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `FlyTextFilter` | [0ed194165256](https://github.com/Aireil/FlyTextFilter/commit/0ed194165256f32a4f773d730a6c2ae5d177d13c)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/FlyTextFilter/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Fungah` | [ff69fa37a228](https://github.com/img02/Fungah-Totally-Safe-Spot/commit/ff69fa37a2286ffa2e6109cd8bc65d6e4c0fe368)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Fungah-Totally-Safe-Spot/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `GatherBuddyReborn` | [6934b9221464](https://github.com/AtmoOmen/GatherBuddyReborn/commit/6934b92214647d89d96e2ed1a55b80b2171f4f25)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/GatherBuddyReborn/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `GatheringPathRenderer` | [e9f684572fdf](https://github.com/PunishXIV/Questionable/commit/e9f684572fdf8ce4f4390f378dab565db8ebf92c)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Questionable/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `GaugeOMatic` | [f34061a9d58d](https://github.com/ItsBexy/GaugeOMatic/commit/f34061a9d58d761fbfafa3fe0877ac51dfdf87ec)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/GaugeOMatic/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Gearsetter` | [19db7afe669e](https://github.com/VeraNala/Gearsetter/commit/19db7afe669e510e6b4fafec2721deb69f244e96)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Gearsetter/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Glamourer` | [0308a4bf6b90](https://github.com/Ottermandias/Glamourer/commit/0308a4bf6b90389ee4c9871f91fc0a03a7f32318)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Glamourer/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `HighFpsPhysicsPlugin` | [eaf7d79d6f57](https://github.com/ItsLunaYup/xivlauncher_physics_plugin/commit/eaf7d79d6f5707c1349dbab3c3918b4a09b64483)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/xivlauncher_physics_plugin/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Honorific` | [78081686085e](https://github.com/Caraxi/Honorific/commit/78081686085e31b150507b2bdd9a8a5e02805e4b)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Honorific/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Housemate` | [889ce7ae6d12](https://github.com/perchbirdd/Housemate/commit/889ce7ae6d12f99b98e808335ed37dfb0d4890fa)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Housemate/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `HuntBuddy` | [baf609914c48](https://github.com/SheepGoMeh/HuntBuddy/commit/baf609914c482dbcfd48262377a6f50cc7ad93c3)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/HuntBuddy/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Hyperborea` | [e6307fe95c32](https://github.com/kawaii/Hyperborea/commit/e6307fe95c32603aa538e7e10fd3566c1435b286)；`api14-manifest-confirmed` | [來源分支](https://github.com/cycleapple/Hyperborea/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `ICE` | [fab3c6062670](https://github.com/LeontopodiumNivale14/Ices-Cosmic-Exploration/commit/fab3c606267088278eeb5344fbe513abce1d5dd8)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Ices-Cosmic-Exploration/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `IINACT` | [7a0ea51f89ac](https://github.com/marzent/IINACT/commit/7a0ea51f89acbde75c8af2e1d721431a32ee190a)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/IINACT/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `InventoryTools` | [2043c0188760](https://github.com/Critical-Impact/InventoryTools/commit/2043c0188760b2e050062cd9c6ffb666a16865da)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/InventoryTools/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `JobBars` | [366cbb79dea8](https://github.com/0ceal0t/JobBars/commit/366cbb79dea8604ada46dcce07943625c1514556)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/JobBars/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Ktisis` | [e97e166ec486](https://github.com/ktisis-tools/Ktisis/commit/e97e166ec486f9c410a96d7a5801bd4f9a555cb9)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Ktisis/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `LMeter` | [32580572cd2c](https://github.com/juicefish/LMeter_TC/commit/32580572cd2c869f1f313123588e5bd0f16ae3c1)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/LMeter_TC/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `LazyLoot` | [6613f821332a](https://github.com/PunishXIV/LazyLoot/commit/6613f821332a8d450841d895a934a257e708f95c)；`api14-head-confirmed` | [來源分支](https://github.com/cycleapple/LazyLoot/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Lifestream` | [d378f2913cee](https://github.com/NightmareXIV/Lifestream/commit/d378f2913cee78bf95c7d6581f5e6eea83c16052)；`api14-manifest-confirmed` | [來源分支](https://github.com/cycleapple/Lifestream/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `LoporritSync` | 未確認獨立 API14 上游；`self-maintained-or-unresolved` | [來源分支](https://github.com/cycleapple/LopClient/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `MapLinker` | [672f8c487b7b](https://github.com/Bluefissure/MapLinker/commit/672f8c487b7b7857a3f92630ac77bab999849d90)；`api14-cutoff-source-confirmed` | [來源分支](https://github.com/cycleapple/MapLinker/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Mappy` | [0265ac3f8f0d](https://github.com/harbingerftw/Mappy/commit/0265ac3f8f0d46119723d9aa56d242b5c9c2c51d)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Mappy/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `MarketBoardPlugin` | [46d3f49fca27](https://github.com/fmauNeko/MarketBoardPlugin/commit/46d3f49fca27c78fb410ba196a3e4feaa28de871)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/MarketBoardPlugin/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Marketbuddy` | [7b2a6a7fa815](https://github.com/PunishXIV/Marketbuddy/commit/7b2a6a7fa815297ae0dd082f4c2c88cd7229c3cb)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Marketbuddy/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `MaskOfKefka` | 未確認獨立 API14 上游；`no-api14-project-history-found` | [來源分支](https://github.com/cycleapple/mask-of-kefka/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `MeterWay` | 未確認獨立 API14 上游；`date-candidate-requires-api-evidence` | [來源分支](https://github.com/cycleapple/MeterWay/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `MidiBard2` | [39adf979ff5c](https://github.com/reckhou/MidiBard2/commit/39adf979ff5c2dd5980b226239a11d5cbd56cbde)；`explicit-api14-branch` | [來源分支](https://github.com/cycleapple/MidiBard2/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `MiniCactpotSolver` | 未確認獨立 API14 上游；`date-candidate-requires-api-evidence` | [來源分支](https://github.com/cycleapple/EzMiniCactpot/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `MissFisher` | [225828c5f5d9](https://github.com/QianChangUwU/MissFisher/commit/225828c5f5d980515d0e025ebcf962ff9a23fc25)；`official-api14-binary-confirmed` | [來源分支](https://github.com/cycleapple/MissFisher/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `MouseLock` | 未確認獨立 API14 上游；`no-api14-project-history-found` | [來源分支](https://github.com/cycleapple/MouseLock/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `MultiHit` | [448c780dad3e](https://github.com/Bluefissure/MultiHit/commit/448c780dad3e407248055f447f8f0fe882512a77)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/MultiHit/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `NOTED` | [51ee34fa9f3c](https://github.com/Tischel/NOTED/commit/51ee34fa9f3c8a73596d69a4d1da2f01ace17fd0)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/NOTED/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Namingway` | 未確認獨立 API14 上游；`date-candidate-requires-api-evidence` | [來源分支](https://github.com/cycleapple/NamingWay/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `NecroLens` | [9e5e34731b83](https://github.com/Jukkales/NecroLens/commit/9e5e34731b831070c967c5236fba27a7b37f4be6)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/NecroLens/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `NoClippy` | [d93eb66bb197](https://github.com/UnknownX7/NoClippy/commit/d93eb66bb197115dbd58876c4cc2a041af3be8c2)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/NoClippy/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `NotificationMaster` | [be830547f3dd](https://github.com/NightmareXIV/NotificationMaster/commit/be830547f3dde05b1d0db8d3050945d78648628c)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/NotificationMaster/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Orbwalker` | [52ce71bba33b](https://github.com/PunishXIV/Orbwalker/commit/52ce71bba33bee1235dbf4536827ca273a3eea62)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Orbwalker/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `PalacePal` | [b3dadf55c51a](https://github.com/PunishXIV/PalacePal/commit/b3dadf55c51afe1b8a6c20cf8d989c4074dcdf35)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/PalacePal/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `PandorasBox` | [814bb212bb13](https://github.com/PunishXIV/PandorasBox/commit/814bb212bb13a93768f2bc8c532ec619f75aa1b1)；`api14-manifest-confirmed` | [來源分支](https://github.com/cycleapple/PandorasBox/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `PartyIcons` | [f595d107d5dd](https://github.com/nebel/xivPartyIcons/commit/f595d107d5ddd1a47c9be613ee45646086e1f31b)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/xivPartyIcons/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `PeepingTom` | 未確認獨立 API14 上游；`date-candidate-requires-api-evidence` | [來源分支](https://github.com/cycleapple/PeepingTom/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `PennyPincher` | [4b0eb9599ee9](https://github.com/tesu/PennyPincher/commit/4b0eb9599ee9a7fa457f0c0da00f030b10abffa8)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/PennyPincher/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Penumbra` | [66bae79d1923](https://github.com/xivdev/Penumbra/commit/66bae79d1923c7077042337781a546c06cef6f9c)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Penumbra/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `PingPlugin` | [e9a7848fd3a8](https://github.com/karashiiro/PingPlugin/commit/e9a7848fd3a803a13d112660acc771c164d50a17)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/PingPlugin/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `PixelPerfect` | [ce246d244013](https://github.com/Haplo064/PixelPerfect/commit/ce246d2440133b624bf1129367e342fa19c28a78)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/PixelPerfect/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `PlayerWatchlist` | 未確認獨立 API14 上游；`self-maintained-or-unresolved` | [來源分支](https://github.com/cycleapple/PlayerWatchlist/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `PocketRecorder` | 未確認獨立 API14 上游；`manual-reference-project-needs-review` | [來源分支](https://github.com/cycleapple/PocketRecorder/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `PriceInsight` | [03de8e2ea3fd](https://github.com/Kouzukii/ffxiv-priceinsight/commit/03de8e2ea3fd4e43530563241bede06a2691b70b)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/ffxiv-priceinsight/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `QoLBar` | [bd6f3c052c0f](https://github.com/UnknownX7/QoLBar/commit/bd6f3c052c0f1fdabc9987804141ecfe065f2dc6)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/QoLBar/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Questionable` | [e9f684572fdf](https://github.com/PunishXIV/Questionable/commit/e9f684572fdf8ce4f4390f378dab565db8ebf92c)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Questionable/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `RadarPlugin` | [3b43eb58776e](https://github.com/KangasZ/RadarPlugin/commit/3b43eb58776e8d8d1a23e2b0c1eee042139f396b)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/RadarPlugin/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Raphael.Dalamud` | [1541b18a9087](https://github.com/Dalamud-DailyRoutines/Raphael.Dalamud/commit/1541b18a9087b7719a8eccfe362b92cdfb189af1)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Raphael.Dalamud/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `ReAction` | [21b475e4abd8](https://github.com/UnknownX7/ReAction/commit/21b475e4abd8cdf221aa20c21e93f9a99491fc7f)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/ReAction/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `ReMakePlacePlugin` | [375cf9dc365d](https://github.com/RemakePlace/plugin/commit/375cf9dc365d10410141d0e5cd09c59aa11d1935)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/ReMakePlacePlugin/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `RezPls` | [4f9004b1a724](https://github.com/Ottermandias/RezPls/commit/4f9004b1a724cf0be268e965a0c260643e55edeb)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/RezPls/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `RotationSolver` | [4f4c029995c7](https://github.com/FFXIV-CombatReborn/RotationSolverReborn/commit/4f4c029995c701e862e3f02f8d0c2b2ef658c4a7)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/RotationSolverReborn/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Saucy` | [6ad3f56a0014](https://github.com/PunishXIV/Saucy/commit/6ad3f56a0014a52bd0e11c2b104e01171dbea569)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Saucy/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `SimpleHeels` | [f74ab6f0950a](https://github.com/Caraxi/SimpleHeels/commit/f74ab6f0950a5fefdca32a77e9cbc8741e0eab81)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/SimpleHeels/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `SimpleTweaksPlugin` | [b3cdea11a4b2](https://github.com/Caraxi/SimpleTweaksPlugin/commit/b3cdea11a4b26d56b101be05997ea8c1b44b44e7)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/SimpleTweaksPlugin/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Skippy` | [e8bc94e165f6](https://github.com/BoxuChan/Skippy/commit/e8bc94e165f6360d6bb4ea0d34bdb07e49104329)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Skippy/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `SomethingNeedDoing` | [f1eeb19b2ada](https://github.com/Jaksuhn/SomethingNeedDoing/commit/f1eeb19b2adabd7c7546e8bda532ecf9c7dc9513)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/SomethingNeedDoing/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `SonarPlugin` | [5af03cf3788b](https://github.com/FFXIV-Sonar/SonarDistrib/commit/5af03cf3788b2a817132c4658cdcbd7cd8e8d125)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/SonarDistrib/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `SortaKinda` | [d2e99fde7fd4](https://github.com/MidoriKami/SortaKinda/commit/d2e99fde7fd4a101ecb7e6372fd26c8dd5fe43b6)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/SortaKinda/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Splatoon` | [98e1a26d977b](https://github.com/PunishXIV/Splatoon/commit/98e1a26d977bd0d52faec215c53d3ff69c569135)；`api14-manifest-confirmed` | [來源分支](https://github.com/cycleapple/Splatoon/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `SubmarineTracker` | [0109da941009](https://github.com/Infiziert90/SubmarineTracker/commit/0109da941009c7280d1aa0e3fcecf8ddcc7dfe54)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/SubmarineTracker/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `TeleporterPlugin` | [427d431d8544](https://github.com/pohky/TeleporterPlugin/commit/427d431d8544870721b8b5f8c9be3f4d734cac7a)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/TeleporterPlugin/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `TextAdvance` | [2c18efea9223](https://github.com/NightmareXIV/TextAdvance/commit/2c18efea92233c5a0e70b751219b015a91c5d74e)；`api14-manifest-confirmed` | [來源分支](https://github.com/cycleapple/TextAdvance/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `TitleEdit` | [ebe574ceb676](https://github.com/RokasKil/TitleEdit/commit/ebe574ceb676438e66596db6a7fe49d2e19dcdaf)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/TitleEdit/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `TriadBuddy` | [0734c65abb26](https://github.com/MgAl2O4/FFTriadBuddyDalamud/commit/0734c65abb2662b5a2aa010b8eb396dc60e55964)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/FFTriadBuddyDalamud/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Umbra` | [f19f0208a3bd](https://github.com/una-xiv/umbra/commit/f19f0208a3bd46c9869119b353498f6a1f546b3e)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/umbra/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `VFXEditor` | [ff7ccc43a4b2](https://github.com/0ceal0t/Dalamud-VFXEditor/commit/ff7ccc43a4b2bf12dd07e10f5a957a484f2583b0)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/Dalamud-VFXEditor-API13/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `Visibility` | [6fa9126183b1](https://github.com/SheepGoMeh/VisibilityPlugin/commit/6fa9126183b1b59bd528f41c0da688ca7bbc3f3e)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/VisibilityPlugin/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `WaymarkPresetPlugin` | 未確認獨立 API14 上游；`date-candidate-requires-api-evidence` | [來源分支](https://github.com/cycleapple/WaymarkPresetPlugin/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `WrathCombo` | [bf5d4eb93b10](https://github.com/PunishXIV/WrathCombo/commit/bf5d4eb93b10196a5aa92bfc86411f9bb4a45646)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/WrathCombo/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `XivTreasureParty` | 未確認獨立 API14 上游；`self-maintained-or-unresolved` | [來源分支](https://github.com/cycleapple/xiv-party-treasure-helper/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `YesAlready` | [35c21fec2e15](https://github.com/PunishXIV/YesAlready/commit/35c21fec2e155d6aaca3815285b2675167e56f89)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/YesAlready/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `ZodiacBuddy` | [1f46fb6281aa](https://github.com/foophoof/ZodiacBuddy/commit/1f46fb6281aaed4f9ad1d65697bb25f13283694f)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/ZodiacBuddy/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `orchestrion` | [314c0a610712](https://github.com/perchbirdd/OrchestrionPlugin/commit/314c0a61071233f9ce93b507f0a9d9e5446147dc)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/OrchestrionPlugin/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `vfaux` | [1a2b76f9ccdc](https://github.com/awgil/vfaux/commit/1a2b76f9ccdc147605f37accb0e32424cb553129)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/vfaux/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `visland` | [c5b705dd6d3e](https://github.com/awgil/ffxiv_visland/commit/c5b705dd6d3e5058273bc3d5c7b6828c37773005)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/ffxiv_visland/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
| `vnavmesh` | [a49e52fc8439](https://github.com/awgil/ffxiv_navmesh/commit/a49e52fc84390cfecfd633e181653c7641110c0a)；`last-api14-before-project-upgrade` | [來源分支](https://github.com/cycleapple/ffxiv_navmesh/tree/api14-tw)；建置／官方 DLL 通過，台服待驗證 |
