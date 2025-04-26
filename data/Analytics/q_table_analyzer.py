# data/Analytics_page/q_table_analyzer.py

import pandas as pd
import pickle

def load_q_table(path: str) -> pd.DataFrame:
    """讀取 Q-table（支援新版 dict 與舊版 DataFrame）"""
    with open(path, "rb") as f:
        q_table = pickle.load(f)

    # ✅ 若是 dict，轉為 DataFrame
    if isinstance(q_table, dict):
        df = pd.DataFrame.from_dict(q_table, orient="index", columns=[0, 1])
        df.index.name = "state"
        return df

    # ✅ 若已是 DataFrame，直接使用
    elif isinstance(q_table, pd.DataFrame):
        return q_table

    else:
        raise ValueError("不支援的 Q-table 格式")

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

