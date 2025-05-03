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
        results = []
        for metric in self.config.get("metrics", []):
            if not metric.get("enabled", False):
                continue
            mtype = metric["type"]
            method = metric["method"]
            name = metric["name"]
            print(f"[INFO] 執行分析：{name}（type: {mtype}, method: {method}）")
            try:
                fn = get_callable(mtype, method)
                result = fn(df)
                results.append({
                    "name": name,
                    "type": mtype,
                    "result": result.get("data", None),
                    "fig": result.get("fig", None),
                    "meta": result.get("meta", {"status": "ok", "msg": f"{name} 分析完成"})
                })
            except Exception as e:
                results.append({
                    "name": name,
                    "type": mtype,
                    "result": None,
                    "fig": None,
                    "meta": {"status": "error", "msg": str(e)}
                })
        return results
    def summary(self):
        lines = []
        for metric in self.get_available_metrics():
            lines.append(f"- {metric}")
        return "\n".join(lines)
    def run_by_name(self, name: str, df):
        for metric in self.config.get("metrics", []):
            if metric.get("name") == name and metric.get("enabled", False):
                fn = get_callable(metric["type"], metric["method"])
                return fn(df)
        raise ValueError(f"找不到啟用的分析項目：{name}")



