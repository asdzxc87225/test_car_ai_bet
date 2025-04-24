# 🔧 模組重構與解耦計畫（Refactor Plan）

## 🎯 目標
- 降低模組之間耦合程度，讓模組可以獨立測試、維護與替換
- 清楚定義每個模組的責任與資料流
- 為第二階段策略與風險模組整合做好架構準備

---

## 📁 模組責任與限制

| 模組 | 角色 | 專責處理 | 不該處理 |
|------|------|-----------|-----------|
| `DataFacade` | 資料中介 | 提供狀態資料、轉移矩陣、特徵工程結果 | 不處理圖表、不跑模型 |
| `AIPredictor` | 策略決策 | 根據狀態預測下注行為 | 不處理資料、不讀寫檔案 |
| `EntropyStrategyAdvisor` | 策略建議 | 根據熵值風險提供建議 | 不訓練模型、不處理 Q-table |
| `BehaviorAnalyzer` | 統計分析 | 勝率、報酬率、下注分布 | 不顯示 UI、不存圖表 |
| `TransitionAnalyzer` | 轉移分析 | 計算狀態轉移矩陣、熵值 | 不參與策略建議 |
| `UI/*.py` | 使用者介面 | 顯示分析結果、觸發控制邏輯 | 不進行資料處理、不指定檔案路徑 |

---

## 🔁 預定調整項目

### 1. 重構 `AIPredictor`
- ❌ 原本：自行處理路徑與資料載入
- ✅ 改為：只接受 `state` 與預先載入的 `Q-table`
- ✅ 預期介面：`predict(state) -> action`

### 2. 設計 `EntropyStrategyAdvisor`
- ✅ 功能：根據 `(state, entropy_map)` 提供下注建議
- ✅ 接口：`suggest_action(state) -> action`

### 3. 引入 `AIController`
- ✅ 作為 UI 與邏輯之間的中介層
- ✅ 管理 AIPredictor、Advisor 的實例與初始化

### 4. 統一使用 `DataFacade` 提供所有分析模組輸入
- ✅ BehaviorAnalyzer、TransitionAnalyzer 不再自己讀檔

---

## 📌 範例模組鏈接

```
UI: BettingPage
    ↳ Controller: AIController
        ↳ Model: AIPredictor
        ↳ Strategy: EntropyStrategyAdvisor
            ↳ Data: 熵值、Q-table（從 DataFacade 預載）
```

---

## 🧪 測試原則
- 所有核心模組（predictor/analyzer/strategy）都可單獨被測試
- 不依賴 UI、不依賴真實檔案路徑
- 資料來源統一由 `DataFacade` 提供 mock 資料

---

## 🧱 下一步建議
1. ✅ 先重構 `AIPredictor`，讓它不再接路徑，只吃 state + table
2. ✅ 建立 `EntropyStrategyAdvisor` 基礎介面與熵值 map 輸入
3. ✅ 設計 `AIController` 類別，供 UI 呼叫決策與策略查詢
4. ✅ 建立最小測試案例驗證解耦成功


