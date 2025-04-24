# 🚗 UC賽車下注系統：功能與需求規劃

## 🎯 目標
建構一套具備策略性下注能力的賽車遊戲 AI 系統，能夠結合 Q-learning 與統計分析，並透過 UI 呈現決策與行為結果。

---

## ✅ 第一階段需求（已完成／正在收尾）

### 資料處理與特徵工程
- 載入 `game_log.csv`
- 特徵計算：
  - `diff`
  - `rolling_sum_5`
  - `wine_type`

### 行為與狀態分析
- 勝率分析
- 投報率分析
- 下注分佈分析
- 狀態熱圖
- 狀態轉移矩陣
- 熵值與轉移頻率計算

### 模型與決策
- Q-learning 訓練與載入
- 根據 Q-table 給出下注建議

### UI 互動與資料視覺化
- 四大分頁架構：下注、AI 控制、資料分析、模型訓練
- 圖表顯示與互動分析按鈕

---

## 🔜 第二階段需求（預計開發）

### 策略與風險控制
- 熵值導向下注策略（EntropyStrategyAdvisor）
- 熵值風險視覺化（RiskVisualizer）
- 狀態風險分類（RiskClassifier）
- 模糊邏輯下注（FuzzyPolicy）

### 模擬與強化訓練
- 模擬器（SimulatorEnv）：依據轉移矩陣模擬下一輪
- 安全強化學習代理人（SafeQLearner, PPOAgent）
- 策略回測與統計（AutoBacktester）

---

## 📦 系統設計需求

### 模組解耦
- UI 不直接依賴分析邏輯，透過 Facade 模組（如 DataFacade）提供資料
- 策略模組與模型模組區分，僅交換決策資訊

### 資料一致性
- 所有模組共用 `DataFacade` 輸出格式（狀態、轉移、特徵）

### 可測性與擴充性
- 所有模組支援單元測試（不得依賴 UI 或檔案 I/O）
- 策略模組支援熱插拔（模糊邏輯、熵值、Q-learning 可替換）

---

## 📁 建議模組結構（抽象）

```
my_ai_bet_tool/
├── core/               ← 核心邏輯：AI、策略、分析器
│   ├── ai_action.py    ← AIPredictor, Q-table 載入
│   ├── entropy_strategy.py
│   ├── transition_analyzer.py
│   └── behavior_analyzer.py
│
├── data/               ← 資料存取與特徵工程
│   ├── data_facade.py
│   └── game_log.csv
│
├── ui/                 ← UI 分頁與元件
│   ├── main_window.py
│   ├── pages/
│   ├── components/
│   └── Analytics_page/
│
├── config/             ← 設定與路徑管理
│   └── config.py
│
├── docs/               ← 文件與計畫規劃
└── main.py
```

---

## 📌 備註
此文件作為模組重構與第二階段開發的需求依據，後續將補充實際資料欄位、狀態定義與熵值公式細節。


