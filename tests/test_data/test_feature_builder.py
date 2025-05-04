# tests/test_data/test_feature_builder.py

import pandas as pd
from data.feature_builder import FeatureBuilder

def test_build_features_output():
    data = {
        "winner": [0, 1, 4, 5, 3],
        "bet": [0, 2, 4, 5, 1]
    }
    df = pd.DataFrame(data)
    result = FeatureBuilder.build_features(df)

    assert "wine_type" in result.columns
    assert "diff" in result.columns
    assert "rolling_sum_5" in result.columns
    assert "win" in result.columns
    assert "cumulative_win_rate" in result.columns

    # 檢查值範圍與資料型別
    assert result["wine_type"].isin([0, 1]).all()
    assert pd.api.types.is_numeric_dtype(result["diff"])
    assert pd.api.types.is_numeric_dtype(result["rolling_sum_5"])
    assert result["win"].isin([0, 1]).all()
    assert pd.api.types.is_float_dtype(result["cumulative_win_rate"])

