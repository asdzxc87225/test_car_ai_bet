# tests/test_dispatcher_and_hooks.py

import pytest
import pandas as pd
from stats.dispatcher import get_callable

def test_behavior_hooks_callable():
    import pandas as pd
    dummy_df = pd.DataFrame({"dummy": [1, 2, 3]})

    for method in ["win_rate", "roi", "bet_distribution"]:
        fn = get_callable("behavior", method)
        assert callable(fn)

        result = fn(dummy_df)
        assert isinstance(result, dict)
        assert result["meta"]["status"] == "error"


def test_qtable_hooks_callable():
    dummy_q = {}  # 模擬一個簡單的 Q 表
    for method in ["max_q", "q_gap", "strategy_entropy"]:
        fn = get_callable("q_table", method)
        assert callable(fn)
        assert fn(dummy_q) is None

def test_entropy_hook_callable():
    dummy_df = pd.DataFrame({"entropy": [0.1, 0.5, 0.9]})
    fn = get_callable("entropy", "entropy_histogram")
    assert callable(fn)
    assert fn(dummy_df) is None

def test_invalid_dispatch_key():
    with pytest.raises(ValueError):
        get_callable("unknown", "nope")

