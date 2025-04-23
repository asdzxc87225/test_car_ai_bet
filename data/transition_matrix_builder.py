# data/transition_matrix_builder.py

import pandas as pd
from collections import defaultdict

def build_transition_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    從 game_log 建立狀態轉移矩陣。
    狀態定義為 (diff, rolling_sum_5)

    Args:
        df: 包含 diff, rolling_sum_5 的資料表

    Returns:
        轉移機率矩陣（DataFrame，index 為起始狀態，columns 為下一狀態）
    """
    # 檢查欄位
    required_cols = {"diff", "rolling_sum_5"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"資料缺少必要欄位：{required_cols - set(df.columns)}")

    # 待補：下一步處理轉移邏輯與統計

    return pd.DataFrame()  # 暫時空表

def build_transition_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    從 game_log 建立狀態轉移矩陣。
    狀態定義為 (diff, rolling_sum_5)

    Returns:
        轉移機率矩陣（DataFrame，index 為起始狀態，columns 為下一狀態）
    """
    required_cols = {"diff", "rolling_sum_5"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"資料缺少必要欄位：{required_cols - set(df.columns)}")

    # 建立狀態序列
    states = list(zip(df["diff"], df["rolling_sum_5"]))

    # 統計轉移次數
    transition_counts = defaultdict(lambda: defaultdict(int))
    for (s1, s2) in zip(states[:-1], states[1:]):
        transition_counts[s1][s2] += 1

    # 所有出現過的狀態
    all_states = sorted(set(states))

    # 建立明確的 MultiIndex
    index = pd.MultiIndex.from_tuples(all_states, names=["diff", "rolling_sum_5"])
    count_matrix = pd.DataFrame(
        data=0,
        index=index,
        columns=index,
        dtype=float  # ✅ 確保後續 heatmap 可用
    )

    for s1 in transition_counts:
        for s2 in transition_counts[s1]:
            count_matrix.loc[s1, s2] = transition_counts[s1][s2]

    # 正規化：轉為機率矩陣
    prob_matrix = count_matrix.div(count_matrix.sum(axis=1), axis=0).fillna(0)

    return  prob_matrix
