# data/Analytics_page/entropy_plotter.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from pathlib import Path
matplotlib.rc('font', family='Noto Serif CJK JP')

def load_entropy_log(path="logs/entropy_data.csv") -> pd.DataFrame:
    if not Path(path).exists():
        raise FileNotFoundError(f"[ERROR] 找不到檔案：{path}")
    df = pd.read_csv(path)
    return df

def plot_entropy_distribution(df: pd.DataFrame, save_path=None, show=True):
    """畫出 entropy 的分佈圖（KDE + histogram）"""
    if "entropy" not in df.columns:
        raise ValueError("DataFrame 中找不到 entropy 欄位")

    plt.figure(figsize=(10, 6))
    sns.histplot(df["entropy"], kde=True, bins=40, color='skyblue', edgecolor='gray')

    plt.title("Entropy 分佈圖", fontsize=14)
    plt.xlabel("Entropy")
    plt.ylabel("樣本數 / 機率密度")
    plt.grid(True, linestyle="--", alpha=0.3)

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path)
        print(f"[INFO] 圖片儲存於：{save_path}")

    if show:
        plt.show()

def main():
    df = load_entropy_log()
    plot_entropy_distribution(df, save_path="plots/entropy_distribution.png")

if __name__ == "__main__":
    main()

