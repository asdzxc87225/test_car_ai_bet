# data/data_facade.py

import pandas as pd
import pickle
import json
from pathlib import Path
from datetime import datetime
from data.feature_builder import FeatureBuilder
from data.data_errors import DataLoadError, DataFormatError

class DataFacade:
    def __init__(self, root: Path):
        """初始化資料中心，設定資料根目錄"""
        self.root = Path(root)
        self._cache: dict[str, object] = {}
        self._on_data_updated = []  # 資料更新通知 callback 列表（目前保留可擴充）

    # --- 對外資料讀取介面 ---
    def game_log(self) -> pd.DataFrame:
        """讀取 game_log"""
        return self._load_csv("raw/game_log.csv")

    def q_table(self, model_name: str = "q_model_0425_2023.pkl") -> pd.DataFrame:
        """讀取指定模型的 Q-Table"""
        return self._load_pickle(f"models/{model_name}")

    def list_models(self) -> list[str]:
        """列出 models 資料夾下所有 .pkl 模型檔案"""
        model_dir = self.root / "models"
        if not model_dir.exists():
            return []
        pkl_files = list(model_dir.glob("q_model_*.pkl"))
        models = [pkl_file.stem for pkl_file in pkl_files]
        return sorted(models)

    def append_game_log(self, new_entry: dict):
        """追加一筆新下注資料到 game_log.csv（不自動 reload，由 Session 控）"""
        if not isinstance(new_entry, dict):
            raise TypeError("新資料必須是 dict 格式")

        required_fields = ['timestamp', 'round', 'bet', 'winner']
        for field in required_fields:
            if field not in new_entry:
                raise DataFormatError(f"新資料缺少必要欄位: {field}")

        if isinstance(new_entry['bet'], list):
            new_entry['bet'] = json.dumps(new_entry['bet'])
        if isinstance(new_entry['timestamp'], datetime):
            new_entry['timestamp'] = new_entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S")

        df_new = pd.DataFrame([new_entry])

        try:
            df_new.to_csv(self.root / "raw/game_log.csv", mode='a', header=False, index=False)
            print("✅ 成功追加新資料到 game_log.csv")
        except Exception as e:
            raise DataLoadError(f"無法追加資料到 game_log.csv: {e}")

    # --- 資料加工（FeatureBuilder）---
    def build_features(self, df_game_log: pd.DataFrame) -> pd.DataFrame:
        """從 game_log 建構特徵欄位"""
        required_columns = ['timestamp', 'round', 'bet', 'winner']
        for col in required_columns:
            if col not in df_game_log.columns:
                raise DataFormatError(f"game_log 缺少必要欄位：{col}")

        features = FeatureBuilder.build_features(df_game_log)
        return features

    # --- 快取操作 ---
    def refresh_cache(self, key: str):
        """手動清除某個 key 的 cache"""
        self._cache.pop(key, None)

    def clear_all_cache(self):
        """清空所有 cache"""
        self._cache.clear()

    # --- 資料更新通知（目前保留，可用於未來 UI 主動更新）---
    def register_on_data_updated(self, callback: callable):
        """註冊資料更新通知的 callback"""
        if callable(callback):
            self._on_data_updated.append(callback)
        else:
            raise TypeError("callback 必須是 callable")

    def _notify_data_updated(self):
        """通知所有已註冊的 callback，資料已更新"""
        for callback in self._on_data_updated:
            try:
                callback()
            except Exception as e:
                print(f"[Error] 通知資料更新失敗: {e}")

    # --- 內部通用私有方法 ---
    def _load_csv(self, rel_path: str) -> pd.DataFrame:
        """從 cache 或磁碟讀取 CSV 檔"""
        if rel_path not in self._cache:
            self._cache[rel_path] = pd.read_csv(self.root / rel_path)
        return self._cache[rel_path]

    def _load_pickle(self, rel_path: str):
        """從 cache 或磁碟讀取 pickle 檔"""
        if rel_path not in self._cache:
            with open(self.root / rel_path, "rb") as f:
                self._cache[rel_path] = pickle.load(f)
        return self._cache[rel_path]

