# data/global_data.py
from data.data_facade import DataFacade
from data.config_loader import load_config
from pathlib import Path

DATA_FACADE = DataFacade(Path("./data"))
CONFIG = load_config()

class Session:
    _cache = {}

    @classmethod
    def get(cls, key: str, **kwargs):
        """取得 session 中的資料"""
        if key not in cls._cache:
            if key == "game_log":
                cls._cache[key] = DATA_FACADE.game_log()
            elif key == "q_table":
                model_name = kwargs.get("model_name", CONFIG.get("default_model", "q_model_0425_2023.pkl"))
                cls._cache[key] = DATA_FACADE.q_table(model_name)
            else:
                raise KeyError(f"未知資料類型 {key}")
        return cls._cache[key]

    @classmethod
    def refresh(cls, key: str, **kwargs):
        model_name = kwargs.get("model_name")
        if model_name and not model_name.endswith(".pkl"):
            model_name += ".pkl"  # 這裡正確補好

        if key == "game_log":
            DATA_FACADE.refresh_cache("raw/game_log.csv")
            cls._cache["game_log"] = DATA_FACADE.game_log()
        elif key == "q_table":
            if model_name:
                cls._cache["q_table"] = DATA_FACADE.q_table(model_name=model_name)
            else:
                cls._cache["q_table"] = DATA_FACADE.q_table()
        else:
            raise ValueError(f"不支援的刷新類型: {key}")

    @classmethod
    def clear_all(cls):
        """清除全部 session cache（可選功能）"""
        cls._cache.clear()

