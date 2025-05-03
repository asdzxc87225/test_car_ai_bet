# stats_controller.py

import yaml
from pathlib import Path
from stats.dispatcher import get_callable

class StatsController:
    def __init__(self, config_path="configs/stats.yaml"):
        self.config = self._load_config(config_path)

    def _load_config(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_available_metrics(self):
        """回傳可支援的分析項目清單"""
        return [m["name"] for m in self.config.get("metrics", []) if m.get("enabled", False)]
    def get_metrics_by_type(self, mtype: str):
        """取得指定類型（如 'behavior'）的啟用任務"""
        return [m for m in self.config.get("metrics", []) if m.get("type") == mtype and m.get("enabled", False)]
    def run_all_enabled_metrics(self, df):
        for metric in self.config.get("metrics", []):
            if not metric.get("enabled", False):
                continue
            mtype = metric["type"]
            method = metric["method"]
            name = metric["name"]
            print(f"[INFO] 執行分析：{name}（type: {mtype}, method: {method}）")
            fn = get_callable(mtype, method)
            fn(df)  # 傳入假資料即可測試
    def summary(self):
        lines = []
        for metric in self.get_available_metrics():
            lines.append(f"- {metric}")
        return "\n".join(lines)


