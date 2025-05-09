## 📦 專案架構說明（Architecture Overview）

### 🔧 目錄結構（責任導向）


### 📂 模組分層說明

| 資料夾       | 功能描述 |
|--------------|----------|
| `core/`       | 包含 Q-learning、策略判斷等非 UI 的邏輯 |
| `data/`       | 所有資料處理（CSV 載入、特徵建構、分析模組） |
| `controllers/` | 中介層，UI 不再直接控制學習與邏輯模組 |
| `ui/`         | 所有互動與畫面模組 |
| ...           | 其餘如 `scripts/`, `tests/`, `docs/` |

### 📈 模組依賴圖

![依賴圖](../main.svg)  ← 插入你先前產生的依賴圖

模組責任切割

UI 與資料中心解耦

權重切換邏輯整合

架構圖與後續優化方向建議


