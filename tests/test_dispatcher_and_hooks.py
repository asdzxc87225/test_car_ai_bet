# tests/test_dispatcher_and_hooks.py

import pytest
import pandas as pd
from stats.dispatcher import get_callable

def test_behavior_hooks_callable():
    dummy_df = pd.DataFrame({"dummy": [1, 2, 3]})
    fn = get_callable("behavior", "win_rate")
    assert callable(fn)
    assert fn(dummy_df) is None  # placeholder 回傳 None

    fn = get_callable("behavior", "roi")
    assert fn(dummy_df) is None

    fn = get_callable("behavior", "bet_distribution")
    assert fn(dummy_df) is None

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

