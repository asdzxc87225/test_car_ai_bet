# stats/hooks/transition_hook.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import entropy

def transition_entropy(df: pd.DataFrame) -> dict:
    """
    計算每個 state 的轉移 entropy，回傳圖表與數據結果
    需要欄位：'diff', 'rolling_sum_5'
    """
    try:
        df = df.copy()

        # 檢查欄位
        if "diff" not in df.columns or "rolling_sum_5" not in df.columns:
            raise ValueError("缺少必要欄位：'diff', 'rolling_sum_5'")

        # 建立 state 與 next_state 欄位
        df["state"] = list(zip(df["diff"], df["rolling_sum_5"]))
        df["next_state"] = df["state"].shift(-1)
        df = df.dropna(subset=["state", "next_state"])

        # 統計轉移次數
        transition_counts = Counter(zip(df["state"], df["next_state"]))

        # 組轉移清單
        state_transitions = {}
        for (s, ns), count in transition_counts.items():
            state_transitions.setdefault(s, []).append((ns, count))

        # 計算 entropy
        entropy_dict = {}
        for state, nexts in state_transitions.items():
            counts = np.array([c for _, c in nexts])
            probs = counts / counts.sum()
            entropy_dict[state] = entropy(probs, base=2)

        # 整理為 DataFrame
        result_df = pd.DataFrame([
            {"state": str(state), "entropy": ent}
            for state, ent in entropy_dict.items()
        ])

        # 繪圖
        fig, ax = plt.subplots(figsize=(7, 4))
        result_df.plot.bar(x="state", y="entropy", ax=ax)
        ax.set_title("Transition Entropy per State")
        ax.set_xlabel("State (diff, rolling_sum_5)")
        ax.set_ylabel("Entropy (bits)")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        return {
            "data": result_df,
            "fig": fig,
            "meta": {"status": "ok", "msg": "transition entropy 分析完成"}
        }

    except Exception as e:
        return {
            "data": None,
            "fig": None,
            "meta": {"status": "error", "msg": str(e)}
        }

