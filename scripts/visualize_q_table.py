import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pathlib import Path
import pickle
import matplotlib
matplotlib.rc('font', family='Noto Serif CJK JP')

MODEL_PATH = Path("data/models/104900.pkl")


def load_q_table(path: Path) -> pd.DataFrame:
    with path.open("rb") as f:
        q_table = pickle.load(f)
    if not isinstance(q_table.index, pd.MultiIndex):
        if isinstance(q_table.index[0], tuple):
            q_table.index = pd.MultiIndex.from_tuples(
                q_table.index, names=["diff", "rolling_sum_5"])
    return q_table


def plot_q_table(q_table: pd.DataFrame):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    q0 = q_table[0].unstack().fillna(0)
    q1 = q_table[1].unstack().fillna(0)

    sns.heatmap(q0, annot=True, fmt=".1f", cmap="YlGnBu", ax=axes[0])
    axes[0].set_title("Q-value: 不下注 (Action 0)")

    sns.heatmap(q1, annot=True, fmt=".1f", cmap="YlOrRd", ax=axes[1])
    axes[1].set_title("Q-value: 下注 (Action 1)")

    for ax in axes:
        ax.invert_yaxis()
        ax.set_xlabel("rolling_sum_5")
        ax.set_ylabel("diff")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("📥 載入 Q-table...")
    q_table = load_q_table(MODEL_PATH)
    print("📊 繪製視覺化圖表...")
    plot_q_table(q_table)

