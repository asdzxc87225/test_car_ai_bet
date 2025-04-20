import pandas as pd
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from pathlib import Path
import numpy as np
from math import log2

matplotlib.rc('font', family='Noto Serif CJK JP')

class TransitionMatrixAnalyzer:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        self.transition_counts = defaultdict(lambda: defaultdict(int))
        self.matrix = None
        self.states = None
        self.multi_states = None

    def compute_transition_counts(self):
        for i in range(len(self.df) - 1):
            s1 = (int(self.df.iloc[i]["diff"]), int(self.df.iloc[i]["rolling_sum_5"]))
            s2 = (int(self.df.iloc[i + 1]["diff"]), int(self.df.iloc[i + 1]["rolling_sum_5"]))
            self.transition_counts[s1][s2] += 1

    def build_transition_matrix(self):
        self.states = sorted(set(self.transition_counts.keys()) | {s for v in self.transition_counts.values() for s in v})
        self.multi_states = pd.MultiIndex.from_tuples(self.states, names=["diff", "rolling_sum_5"])
        self.matrix = pd.DataFrame(index=self.multi_states, columns=self.multi_states, data=0.0)

        for s1 in self.transition_counts:
            total = sum(self.transition_counts[s1].values())
            for s2 in self.transition_counts[s1]:
                self.matrix.loc[s1, s2] = self.transition_counts[s1][s2] / total

    def save_matrix_to_csv(self, out_path: str):
        self.matrix.to_csv(out_path)

    def plot_heatmap(self, save_path: str = "data/transition_matrix_heatmap.png"):
        matrix_flat = self.matrix.copy()
        matrix_flat.index = [f"{a},{b}" for a, b in matrix_flat.index]
        matrix_flat.columns = [f"{a},{b}" for a, b in matrix_flat.columns]

        plt.figure(figsize=(12, 10))
        sns.heatmap(matrix_flat, cmap="YlGnBu", annot=False)
        plt.title("Markov 狀態轉移機率矩陣")
        plt.xlabel("Next State")
        plt.ylabel("Current State")
        plt.tight_layout()
        plt.savefig(save_path)
        plt.show()

    def plot_high_frequency_paths(self, top_n=10):
        flat_transitions = [((a, b), (c, d), count)
                            for (a, b), targets in self.transition_counts.items()
                            for (c, d), count in targets.items()]
        sorted_transitions = sorted(flat_transitions, key=lambda x: -x[2])[:top_n]

        print("\n🔥 高頻轉移路徑：")
        for s1, s2, cnt in sorted_transitions:
            print(f"{s1} → {s2}：{cnt} 次")

    def compute_entropy(self):
        entropy_dict = {}
        for s1 in self.transition_counts:
            total = sum(self.transition_counts[s1].values())
            probs = [v / total for v in self.transition_counts[s1].values() if v > 0]
            entropy = -sum(p * log2(p) for p in probs)
            entropy_dict[s1] = entropy

        entropy_series = pd.Series(entropy_dict).sort_values(ascending=False)
        print("\n📊 各狀態熵值（不確定性）：")
        print(entropy_series.head(10))

    def run_all(self):
        print("📥 開始分析 train.csv 的狀態轉移矩陣...")
        self.compute_transition_counts()
        self.build_transition_matrix()
        self.save_matrix_to_csv("data/transition_matrix.csv")
        self.plot_heatmap()
        self.plot_high_frequency_paths()
        self.compute_entropy()
        print("✅ 分析完成，結果已儲存與繪製完畢。")


if __name__ == "__main__":
    analyzer = TransitionMatrixAnalyzer("data/train.csv")
    analyzer.run_all()

