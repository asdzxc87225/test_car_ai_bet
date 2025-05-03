# tests/test_stats_controller.py
# tests/test_stats_controller.py

import pytest
import yaml
import pandas as pd
from stats.stats_controller import StatsController
from stats.dispatcher import get_callable, DISPATCH_TABLE

# 建立一個暫時的 YAML config 文件
@pytest.fixture
def tmp_config_file(tmp_path):
    config = {
        "metrics": [
            {"name": "win_rate_by_type", "type": "behavior", "method": "win_rate", "enabled": True},
            {"name": "qtable_max", "type": "q_table", "method": "max_q", "enabled": False},
        ]
    }
    config_path = tmp_path / "mock_stats.yaml"
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f)
    return config_path

def test_available_metrics(tmp_config_file):
    controller = StatsController(config_path=tmp_config_file)
    metrics = controller.get_available_metrics()
    assert "win_rate_by_type" in metrics
    assert "qtable_max" not in metrics  # disabled

def test_get_metrics_by_type(tmp_config_file):
    controller = StatsController(config_path=tmp_config_file)
    behavior_metrics = controller.get_metrics_by_type("behavior")
    assert len(behavior_metrics) == 1
    assert behavior_metrics[0]["method"] == "win_rate"

def test_summary_output(tmp_config_file):
    controller = StatsController(config_path=tmp_config_file)
    summary = controller.summary()
    assert "- win_rate_by_type" in summary

def test_run_all_enabled_metrics_basic(monkeypatch, tmp_config_file):
    controller = StatsController(config_path=tmp_config_file)
    dummy_df = {}

    # 模擬 hook 函式
    called = []

    def fake_callable(df):
        called.append("triggered")
        return {
            "data": {"sample": 1},
            "fig": None,
            "meta": {"status": "ok", "msg": "done"}
        }

    # 注入假 callable
    monkeypatch.setitem(DISPATCH_TABLE, ("behavior", "win_rate"), fake_callable)

    results = controller.run_all_enabled_metrics(dummy_df)
    assert called, "run_all_enabled_metrics 未正確執行 hook"
    assert isinstance(results, list)
    assert results[0]["meta"]["status"] == "ok"

def test_dispatcher_missing_callable_raises():
    with pytest.raises(ValueError):
        get_callable("nonexistent", "no_method")

def test_run_all_enabled_metrics_result_structure(monkeypatch, tmp_config_file):
    called = []

    def mock_fn(df):
        called.append("called")
        return {
            "data": {"mocked": True},
            "fig": None,
            "meta": {"status": "ok", "msg": "mock success"}
        }

    monkeypatch.setitem(DISPATCH_TABLE, ("behavior", "win_rate"), mock_fn)

    controller = StatsController(config_path=tmp_config_file)
    df = pd.DataFrame({"dummy": [1, 2, 3]})
    results = controller.run_all_enabled_metrics(df)

    assert "called" in called
    assert isinstance(results, list)
    assert "result" in results[0]
    assert results[0]["result"] == {"mocked": True}
    assert results[0]["meta"]["status"] == "ok"

