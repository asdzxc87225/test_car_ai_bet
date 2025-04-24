# 🚗 AI 賽車下注工具

一個基於 Q-learning 強化學習的賽車下注系統，支援 UI 操作、快捷鍵下注、模型訓練與行為分析。

## 📦 專案架構總覽

- `data/`: 資料處理與模型儲存
- `agent/`: Q-learning 模型與訓練邏輯
- `scripts/`: CLI 模型訓練、評估與分析工具
- `ui/`: 使用者介面（PySide6）
- `docs/`: 學習筆記與分析報告

## 🚀 快速開始

make train    # 訓練 Q-learning 模型
make eval     # 評估模型表現
make run      # 啟動 UI

## 🚧 重構進行中：目標說明

目前專案正在進行 **模組分層重構與目錄整理**，目的是提升維護性與模組邊界清晰度。

### 🔧 第一階段：目錄結構重整
- [x] 將檔案依照邏輯分類（UI / Data / Core / Controller / Script）
- [ ] 搬移模組至新資料夾，但**不改邏輯、不改匯入方式**

### 🎯 接下來規劃
- 抽出 `ModelTrainingController`（從 `training_page.py` 拆出）
- 拆分 `data_facade.py` 成：
  - `q_table_manager.py`
  - `game_log_loader.py`
  - `state_feature_builder.py`
- 建立 UI → 控制器 → 資料層 的明確依賴流向

📄 詳細說明請見：
[`docs/refactor_plan.md`](docs/refactor_plan.md)


