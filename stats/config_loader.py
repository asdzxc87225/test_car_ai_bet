# data/config_loader.py

import yaml
from pathlib import Path

class ConfigLoader:
    def __init__(self, config_path: str | Path):
        self.path = Path(config_path)
        self.config = self._load_yaml()

    def _load_yaml(self) -> dict:
        with self.path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get(self, key: str, default=None):
        return self.config.get(key, default)

    def keys(self):
        return self.config.keys()

    def raw(self) -> dict:
        return self.config

