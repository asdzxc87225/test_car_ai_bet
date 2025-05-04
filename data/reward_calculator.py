# data/reward_calculator.py

import pandas as pd

class RewardCalculator:
    @staticmethod
    def attach_reward(df: pd.DataFrame) -> pd.DataFrame:
        """
        為資料加入 reward 欄位：
        - 若下注中獎：reward = odds
        - 若沒中：reward = -100（可視情況修改）
        """
        df = df.copy()

        if not {'bet', 'winner', 'odds'}.issubset(df.columns):
            raise ValueError("缺少必要欄位：'bet', 'winner', 'odds'")

        df["reward"] = df.apply(
            lambda row: row["odds"] if row["bet"] == row["winner"] else -100,
            axis=1
        )
        return df

