# data/feature_builder.py

import pandas as pd

class FeatureBuilder:
    @staticmethod
    def build_features(df: pd.DataFrame) -> pd.DataFrame:
        """
        為原始資料加上分析所需的特徵欄位：
        - wine_type：小車勝利為 1，大車為 0
        - diff：前後勝利型態差值
        - rolling_sum_5：前 5 回合的小車勝利總數
        """
        df = df.copy()

        df["wine_type"] = (df["winner"] < 4).astype(int)
        df["diff"] = df["wine_type"].diff().fillna(0)
        df["rolling_sum_5"] = df["wine_type"].rolling(window=5, min_periods=1).sum()

        # ✅ 檢查 bet 欄位是否存在再建立 win 資料
        if "bet" in df.columns:
            df["win"] = (df["bet"] == df["winner"]).astype(int)
            df["cumulative_win_rate"] = df["win"].expanding().mean()

        return df
