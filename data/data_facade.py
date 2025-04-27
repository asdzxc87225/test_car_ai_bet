import pickle
import pandas as pd

class DataFacade:
    def __init__(self, path_game_log: str, path_q_table: str):
        self.path_game_log = path_game_log
        self.path_q_table = path_q_table
        self._game_log = None
        self._features = None
        self._q_table = None

        self._load_game_log()
        self._load_q_table()

    def _load_game_log(self):
        """從 CSV 讀取 game_log 並緩存"""
        try:
            self._game_log = pd.read_csv(self.path_game_log)
        except Exception as e:
            print(f"[Error] 無法讀取 game_log: {e}")

    def _load_q_table(self):
        """從 pickle 檔案讀取 q_table"""
        try:
            with open(self.path_q_table, "rb") as f:
                self._q_table = pickle.load(f)
        except Exception as e:
            print(f"[Error] 無法讀取 q_table: {e}")

    def get_game_log(self):
        if self._game_log is not None:
            return self._game_log.copy()
        else:
            raise ValueError("尚未載入 game_log 資料！")

    def get_q_table(self):
        if self._q_table is not None:
            # 如果是 DataFrame，就 copy
            if hasattr(self._q_table, "copy"):
                return self._q_table.copy()
            # 如果是 dict 就直接傳（dict一般不用深複製）
            return self._q_table
        else:
            raise ValueError("尚未載入 q_table 資料！")
