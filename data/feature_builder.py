import pandas as pd

class FeatureBuilder:
    @staticmethod
    def build_features(game_log: pd.DataFrame) -> pd.DataFrame:
        """依據 game_log 加工出特徵欄位"""
        df = game_log.copy()
        df['wine_type'] = (df['winner'] < 4).astype(int)
        df['diff'] = df['wine_type'].diff()
        df['rolling_sum_5'] = df['diff'].rolling(window=5, min_periods=1).sum()
        return df

