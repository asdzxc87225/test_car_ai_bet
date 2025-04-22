# data/data_facade.py
import os
import pandas as pd
from data.Analytics_page.feature_builder import build_features
class DataFacade:
    def __init__(self):
        # 設定資料位置（可日後讀設定檔）
        self.paths = {
            "game_log": "data/game_log.csv",
            "q_table": "data/models/final.pkl",
            "transition_matrix": "data/transition_matrix.csv"
        }


    def get_q_table(self) -> pd.DataFrame:
        return pd.read_pickle(self.paths["q_table"])

    def get_q_matrix(self, action: int = 1) -> pd.DataFrame:
        q_table = self.get_q_table()
        return q_table[action].unstack()

    def get_transition_matrix(self) -> pd.DataFrame:
        return pd.read_csv(self.paths["transition_matrix"], index_col=0)

    def list_models(self, dir_path="data/models") -> list[str]:
        return sorted([
            f for f in os.listdir(dir_path)
            if f.endswith(".pkl")
        ])

    def set_game_log(self, filename: str):
        self.paths["game_log"] = f"data/{filename}"

    def set_q_table(self, filename: str):
        self.paths["q_table"] = f"data/models/{filename}"
    def get_game_log(self) -> pd.DataFrame:
        df = pd.read_csv(self.paths["game_log"])
        df = build_features(df)  # 👈 加上自動處理
        return df

