# Data Center 2.0 說明文件

---

## 🌟 系統目標

Data Center 2.0 統一管理跎車下注系統的基礎資料與特徵處理，
確保資料存取一致、快取效能最佳化，並支援後續推論與訓練流程。

**管理範圍：**
- 跎車歷史資料（`game_log.csv`）
- Q-learning 模型（`q_table.pkl`）
- 特徵工程（如 `diff`, `rolling_sum_5`, `wine_type`）
- 資料快取與更新控制

---

## 📂 模組結構

| 模組/檔案 | 功能說明 |
|:---|:---|
| `data_facade.py` | 磁碟存取、資料快取、資料增加 |
| `feature_builder.py` | 提供特徵欄位建構工具 |
| `data_errors.py` | 資料層錯誤定義 |
| `global_data.py` | Session 快取管理層 |

---

## ⚙️ DataFacade 功能

| 方法 | 說明 |
|:---|:---|
| `game_log()` | 讀取 game_log，快取管理 |
| `q_table(model_name)` | 讀取指定模型的 Q-table |
| `list_models()` | 列出 models 資料夾的所有模型 |
| `append_game_log(new_entry)` | 增加新下注資料 |
| `build_features(df)` | 對外提供特徵建構 |
| `refresh_cache(key)` | 清除單一快取 |
| `clear_all_cache()` | 清空全部快取 |
| `register_on_data_updated(callback)` | 註冊資料更新通知 |
| `_notify_data_updated()` | 呼叫資料更新通知 |

---

## 🧐 資料流設計（推論與訓練）

---

### 📈 推論（Predict）資料流範例

從最新 game_log 預測下一次行動：

```python
from data.global_data import Session
from data.feature_builder import FeatureBuilder

# 取得最新資料
game_log = Session.get("game_log")
features = FeatureBuilder.build_features(game_log)

# 取最新一筆特徵
last_row = features.iloc[-1]
diff = last_row["diff"]
rolling_sum_5 = last_row["rolling_sum_5"]

# 拿取 Q 表
q_table = Session.get("q_table")
state = (diff, rolling_sum_5)

# 預測動作
if state in q_table:
    action_values = q_table[state]
    action = max(action_values, key=action_values.get)
else:
    action = "押小車"

print(f"建議動作：{action}")
```

---

### 🌟 訓練（Train）資料流範例

從全體 game_log 訓練新的 Q-learning 模型：

```python
from data.global_data import Session
from data.feature_builder import FeatureBuilder
from agent.trainer import QLearner

# 取得訓練資料
game_log = Session.get("game_log")
features = FeatureBuilder.build_features(game_log)

# 組裝訓練資料
training_data = []

for idx in range(len(features) - 1):
    current = features.iloc[idx]
    next_row = features.iloc[idx + 1]

    state = (current["diff"], current["rolling_sum_5"])
    action = ...      # 根據下注紀錄推方
    reward = ...      # 根據勝負結果計算
    next_state = (next_row["diff"], next_row["rolling_sum_5"])

    training_data.append((state, action, reward, next_state))

# 訓練模型
qlearner = QLearner()

for state, action, reward, next_state in training_data:
    qlearner.learn(state, action, reward, next_state)

# 儲存新模型
qlearner.save("./data/models/q_model_0501.pkl")
```

---

## 📚 數據處理規範

- 資料取用：統一使用 `Session.get("game_log")`, `Session.get("q_table")`
- 特徵處理：不直接修改 Session，在本地轉換
- 資料增加：使用 `append_game_log()`，並手動 `Session.refresh()`
- 特徵常駐：有需要時可在 Session 內增加特徵 cache

---

## 🛡️ 例外錯誤處理

| 錯誤類別 | 說明 |
|:---|:---|
| `DataLoadError` | 讀取檔案失敗或資料錯誤時抽出 |
| `DataFormatError` | 必要欄位缺失或資料結構不符時抽出 |

---

## 🚀 未來擴充方向

- 支援 fuzzy 觀測特徵（`fuzzy_rules`）
- 增加 state 風險層級（`state_risk_level`）
- 資料快取自動失效與 refresh 機制
- 模型訓練自動化（AutoTrainer）

---


