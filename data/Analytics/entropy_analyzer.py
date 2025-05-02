# data/Analytics_page/entropy_analyzer.py

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
import numpy as np
matplotlib.rc('font', family='Noto Serif CJK JP')


# 預設 fuzzy 門檻
DEFAULT_LOW_THRESH = 0.05
DEFAULT_HIGH_THRESH = 0.3

def load_entropy_data(path="logs/entropy_data.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    return df

def assign_fuzzy_level(df: pd.DataFrame, low=DEFAULT_LOW_THRESH, high=DEFAULT_HIGH_THRESH) -> pd.DataFrame:
    def fuzzify(e):
        if e < low:
            return "low"
        elif e < high:
            return "medium"
        else:
            return "high"
    df["risk_level"] = df["entropy"].apply(fuzzify)
    return df

def plot_entropy_vs_reward(df: pd.DataFrame, save_path="plots/entropy_vs_reward.png"):
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x="entropy", y="reward", data=df, alpha=0.5)
    plt.title("Entropy vs Reward")
    plt.xlabel("Entropy")
    plt.ylabel("Reward")
    plt.grid(True)
    _save_plot(save_path)

def plot_entropy_by_action(df: pd.DataFrame, save_path="plots/entropy_by_action.png"):
    plt.figure(figsize=(6, 5))
    sns.boxplot(x="action", y="entropy", data=df)
    plt.title("Entropy 分佈（依據 Action）")
    plt.xlabel("Action")
    plt.ylabel("Entropy")
    _save_plot(save_path)

def plot_reward_by_entropy_level(df: pd.DataFrame, save_path="plots/reward_by_risk_level.png"):
    plt.figure(figsize=(6, 5))
    sns.boxplot(x="risk_level", y="reward", data=df, order=["low", "medium", "high"])
    plt.title("Reward 分佈（依 fuzzy 風險等級）")
    plt.xlabel("Fuzzy 風險等級")
    plt.ylabel("Reward")
    _save_plot(save_path)

def plot_entropy_heatmap(df: pd.DataFrame, save_path="plots/entropy_heatmap.png"):
    if "diff" not in df.columns or "rolling_sum_5" not in df.columns:
        print("[WARN] 缺少 diff 或 rolling_sum_5 欄位，跳過熱圖")
        return

    pivot = df.groupby(["diff", "rolling_sum_5"])["entropy"].mean().unstack()
    if pivot.empty:
        print("[WARN] 熱圖資料為空，跳過畫圖")
        return

    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot, cmap="YlOrRd", annot=False)
    plt.title("狀態平均 Entropy 熱圖")
    plt.xlabel("rolling_sum_5")
    plt.ylabel("diff")
    _save_plot(save_path)

def plot_entropy_sample_distribution(df: pd.DataFrame, save_path="plots/entropy_sample_distribution.png"):
    df["entropy_bin"] = pd.cut(df["entropy"], bins=np.arange(0, 0.75, 0.05))
    counts = df["entropy_bin"].value_counts().sort_index()

    plt.figure(figsize=(8, 5))
    counts.plot(kind="bar", color="skyblue")
    plt.title("Entropy 區段樣本分佈圖")
    plt.xlabel("Entropy 區間")
    plt.ylabel("樣本數")
    plt.xticks(rotation=45)
    _save_plot(save_path)

def summarize_entropy_by_state(df: pd.DataFrame, save_path="logs/state_entropy_summary.csv") -> pd.DataFrame:
    df_state = df.groupby("state")["entropy"].mean().reset_index()
    df_state.columns = ["state", "avg_entropy"]
    df_state = df_state.sort_values("avg_entropy", ascending=False)
    df_state.to_csv(save_path, index=False)
    return df_state

def _save_plot(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path)
    print(f"[INFO] 圖片已儲存：{path}")
    plt.close()

def analyze_all():
    df = load_entropy_data()
    df = assign_fuzzy_level(df)

    plot_entropy_vs_reward(df)
    plot_entropy_by_action(df)
    plot_reward_by_entropy_level(df)
    plot_entropy_sample_distribution(df)
    plot_entropy_heatmap(df)
    summarize_entropy_by_state(df)

    print("\n[INFO] Entropy 分析與圖表已完成。")

if __name__ == "__main__":
    analyze_all()

