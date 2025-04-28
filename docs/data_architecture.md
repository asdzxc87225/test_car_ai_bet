# Data 層設計說明：DataFacade 與 Session

---

## 1. 目標
為了確保專案資料管理的**一致性**、**效能最佳化**與**擴充彈性**，  
本專案採用兩層資料管理架構：

- `DataFacade`：負責原始資料的磁碟存取與快取管理
- `Session`：負責運行時期的資料副本快取與一致性控制

---

## 2. DataFacade 的角色
**DataFacade** 是資料的**磁碟入口**，主要負責：

- 讀取 `game_log.csv`、`q_table.pkl`
- 進行基本的磁碟快取（第一次讀取後快取於記憶體）
- 提供資料更新（如 `append_game_log()`）

✅ **不做資料加工（特徵處理）**  
✅ **只負責讀取、寫入磁碟上的原始資料**

---

## 3. Session 的角色
**Session** 是資料的**記憶體快取中心**，主要負責：

- 管理運行中的資料副本
- 快速提供 UI、AI、分析模組即時資料
- 控制資料一致性（透過 `get()` 和 `refresh()` 操作）

✅ **不直接修改原始資料**  
✅ **不做資料處理（僅快取原始版本）**

---

## 4. DataFacade 與 Session 的差異比較

| 功能面向 | DataFacade | Session |
|:---------|:-----------|:--------|
| 資料來源 | 磁碟（CSV、Pickle） | 記憶體（副本） |
| 管理方式 | 檔案 I/O | 快取控制 |
| 資料型態 | 原始資料 | 副本資料 |
| 資料加工 | ❌ 無 | ❌ 無（加工在模組內做） |
| 快取更新 | 讀檔時自動快取 | 手動 `refresh(key)` |
| 使用場景 | 初次讀取資料、追加資料 | 頻繁存取資料、訓練、分析 |

---

## 5. 數據處理與特徵工程規範

未來所有數據處理、特徵工程必須遵守以下原則：

1. **取得資料**
    - 使用 `Session.get("game_log")` / `Session.get("q_table")` 拿取副本資料
    - 禁止直接操作 DataFacade 或直接讀磁碟

2. **資料處理（如特徵加工）**
    - 必須在模組內或 `FeatureBuilder` 工具內處理
    - 禁止直接修改 Session 內的資料（Session資料應保持只讀）

3. **新增資料**
    - 透過 `DataFacade.append_game_log(new_entry)` 新增下注資料
    - 新增後，必須呼叫 `Session.refresh("game_log")` 更新快取

4. **特徵常駐需求（可擴充）**
    - 如需常駐特徵（如熵值、風險等特徵），可考慮在 Session 增設新 key（如 `"features"`）

5. **未來資料結構演進**
    - `game_log` 仍使用 DataFrame
    - `q_table` 統一採用 dict of dict 結構，靈活支援未來更複雜狀態與動作空間

---

## 6. 附註
- Session 設計目標是確保整個系統資料流**乾淨、一致、可控**。
- 所有高層模組（下注、分析、AI 控制）只能依賴 Session，不能越級存取 DataFacade。
- 未來若擴充至 fuzzy decision、模擬器、自動化訓練，仍可以平滑延伸此資料流架構。

---

# 🚀 未來擴充方向
- 支援更多資料類型，如：fuzzy 規則庫（fuzzy_rules）、訓練歷史（training_log）
- 資料持久化（如 Parquet, SQLite）
- 訓練流程自動化（AutoTrainer 結合 Session 快取）

---

