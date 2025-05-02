# Data Center 2.0 說明文件

---

## 🎯 系統目標

本資料中心（Data Center 2.0）負責統一管理賽車下注系統中的所有基礎資料，
包括：

- 賽事歷史資料 (game_log.csv)
- Q-learning 模型權重 (q_table.pkl)
- 特徵工程 (Feature Engineering) 處理
- 資料快取管理
- 資料更新通知 (Signal)

以支援下注策略模組、AI預測模組與前端UI互動模組。

---

## 📂 模組結構

| 檔案/模組 | 功能說明 |
|:---|:---|
| `data_facade.py` | 資料讀取、特徵建構、資料追加、資料刷新 |
| `feature_builder.py` | 負責從 game_log 建構特徵資料（如 diff, rolling_sum_5, wine_type） |
| `data_errors.py` | 定義資料中心相關的自定義錯誤類別 (DataLoadError, DataFormatError) |

---

## ⚙️ 功能說明

### DataFacade 類別

| 方法 | 說明 |
|:---|:---|
| `reload()` | 重新讀取 game_log、q_table 並重建特徵資料，並觸發資料更新通知 |
| `append_game_log(new_entry: dict, auto_reload=True)` | 追加一筆新下注資料到 game_log.csv，可選擇是否立即刷新資料 |
| `get_game_log()` | 取得 game_log 的副本 |
| `get_features()` | 取得特徵資料的副本 |
| `get_q_table()` | 取得 q_table 的副本（DataFrame或dict） |
| `register_on_data_updated(callback)` | 註冊資料更新完成時要呼叫的外部函數 |
| `_notify_data_updated()` | 資料更新完成後，觸發所有註冊的 callback |

---

## ⚡ 例外錯誤處理（Exception Handling）

使用自定義錯誤類別：

| 錯誤類別 | 使用場景 |
|:---|:---|
| `DataCenterError` | 資料中心錯誤的基礎類別 |
| `DataLoadError` | 讀取資料（如 game_log, q_table）失敗時拋出 |
| `DataFormatError` | 資料欄位不完整、格式錯誤時拋出 |

所有異常狀況會統一拋出上述錯誤類型，  
方便外部模組（例如 UI）根據錯誤類型正確處理或顯示錯誤訊息。

---

## 🔥 資料流流程概述

```plaintext
1. 初始化 DataFacade → 讀取 game_log.csv → 特徵建構 → 讀取 q_table.pkl
2. 呼叫 get_game_log(), get_features(), get_q_table() 取得資料副本
3. 呼叫 append_game_log() 追加下注資料（可選是否自動 reload）
4. 呼叫 reload() → 資料刷新 → 觸發 on_data_updated 通知
5. 資料中心統一管理錯誤，確保系統穩定

