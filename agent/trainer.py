from pathlib import Path
import pandas as pd
import numpy as np
import pickle
from collections import defaultdict

class QLearner:
    def __init__(self, epsilon=0.9, alpha=0.1, gamma=0.95):
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.q_table = defaultdict(lambda: np.zeros(2))  # 動作為 0/1

    def _get_state(self, row):
        """將單列資料轉換為 state key，例如 (diff, rolling_sum_5)"""
        return (row['diff'], row['rolling_sum_5'])

    def _choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice([0, 1])  # 探索
        return np.argmax(self.q_table[state])  # 利用

    def _update_q(self, s, a, r, s_):
        best_next_q = np.max(self.q_table[s_])
        self.q_table[s][a] += self.alpha * (r + self.gamma * best_next_q - self.q_table[s][a])

    def train(self, df: pd.DataFrame, episodes: int = 1000):
        required_cols = {"diff", "rolling_sum_5", "wine_type"}
        missing = required_cols - set(df.columns)

        if missing:
            raise ValueError(f"資料缺少必要欄位：{', '.join(missing)}")
        for ep in range(episodes):
            for i in range(len(df) - 1):
                row = df.iloc[i]
                next_row = df.iloc[i + 1]
                s = self._get_state(row)
                a = self._choose_action(s)

                # 獎勵設計：若猜中 wine_type，給 +1，否則 -1
                correct = int(a == row['wine_type'])
                r = 1 if correct else -1

                s_ = self._get_state(next_row)
                self._update_q(s, a, r, s_)

        self._finalize_q_table()

    def _finalize_q_table(self):
        """轉換 defaultdict 為固定 Q 表格 DataFrame"""
        index = list(self.q_table.keys())
        data = [self.q_table[s] for s in index]
        self.q_table = pd.DataFrame(data, index=index, columns=[0, 1])

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load(self, path):
        with open(path, 'rb') as f:
            self.q_table = pickle.load(f)

    def get_q_table(self) -> pd.DataFrame:
        return self.q_table

    def evaluate(self, df: pd.DataFrame) -> dict:
        hits = 0
        total = 0
        balance = 0

        for i in range(len(df)):
            row = df.iloc[i]
            s = self._get_state(row)
            if s not in self.q_table.index:
                continue
            a = np.argmax(self.q_table.loc[s])
            correct = int(a == row['wine_type'])
            total += 1
            hits += correct
            balance += (5 if correct else -1)  # 可依賠率自定義

        hit_rate = hits / total if total else 0
        roi = balance / total if total else 0

        return {
            "hit_rate": hit_rate,
            "roi": roi,
            "total_reward": balance,
            "total_tested": total
        }
