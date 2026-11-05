# API14 移植進度

2026-11-06：125 個插件已納入 API14 預備移植及實質複查；132 個遠端分支與本機提交一致。

124 個開源插件建置通過（PocketRecorder 含 Windows CI 原生 C++）；MissFisher 完成官方 API14 套件繁中移植與驗證打包。

125 個主 DLL 皆參照 API14／.NET 10；868 個受檢受控輸出未發現非 API14 的 Dalamud 參照。六個共用依賴建置通過。

**全部仍待台服 API14 實機驗證；目前發布清單為空。** 其中 15 個插件尚無獨立確認的 API14 上游版本，見 [完整複查與例外](UPSTREAM_REVIEW.md)。

| 插件 | API13 起點 | API14 來源分支 | 進度 |
|---|---|---|---|
| Action Timeline Replacement (`ActionTimelineReplacement`) | 1.0.0.1 | [cycleapple/ActionTimelineReplacement](https://github.com/cycleapple/ActionTimelineReplacement/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Aetherment (`Aetherment`) | 0.4.0.0 | [cycleapple/aetherment](https://github.com/cycleapple/aetherment/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Allagan Item Search (`AllaganItemSearch`) | 1.0.0.4 | [cycleapple/AllaganItemSearch](https://github.com/cycleapple/AllaganItemSearch/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Allagan Market (`AllaganMarket`) | 1.2.0.9 | [cycleapple/AllaganMarket](https://github.com/cycleapple/AllaganMarket/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| AntiAfkKick (`AntiAfkKick-Dalamud`) | 2.1.0.10 | [cycleapple/AntiAfkKick](https://github.com/cycleapple/AntiAfkKick/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Artisan (`Artisan`) | 4.0.4.26 | [cycleapple/Artisan](https://github.com/cycleapple/Artisan/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| AutoDuty (`AutoDuty`) | 0.0.0.9 | [cycleapple/AutoDuty](https://github.com/cycleapple/AutoDuty/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| AutoHook (`AutoHook`) | 5.0.0.15 | [cycleapple/AutoHook](https://github.com/cycleapple/AutoHook/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| AutoMinion (`AutoMinion`) | 1.0.0.2 | [cycleapple/AutoMinion](https://github.com/cycleapple/AutoMinion/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| AutoRetainer (`AutoRetainer`) | 4.5.1.30 | [cycleapple/AutoRetainer](https://github.com/cycleapple/AutoRetainer/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| CBT (`Automaton`) | 69.103.0.1 | [cycleapple/ffxiv-bundleoftweaks](https://github.com/cycleapple/ffxiv-bundleoftweaks/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Avarice (`Avarice`) | 2.1.1.8 | [cycleapple/Avarice](https://github.com/cycleapple/Avarice/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Burning Down the House (`BDTHPlugin`) | 1.7.1.2 | [cycleapple/BDTHPlugin](https://github.com/cycleapple/BDTHPlugin/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| BOCCHI 新月島助手 (`BOCCHI`) | 1.0.1.2 | [cycleapple/BOCCHI](https://github.com/cycleapple/BOCCHI/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Better Mount Roulette (`BetterMountRoulette`) | 1.0.0.2 | [cycleapple/BetterMountRoulette](https://github.com/cycleapple/BetterMountRoulette/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| BigPlayerDebuffs (`BigPlayerDebuffs`) | 1.1.0.14 | [cycleapple/BigPlayerDebuffs](https://github.com/cycleapple/BigPlayerDebuffs/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Boss Mod (`BossMod`) | 0.1.4.3 | [cycleapple/ffxiv_bossmod](https://github.com/cycleapple/ffxiv_bossmod/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Bossmod Reborn (`BossModReborn`) | 7.3.8.8 | [cycleapple/BossmodReborn](https://github.com/cycleapple/BossmodReborn/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Brio (`Brio`) | 0.5.2.3 | [cycleapple/Brio](https://github.com/cycleapple/Brio/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Cammy (`Cammy`) | 2.1.0.14 | [cycleapple/Cammy](https://github.com/cycleapple/Cammy/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| ChatCoordinates (`ChatCoordinates`) | 2.1.2.10 | [cycleapple/dalamud-chatcoordinates](https://github.com/cycleapple/dalamud-chatcoordinates/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Chat 2 (`ChatTwo`) | 1.32.0.3 | [cycleapple/ChatTwo](https://github.com/cycleapple/ChatTwo/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Chilled Leves (`ChilledLeves`) | 1.0.1.22 | [cycleapple/ChilledLeves](https://github.com/cycleapple/ChilledLeves/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Craftimizer (`Craftimizer`) | 2.8.0.2 | [cycleapple/Craftimizer](https://github.com/cycleapple/Craftimizer/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| CrossUp (`CrossUp`) | 1.7.1.14 | [cycleapple/CrossUp](https://github.com/cycleapple/CrossUp/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| CustomResolution (`CustomResolution2782`) | 1.0.1.0 | [cycleapple/DP-CustomResolution](https://github.com/cycleapple/DP-CustomResolution/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Customize+ (`CustomizePlus`) | 2.0.7.31 | [cycleapple/CustomizePlus](https://github.com/cycleapple/CustomizePlus/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| DailyDuty (`DailyDuty`) | 5.3.2.14 | [cycleapple/DailyDuty](https://github.com/cycleapple/DailyDuty/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Death Recap (`DeathRecap`) | 1.13.2.3 | [cycleapple/ffxiv-deathrecap](https://github.com/cycleapple/ffxiv-deathrecap/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| MonsterDex (`DeepDungeonDex`) | 2.13.6.2 | [cycleapple/MonsterDex](https://github.com/cycleapple/MonsterDex/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Deliveroo (`Deliveroo`) | 7.4.0.1 | [cycleapple/Deliveroo](https://github.com/cycleapple/Deliveroo/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Distance (`Distance`) | 1.1.3.6 | [cycleapple/Distance](https://github.com/cycleapple/Distance/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Doorbell (`Doorbell`) | 1.0.4.1 | [cycleapple/Doorbell](https://github.com/cycleapple/Doorbell/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| DozeAnywhere (`DozeAnywhere`) | 13.1.0.1 | [cycleapple/DozeAnywhere](https://github.com/cycleapple/DozeAnywhere/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| EasyEyes (`EasyEyes`) | 1.3.1.1 | [cycleapple/EasyEyes](https://github.com/cycleapple/EasyEyes/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| EnemyListDebuffs (`EnemyListDebuffs`) | 1.13.0.0 | [cycleapple/EnemyListDebuffs](https://github.com/cycleapple/EnemyListDebuffs/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| EngageTimer (`EngageTimer`) | 2.4.4.1 | [cycleapple/EngageTimer](https://github.com/cycleapple/EngageTimer/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| EnemyListHP (`EnmityHp`) | 2.0.1.8 | [cycleapple/EnmityHp](https://github.com/cycleapple/EnmityHp/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Eureka Linker (`EurekaTrackerAutoPopper`) | 1.5.9.5 | [cycleapple/EurekaTrackerAutoPopper](https://github.com/cycleapple/EurekaTrackerAutoPopper/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Explorer's Icebox (`ExplorersIcebox`) | 1.0.4.6 | [cycleapple/Explorers-Icebox](https://github.com/cycleapple/Explorers-Icebox/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| FPS Plugin (`FPSPlugin`) | 1.7.0.5 | [cycleapple/FPSPlugin](https://github.com/cycleapple/FPSPlugin/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Facade (`Facade`) | 1.0.0.3 | [cycleapple/Facade](https://github.com/cycleapple/Facade/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| FlashOnTell (`FlashOnTell`) | 0.0.9.0 | [cycleapple/Dalamud-FlashOnTellPlugin](https://github.com/cycleapple/Dalamud-FlashOnTellPlugin/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| FlyTextFilter (`FlyTextFilter`) | 4.4.0.3 | [cycleapple/FlyTextFilter](https://github.com/cycleapple/FlyTextFilter/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Fungah (`Fungah`) | 1.0.0.7 | [cycleapple/Fungah-Totally-Safe-Spot](https://github.com/cycleapple/Fungah-Totally-Safe-Spot/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| GatherBuddy Reborn (`GatherBuddyReborn`) | 7.3.5.7 | [cycleapple/GatherBuddyReborn](https://github.com/cycleapple/GatherBuddyReborn/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| GatheringPathRenderer (`GatheringPathRenderer`) | 0.10.0.1 | [cycleapple/Questionable](https://github.com/cycleapple/Questionable/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Gauge-O-Matic (`GaugeOMatic`) | 0.8.2.3 | [cycleapple/GaugeOMatic](https://github.com/cycleapple/GaugeOMatic/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Gearsetter (`Gearsetter`) | 4.0.0.1 | [cycleapple/Gearsetter](https://github.com/cycleapple/Gearsetter/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Glamourer (`Glamourer`) | 1.5.0.16 | [cycleapple/Glamourer](https://github.com/cycleapple/Glamourer/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| High FPS Physics Fix (`HighFpsPhysicsPlugin`) | 8.3.0.1 | [cycleapple/xivlauncher_physics_plugin](https://github.com/cycleapple/xivlauncher_physics_plugin/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Honorific (`Honorific`) | 1.7.1.3 | [cycleapple/Honorific](https://github.com/cycleapple/Honorific/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Housemate (`Housemate`) | 1.0.3.4 | [cycleapple/Housemate](https://github.com/cycleapple/Housemate/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Hunt Buddy (`HuntBuddy`) | 1.2.2.0 | [cycleapple/HuntBuddy](https://github.com/cycleapple/HuntBuddy/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Hyperborea (`Hyperborea`) | 1.0.0.33 | [cycleapple/Hyperborea](https://github.com/cycleapple/Hyperborea/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Ice's Cosmic Exploration (`ICE`) | 0.0.73.52 | [cycleapple/Ices-Cosmic-Exploration](https://github.com/cycleapple/Ices-Cosmic-Exploration/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| IINACT (`IINACT`) | 1.13.9.7 | [cycleapple/IINACT](https://github.com/cycleapple/IINACT/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Allagan Tools (`InventoryTools`) | 1.13.1.14 | [cycleapple/InventoryTools](https://github.com/cycleapple/InventoryTools/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| JobBars (`JobBars`) | 1.3.2.3 | [cycleapple/JobBars](https://github.com/cycleapple/JobBars/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Ktisis v0.3 (`Ktisis`) | 0.3.14.5 | [cycleapple/Ktisis](https://github.com/cycleapple/Ktisis/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| LMeter (`LMeter`) | 1.13.0.3 | [cycleapple/LMeter_TC](https://github.com/cycleapple/LMeter_TC/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| LazyLoot (`LazyLoot`) | 5.3.2.5 | [cycleapple/LazyLoot](https://github.com/cycleapple/LazyLoot/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Lifestream (`Lifestream`) | 2.5.3.9 | [cycleapple/Lifestream](https://github.com/cycleapple/Lifestream/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Loporrit Sync (`LoporritSync`) | 1.0.9.2 | [cycleapple/LopClient](https://github.com/cycleapple/LopClient/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| MapLinker (`MapLinker`) | 1.1.11.2 | [cycleapple/MapLinker](https://github.com/cycleapple/MapLinker/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Mappy (`Mappy`) | 3.1.6.12 | [cycleapple/Mappy](https://github.com/cycleapple/Mappy/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Market board (`MarketBoardPlugin`) | 1.11.0.0 | [cycleapple/MarketBoardPlugin](https://github.com/cycleapple/MarketBoardPlugin/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Marketbuddy (`Marketbuddy`) | 0.2.4.1 | [cycleapple/Marketbuddy](https://github.com/cycleapple/Marketbuddy/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Mask of Kefka (`MaskOfKefka`) | 0.2.0.1 | [cycleapple/mask-of-kefka](https://github.com/cycleapple/mask-of-kefka/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| MeterWay (`MeterWay`) | 1.0.17.2 | [cycleapple/MeterWay](https://github.com/cycleapple/MeterWay/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| MidiBard 2 (`MidiBard2`) | 3.2.1.3 | [cycleapple/MidiBard2](https://github.com/cycleapple/MidiBard2/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| ezMiniCactpot (`MiniCactpotSolver`) | 3.0.0.4 | [cycleapple/EzMiniCactpot](https://github.com/cycleapple/EzMiniCactpot/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| MissFisher (`MissFisher`) | 1.6.5.13 | [cycleapple/MissFisher](https://github.com/cycleapple/MissFisher/tree/api14-tw) | 官方 API14 繁中移植／打包通過；台服待驗證 |
| MouseLock (`MouseLock`) | 1.0.0.5 | [cycleapple/MouseLock](https://github.com/cycleapple/MouseLock/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| MultiHit (`MultiHit`) | 0.0.4.1 | [cycleapple/MultiHit](https://github.com/cycleapple/MultiHit/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| NOTED (`NOTED`) | 1.6.0.0 | [cycleapple/NOTED](https://github.com/cycleapple/NOTED/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Namingway (`Namingway`) | 1.1.17.1 | [cycleapple/NamingWay](https://github.com/cycleapple/NamingWay/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| NecroLens (`NecroLens`) | 1.0.8.13 | [cycleapple/NecroLens](https://github.com/cycleapple/NecroLens/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| NoClippy (`NoClippy`) | 0.5.0.20 | [cycleapple/NoClippy](https://github.com/cycleapple/NoClippy/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| NotificationMaster (`NotificationMaster`) | 2.1.1.13 | [cycleapple/NotificationMaster](https://github.com/cycleapple/NotificationMaster/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Orbwalker (`Orbwalker`) | 1.0.1.7 | [cycleapple/Orbwalker](https://github.com/cycleapple/Orbwalker/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Palace Pal (`PalacePal`) | 4.14.0.3 | [cycleapple/PalacePal](https://github.com/cycleapple/PalacePal/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Pandora's Box (`PandorasBox`) | 1.6.3.19 | [cycleapple/PandorasBox](https://github.com/cycleapple/PandorasBox/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Party Icons (`PartyIcons`) | 1.2.3.3 | [cycleapple/xivPartyIcons](https://github.com/cycleapple/xivPartyIcons/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Peeping Tom (`PeepingTom`) | 1.7.13.1 | [cycleapple/PeepingTom](https://github.com/cycleapple/PeepingTom/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Penny Pincher (`PennyPincher`) | 1.8.0.6 | [cycleapple/PennyPincher](https://github.com/cycleapple/PennyPincher/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Penumbra (`Penumbra`) | 1.5.1.26 | [cycleapple/Penumbra](https://github.com/cycleapple/Penumbra/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| PingPlugin (`PingPlugin`) | 2.9.0.2 | [cycleapple/PingPlugin](https://github.com/cycleapple/PingPlugin/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Pixel Perfect (`PixelPerfect`) | 3.3.2.1 | [cycleapple/PixelPerfect](https://github.com/cycleapple/PixelPerfect/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| PlayerWatchlist (`PlayerWatchlist`) | 1.0.0.1 | [cycleapple/PlayerWatchlist](https://github.com/cycleapple/PlayerWatchlist/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Pocket Recorder（繁體中文） (`PocketRecorder`) | 1.0.5.23 | [cycleapple/PocketRecorder](https://github.com/cycleapple/PocketRecorder/tree/api14-tw) | Windows C#／原生 CI 通過；台服待驗證 |
| Price Insight (`PriceInsight`) | 2.11.3.5 | [cycleapple/ffxiv-priceinsight](https://github.com/cycleapple/ffxiv-priceinsight/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| QoL Bar (`QoLBar`) | 2.3.3.8 | [cycleapple/QoLBar](https://github.com/cycleapple/QoLBar/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Questionable (`Questionable`) | 13.68.129.8 | [cycleapple/Questionable](https://github.com/cycleapple/Questionable/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Radar Plugin (`RadarPlugin`) | 2.1.8.3 | [cycleapple/RadarPlugin](https://github.com/cycleapple/RadarPlugin/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Raphael.Dalamud (`Raphael.Dalamud`) | 0.0.5.1 | [cycleapple/Raphael.Dalamud](https://github.com/cycleapple/Raphael.Dalamud/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| ReAction (`ReAction`) | 1.3.4.4 | [cycleapple/ReAction](https://github.com/cycleapple/ReAction/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| ReMakePlace Plugin (`ReMakePlacePlugin`) | 7.3.4.0 | [cycleapple/ReMakePlacePlugin](https://github.com/cycleapple/ReMakePlacePlugin/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| RezPls (`RezPls`) | 1.5.2.3 | [cycleapple/RezPls](https://github.com/cycleapple/RezPls/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Rotation Solver Reborn (`RotationSolver`) | 7.3.5.4 | [cycleapple/RotationSolverReborn](https://github.com/cycleapple/RotationSolverReborn/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Saucy (`Saucy`) | 1.4.2.9 | [cycleapple/Saucy](https://github.com/cycleapple/Saucy/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Simple Heels (`SimpleHeels`) | 0.10.7.5 | [cycleapple/SimpleHeels](https://github.com/cycleapple/SimpleHeels/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Simple Tweaks (`SimpleTweaksPlugin`) | 1.10.11.2 | [cycleapple/SimpleTweaksPlugin](https://github.com/cycleapple/SimpleTweaksPlugin/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Skippy (`Skippy`) | 1.2.2.9 | [cycleapple/Skippy](https://github.com/cycleapple/Skippy/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Something Need Doing (`SomethingNeedDoing`) | 0.0.0.1 | [cycleapple/SomethingNeedDoing](https://github.com/cycleapple/SomethingNeedDoing/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Sonar (`SonarPlugin`) | 0.7.4.4 | [cycleapple/SonarDistrib](https://github.com/cycleapple/SonarDistrib/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| SortaKinda (`SortaKinda`) | 2.1.1.8 | [cycleapple/SortaKinda](https://github.com/cycleapple/SortaKinda/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Splatoon (`Splatoon`) | 3.8.2.5 | [cycleapple/Splatoon](https://github.com/cycleapple/Splatoon/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Submarine Tracker (`SubmarineTracker`) | 2.0.2.2 | [cycleapple/SubmarineTracker](https://github.com/cycleapple/SubmarineTracker/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Teleporter (`TeleporterPlugin`) | 2.0.2.11 | [cycleapple/TeleporterPlugin](https://github.com/cycleapple/TeleporterPlugin/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| TextAdvance (`TextAdvance`) | 3.2.4.8 | [cycleapple/TextAdvance](https://github.com/cycleapple/TextAdvance/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Title Edit (`TitleEdit`) | 3.0.6.22 | [cycleapple/TitleEdit](https://github.com/cycleapple/TitleEdit/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| TriadBuddy (`TriadBuddy`) | 1.13.0.2 | [cycleapple/FFTriadBuddyDalamud](https://github.com/cycleapple/FFTriadBuddyDalamud/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Umbra XIV (`Umbra`) | 3.1.7.1 | [cycleapple/umbra](https://github.com/cycleapple/umbra/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| VFXEditor（繁體中文） (`VFXEditor`) | 1.9.2.10 | [cycleapple/Dalamud-VFXEditor-API13](https://github.com/cycleapple/Dalamud-VFXEditor-API13/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Visibility (`Visibility`) | 1.1.9.2 | [cycleapple/VisibilityPlugin](https://github.com/cycleapple/VisibilityPlugin/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Waymark Preset Plugin (`WaymarkPresetPlugin`) | 1.5.5.0 | [cycleapple/WaymarkPresetPlugin](https://github.com/cycleapple/WaymarkPresetPlugin/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Wrath Combo (`WrathCombo`) | 1.0.1.25 | [cycleapple/WrathCombo](https://github.com/cycleapple/WrathCombo/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| XIV 藏寶圖工具小幫手 (`XivTreasureParty`) | 0.1.9.4 | [cycleapple/xiv-party-treasure-helper](https://github.com/cycleapple/xiv-party-treasure-helper/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| YesAlready (`YesAlready`) | 0.0.0.1 | [cycleapple/YesAlready](https://github.com/cycleapple/YesAlready/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| ZodiacBuddy (`ZodiacBuddy`) | 1.13.0.2 | [cycleapple/ZodiacBuddy](https://github.com/cycleapple/ZodiacBuddy/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Orchestrion Plugin (`orchestrion`) | 2.2.0.13 | [cycleapple/OrchestrionPlugin](https://github.com/cycleapple/OrchestrionPlugin/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Easier Faux Hollows (`vfaux`) | 0.0.0.11 | [cycleapple/vfaux](https://github.com/cycleapple/vfaux/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| Visland (`visland`) | 0.0.0.139 | [cycleapple/ffxiv_visland](https://github.com/cycleapple/ffxiv_visland/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
| vnavmesh (`vnavmesh`) | 1.1.2.5 | [cycleapple/ffxiv_navmesh](https://github.com/cycleapple/ffxiv_navmesh/tree/api14-tw) | API14 SDK 建置通過；台服待驗證 |
