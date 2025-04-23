
import pandas as pd
import numpy as np

class TransitionAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def get_matrix(self) -> pd.DataFrame:
        """回傳 transition matrix"""
        return self.df

    def calc_entropy(self) -> pd.DataFrame:
        """每個 row（狀態）的行熵"""
        def entropy(row):
            probs = row[row > 0]
            return -np.sum(probs * np.log2(probs))

        entropy_series = self.df.apply(entropy, axis=1)
        return entropy_series.reset_index(name="entropy")

    def calc_frequency(self) -> pd.DataFrame:
        """轉換為次數矩陣（假設轉移矩陣是機率）"""
        freq_matrix = self.df * 100  # 先簡單用倍數表示
        return freq_matrix.astype(int)
