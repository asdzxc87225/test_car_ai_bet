import pandas as pd
from data.behavior_logic import calc_roi_curve

def test_calc_roi_curve_structure():
    # 建立假資料
    df = pd.DataFrame({
        "round": [1, 2, 3, 4, 5],
        "winner": [0, 1, 2, 3, 4],
        "bet":    [0, 1, 3, 2, 4]
    })

    result = calc_roi_curve(df)

    # 確認結構
    assert isinstance(result, dict)
    assert "fig" in result
    assert "data" in result
    assert "meta" in result
    assert "status" in result["meta"]

    # 若成功，進一步檢查資料
    if result["meta"]["status"] == "ok":
        assert "roi" in result["data"].columns, "data 中缺少 roi 欄位"

