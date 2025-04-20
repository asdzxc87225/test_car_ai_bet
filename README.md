# 🚗 AI 賽車下注工具

一個基於 Q-learning 強化學習的賽車下注系統，支援 UI 操作、快捷鍵下注、模型訓練與行為分析。

## 📦 專案架構總覽

- `data/`: 資料處理與模型儲存
- `agent/`: Q-learning 模型與訓練邏輯
- `scripts/`: CLI 模型訓練、評估與分析工具
- `ui/`: 使用者介面（PySide6）
- `docs/`: 學習筆記與分析報告

## 🚀 快速開始

```bash
make train    # 訓練 Q-learning 模型
make eval     # 評估模型表現
make run      # 啟動 UI

