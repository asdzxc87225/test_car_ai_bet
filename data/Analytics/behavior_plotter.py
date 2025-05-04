# data/Analytics_page/behavior_plotter.py
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import seaborn as sns
import ast


def safe_parse_bet(bet):
    try:
        if isinstance(bet, dict):
            return {int(k): v for k, v in bet.items()}
        elif isinstance(bet, str):
            parsed = ast.literal_eval(bet)
            if isinstance(parsed, dict):
                return {int(k): v for k, v in parsed.items()}
            elif isinstance(parsed, list):
                return {i: v for i, v in enumerate(parsed)}
        elif isinstance(bet, list):
            return {i: v for i, v in enumerate(bet)}
    except Exception:
        pass
    return {}  # 保底返回空 dict

def plot_cumulative_win_rate(df: pd.DataFrame) -> Figure:
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(df["round"], df["cumulative_win_rate"], marker="o", linewidth=2, label="累積勝率")
    ax.set_title(" 累積勝率折線圖")
    ax.set_xlabel("Round")
    ax.set_ylabel("Cumulative Win Rate")
    ax.grid(True)
    ax.legend()
    return fig


def plot_roi_line(df: pd.DataFrame) -> Figure:
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
    bet_count = {i: 0 for i in range(8)}

    for _, row in df.iterrows():
        try:
            if "bet" not in row or pd.isna(row["bet"]):
                continue

            bet = safe_parse_bet(row["bet"])
            for car, val in bet.items():
                if val > 0:
                    bet_count[int(car)] += 1
        except Exception as e:
            print(f"⚠️ round={row.get('round', '?')} 錯誤：{e}")
            continue

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
    for col in ["diff", "rolling_sum_5", "profit"]:
        if col not in df.columns:
            raise ValueError(f"資料中缺少欄位：{col}")

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

