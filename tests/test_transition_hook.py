# tests/test_transition_hook.py

import pytest
import pandas as pd
from stats.hooks.transition_hook import transition_entropy

def test_transition_entropy_output_ok():
    # 準備 mock 資料：有 diff 與 rolling_sum_5 欄位
    df = pd.DataFrame({
        "diff": [1, 0, -1, 1, 1],
        "rolling_sum_5": [2, 2, 1, 3, 4]
    })
    
    result = transition_entropy(df)

    assert result["meta"]["status"] == "ok"
    assert result["fig"] is not None
    assert result["data"] is not None
    assert "entropy" in result["data"].columns

def test_transition_entropy_missing_column():
    # 準備錯誤資料：少欄位
    df = pd.DataFrame({
        "rolling_sum_5": [1, 2, 3, 4, 5]
    })

    result = transition_entropy(df)

    assert result["meta"]["status"] == "error"
    assert "diff" in result["meta"]["msg"]

