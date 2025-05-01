# core/q_table_manager.py

import pandas as pd
from typing import List, Tuple

class QTableManager:
    def __init__(self):
        self.q_table = None
        self.meta = {}
    def init_q_table_from_range(self, diff_range: range, rsum_range: range, n_actions: int) -> pd.DataFrame:
        states = [(d, r) for d in diff_range for r in rsum_range]
        return self.init_q_table(states, n_actions)
    def init_q_table(self, states: List[Tuple[int, int]], n_actions: int) -> pd.DataFrame:
        self.q_table = pd.DataFrame(
            0.0, 
            index=pd.MultiIndex.from_tuples(states, names=["diff", "rsum"]),
            columns=range(n_actions)
        )
        self.meta = {
            "version": "2.0b",
            "n_actions": n_actions,
            "n_states": len(states),
        }
        return self.q_table
    def from_dict(self, q_dict: dict, n_actions: int = None) -> pd.DataFrame:
        """手動轉換 dict → MultiIndex DataFrame"""
        if not q_dict:
            raise ValueError("q_dict 為空，無法轉換成 Q 表")

        index = list(q_dict.keys())
        data = list(q_dict.values())

        if n_actions is None:
            first_row = data[0]
            if not isinstance(first_row, (list, tuple)):
                raise ValueError("q_dict 的值應為 list 或 tuple")
            n_actions = len(first_row)

        df = pd.DataFrame(data, index=pd.MultiIndex.from_tuples(index, names=["diff", "rsum"]))
        df.columns = list(range(n_actions))
        self.q_table = df
        return df




