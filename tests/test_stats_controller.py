# tests/test_stats_controller.py

import pytest
from stats.stats_controller import StatsController
from pathlib import Path
import yaml

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

