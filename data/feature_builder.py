# data/feature_builder.py
import pandas as pd
from pathlib import Path

SMALL_CARS = {0, 1, 2, 3}

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """加入 wine_type / diff / rolling_sum_5，返回新 DataFrame"""
    df = df.copy()

    # 小車 = 1；大車 = 0
    df["wine_type"] = df["winner"].apply(lambda x: 1 if x in SMALL_CARS else 0)

    # 與上一局的差分
    df["diff"] = df["wine_type"].diff().fillna(0).astype(int)

    # 近 5 局小車勝利數（不 shift）
    df["rolling_sum_5"] = (
        df["wine_type"]
          .rolling(window=5, min_periods=1)
          .sum()
          .astype(int)
    )
    return df

