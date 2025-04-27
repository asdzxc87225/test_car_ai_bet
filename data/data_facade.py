import pickle
import pandas as pd
from data.feature_builder import FeatureBuilder
import json
from datetime import datetime
from data.data_errors import DataLoadError, DataFormatError

class DataFacade:
    def __init__(self, path_game_log: str, path_q_table: str):
        """初始化資料中心，讀取 game_log 與 q_table，建構特徵資料"""
        self._on_data_updated = []  # 資料更新後的通知 callback 列表

        self.path_game_log = path_game_log
        self.path_q_table = path_q_table
        self._game_log = None
        self._features = None
        self._q_table = None

        self._load_game_log()
        self._build_features()
        self._load_q_table()

    def register_on_data_updated(self, callback: callable):
        """外部模組可以註冊資料更新完成時要通知的函數"""
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

    def reload(self):
        """重新讀取資料並刷新快取（game_log, features, q_table）"""
        self._load_game_log()
        self._build_features()
        self._load_q_table()
        self._notify_data_updated()

    def _build_features(self):
        """加工特徵資料，快取起來"""
        if self._game_log is None:
            raise DataLoadError("尚未載入 game_log 資料，無法建構 features。")
        
        # 檢查必要欄位是否存在
        required_columns = ['timestamp', 'round', 'bet', 'winner']
        for col in required_columns:
            if col not in self._game_log.columns:
                raise DataFormatError(f"game_log 缺少必要欄位：{col}")

        self._features = FeatureBuilder.build_features(self._game_log)

    def _load_game_log(self):
        """從 CSV 讀取 game_log 並快取"""
        try:
            self._game_log = pd.read_csv(self.path_game_log)
        except FileNotFoundError:
            raise DataLoadError(f"找不到 game_log 檔案：{self.path_game_log}")
        except Exception as e:
            raise DataLoadError(f"讀取 game_log 時發生錯誤：{e}")

    def _load_q_table(self):
        """從 pickle 檔案讀取 q_table 並快取"""
        try:
            with open(self.path_q_table, "rb") as f:
                self._q_table = pickle.load(f)
        except FileNotFoundError:
            raise DataLoadError(f"找不到 q_table 檔案：{self.path_q_table}")
        except Exception as e:
            raise DataLoadError(f"讀取 q_table 時發生錯誤：{e}")

    def get_features(self):
        """取得特徵資料的副本（防止外部污染）"""
        if self._features is not None:
            return self._features.copy()
        else:
            raise DataLoadError("尚未建構 features 資料！")

    def get_game_log(self):
        """取得 game_log 的副本"""
        if self._game_log is not None:
            return self._game_log.copy()
        else:
            raise DataLoadError("尚未載入 game_log 資料！")

    def get_q_table(self):
        """取得 q_table 的副本（DataFrame）或直接回傳（dict）"""
        if self._q_table is not None:
            if hasattr(self._q_table, "copy"):
                return self._q_table.copy()
            return self._q_table
        else:
            raise DataLoadError("尚未載入 q_table 資料！")

    def append_game_log(self, new_entry: dict, auto_reload: bool = True):
        """追加一筆新下注資料到 game_log.csv，可選擇是否自動刷新快取"""
        if not isinstance(new_entry, dict):
            raise TypeError("新資料必須是 dict 格式")

        required_fields = ['timestamp', 'round', 'bet', 'winner']
        for field in required_fields:
            if field not in new_entry:
                raise DataFormatError(f"新資料缺少必要欄位: {field}")

        # 強制 bet 轉成 JSON 字串格式
        if isinstance(new_entry['bet'], list):
            new_entry['bet'] = json.dumps(new_entry['bet'])

        # 強制 timestamp 轉成標準字串格式
        if isinstance(new_entry['timestamp'], datetime):
            new_entry['timestamp'] = new_entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S")

        df_new = pd.DataFrame([new_entry])

        try:
            df_new.to_csv(self.path_game_log, mode='a', header=False, index=False)
            print("✅ 成功追加新資料到 game_log.csv")
            if auto_reload:
                self.reload()
        except Exception as e:
            raise DataLoadError(f"無法追加資料到 game_log.csv: {e}")

