
---

## 🧠 第二階段：模組解耦與邏輯抽出

### 🎮 控制器（Controllers）模組抽出

| 新模組 | 來源檔案 | 功能說明 |
|--------|----------|----------|
| `ModelTrainingController` | `ui/training_page.py` | 封裝 agent 訓練、驗證、儲存流程 |
| `StrategyAdvisor`         | `ui/ai_control.py`     | 將 Q 表、熵值轉成下注建議邏輯 |

---

### 📦 `data_facade.py` 重構拆分提案

| 新模組 | 原始功能 | 備註 |
|--------|----------|------|
| `game_log_loader.py` | 載入並轉換 log 成 DataFrame | 讀取與格式處理 |
| `state_feature_builder.py` | 建立 `(diff, rolling_sum_5)` 狀態特徵 | 特徵工程 |
| `q_table_manager.py` | 儲存、讀取、查詢 Q 表 | Q-learning 模組專用 |

---

## 🔬 第三階段：強化測試與替換性

- 為每個核心模組設計 interface，讓日後可替換：
  - Q-learning → PPO、SafeQ
  - 資料來源 → 模擬器 or 真實 log
- 建立 `tests/` 目錄下對應測試檔案

---

## ✅ 總結與進度追蹤

| 項目 | 狀態 | 備註 |
|------|------|------|
| 目錄結構重整 | 🔄 進行中 | 重構分支：`refactor/structure-cleanup` |
| `ModelTrainingController` | ⏳ 準備撰寫 | 預計下一步 |
| `data_facade` 拆分 | ⏳ 規劃中 | 將逐步模組化 |
| 文件整合 | ✅ README + docs 正在同步中 |

---

📌 後續所有變更將逐步記錄於此文件，請搭配 `README.md` 一同查看。

