# data/Analytics_page/q_table_analyzer.py

import pandas as pd

def load_q_table(path: str) -> pd.DataFrame:
    """讀取 Q-table 檔案（目前支援 .pkl）"""
    return pd.read_pickle(path)

def compute_max_q(q_table: pd.DataFrame) -> pd.Series:
    """每個 state 的最大 Q 值"""
    return q_table.max(axis=1)

def compute_q_confidence(q_table: pd.DataFrame) -> pd.Series:
    """Q 差值（信心度）：|Q1 - Q0|"""
    if 0 not in q_table.columns or 1 not in q_table.columns:
        raise ValueError("Q-table 必須包含動作 0 與 1")
    return (q_table[1] - q_table[0]).abs()

def compute_argmax_action(q_table: pd.DataFrame) -> pd.Series:
    """Q-table 中每個 state 對應的動作（0 or 1）"""
    return q_table.idxmax(axis=1)

def filter_by_confidence(q_table: pd.DataFrame, threshold: float) -> pd.Series:
    """信心度是否高於門檻（布林遮罩）"""
    confidence = compute_q_confidence(q_table)
    return confidence > threshold

