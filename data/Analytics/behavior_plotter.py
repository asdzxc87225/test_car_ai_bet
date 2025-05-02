# data/Analytics_page/behavior_plotter.py

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import seaborn as sns



def plot_cumulative_win_rate(df: pd.DataFrame) -> Figure:
    """
    繪製累積勝率折線圖

    Args:
        df: 包含欄位 round, cumulative_win_rate

    Returns:
        matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df["round"], df["cumulative_win_rate"], marker="o", linewidth=2, label="累積勝率")
    ax.set_title(" 累積勝率折線圖")
    ax.set_xlabel("Round")
    ax.set_ylabel("Cumulative Win Rate")
    ax.grid(True)
    ax.legend()
    return fig
def plot_roi_line(df: pd.DataFrame) -> Figure:
    """
    繪製每局 ROI（投報率）變化圖

    Args:
        df: 包含欄位 round, roi

    Returns:
        matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df["round"], df["roi"], marker="x", linestyle="-", linewidth=1.5, color="green", label="投報率 ROI")
    ax.axhline(1.0, color="gray", linestyle="--", linewidth=1, label="損益平衡線")
    ax.set_title(" 每局投報率 ROI")
    ax.set_xlabel("Round")
    ax.set_ylabel("ROI")
    ax.grid(True)
    ax.legend()
    return fig

def plot_bet_distribution(df: pd.DataFrame, car_labels: dict = None) -> Figure:
    """
    畫出各台車的總下注次數（有下注即算一次）

    Args:
        df: 包含 'bet' 欄位的 DataFrame
        car_labels: 可選，車輛名稱對照字典（例如 {"0": "聯結機"}）

    Returns:
        matplotlib.figure.Figure
    """
    bet_count = {i: 0 for i in range(8)}  # 假設 0~7 共 8 台車

    for _, row in df.iterrows():
        try:
            # 檢查欄位與空值
            if "bet" not in row or pd.isna(row["bet"]):
                raise ValueError("bet 欄位遺失或為空")

            # 處理下注格式
            bet = row["bet"]
            if isinstance(bet, str):
                bet = eval(bet)
            if isinstance(bet, list):
                bet = {i: v for i, v in enumerate(bet)}
            if isinstance(bet, dict):
                bet = {int(k): v for k, v in bet.items()}
            else:
                raise ValueError(f"無法解析下注格式：{type(bet)}")

            for car, val in bet.items():
                if val > 0:
                    bet_count[int(car)] += 1

        except Exception as e:
            print(f"⚠️ 計算下注分佈失敗 round={row.get('round', '?')} 錯誤：{e}")
            continue

    # 畫圖
    fig, ax = plt.subplots(figsize=(7, 4))
    keys = list(bet_count.keys())
    values = list(bet_count.values())
    labels = [car_labels.get(str(k), f"車 {k}") for k in keys] if car_labels else [f"車 {k}" for k in keys]

    ax.bar(labels, values, color="skyblue")
    ax.set_title(" 各車下注次數分佈")
    ax.set_ylabel("次數")
    ax.set_xlabel("車輛")
    ax.grid(axis="y")

    return fig


def plot_state_reward_heatmap(df: pd.DataFrame) -> Figure:
    """
    畫出 (diff, rolling_sum_5) 為 state 的平均報酬 heatmap

    Args:
        df: 包含 diff, rolling_sum_5, profit 欄位的 DataFrame

    Returns:
        matplotlib.figure.Figure
    """
    # 檢查欄位是否存在
    print(pd)
    for col in ["diff", "rolling_sum_5", "profit"]:
        if col not in df.columns:
            raise ValueError(f"資料中缺少欄位：{col}")

    # 轉為 heatmap 數據
    pivot = df.pivot_table(
        index="rolling_sum_5",
        columns="diff",
        values="profit",
        aggfunc="mean"
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="coolwarm", center=0, ax=ax)

    ax.set_title(" 狀態 (diff, rolling_sum_5) 平均報酬熱圖")
    ax.set_xlabel("diff")
    ax.set_ylabel("rolling_sum_5")

    return fig


