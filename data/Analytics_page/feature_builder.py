# data/Analytics_page/feature_builder.py

import pandas as pd

SMALL_CARS = {0, 1, 2, 3}

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    加入以下欄位：
    - wine_type: 小車勝為 1，大車勝為 0
    - diff: 與前一局的差分（+1 平移避免 -1）
    - rolling_sum_5: 近五局小車勝次數
    """
    df = df.copy()

    # 小車勝：1，大車勝：0
    df["wine_type"] = df["winner"].apply(lambda x: 1 if x in SMALL_CARS else 0)

    # 與上一局的差分（並做偏移 +1）
    df["diff"] = df["wine_type"].diff().fillna(0).astype(int) + 1

    # 近 5 局小車勝利數（不 shift）
    df["rolling_sum_5"] = (
        df["wine_type"]
          .rolling(window=5, min_periods=1)
          .sum()
          .astype(int)
    )

    return df

