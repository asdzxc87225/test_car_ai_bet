import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure

class TransitionPlotter:
    def __init__(self, font_family="Noto Serif CJK JP"):
        plt.rcParams['font.family'] = font_family

    def plot_entropy_bar(self, df_entropy: pd.DataFrame) -> Figure:
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # 取得 x 軸 label（將多重欄位合併成字串）
        if isinstance(df_entropy.columns[0], tuple) or df_entropy.columns[0] != "state":
            df_entropy["state"] = df_entropy.iloc[:, 0].astype(str)  # 將第一欄當作狀態名稱

        ax.bar(df_entropy["state"], df_entropy["entropy"], color="orange")
        ax.set_title("狀態轉移熵值")
        ax.set_ylabel("Entropy")
        ax.set_xlabel("State")
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        return fig

    def plot_transition_matrix(self, df_matrix: pd.DataFrame) -> Figure:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(df_matrix, annot=True, fmt=".2f", cmap="YlGnBu", ax=ax)
        ax.set_title("狀態轉移機率矩陣")
        ax.set_xlabel("下一狀態 s'")
        ax.set_ylabel("當前狀態 s")
        return fig

    def plot_frequency_matrix(self, df_freq: pd.DataFrame) -> Figure:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(df_freq, annot=True, fmt=".0f", cmap="Reds", ax=ax)
        ax.set_title("狀態轉移次數統計圖")
        ax.set_xlabel("下一狀態 s'")
        ax.set_ylabel("當前狀態 s")
        return fig

