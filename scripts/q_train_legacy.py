import pandas as pd
import numpy as np
import random
from pathlib import Path

# 超參數
ACTIONS = [0, 1]  # 0: 不下注, 1: 下注
EPSILON = 0.9     # 探索率
ALPHA = 0.1       # 學習率
GAMMA = 0.9       # 折扣率
EPISODES = 500    # 訓練回合數

MODEL_DIR = Path("data/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """清理 diff 與 rolling_sum_5 使其落在合法範圍"""
    data = data.copy()
    data["diff"] = data["diff"].astype(int)
    data["rolling_sum_5"] = data["rolling_sum_5"].astype(int)
    valid_diffs = [0, 1, 2]
    valid_sums = [0, 1, 2, 3, 4, 5]
    return data[data["diff"].isin(valid_diffs) & data["rolling_sum_5"].isin(valid_sums)]

def build_q_table(states):
    q_table = pd.DataFrame(
        0.0,
        index=pd.MultiIndex.from_tuples(states, names=["diff", "rolling_sum_5"]),
        columns=ACTIONS
    )
    q_table.sort_index(inplace=True)
    return q_table

def choose_action(state, q_table):
    if (np.random.uniform() > EPSILON) or (state not in q_table.index):
        return np.random.choice(ACTIONS)
    row = q_table.loc[state]
    return int(row.idxmax())

def get_env_feedback(S, A, data):
    R = 0
    a0 = int(data['diff'])
    b0 = int(data['rolling_sum_5'])
    win = int(data["wine_type"])
    if A == 1:
        R = 2 if win == 1 else -8
    S_ = (a0, b0)
    return S_, R

def train_q_table(data):
    data = clean_data(data)
    all_states = [(d, r) for d in [0, 1, 2] for r in [0, 1, 2, 3, 4, 5]]
    q_table = build_q_table(all_states)

    for ep in range(EPISODES):
        idx = 0
        while idx + 1 < len(data):
            now = data.iloc[idx]
            nxt = data.iloc[idx + 1]

            S = (int(now["diff"]), int(now["rolling_sum_5"]))
            A = choose_action(S, q_table)
            S_, R = get_env_feedback(S, A, nxt)

            if S_ not in q_table.index:
                q_table.loc[S_, :] = 0.0
                q_table.sort_index(inplace=True)

            q_predict = float(q_table.loc[S, A])
            q_target = R + GAMMA * float(q_table.loc[S_].max())
            q_table.loc[S, A] += ALPHA * (q_target - q_predict)

            idx += 1

        if (ep + 1) % 50 == 0:
            name = f"ep{ep+1:04d}.pkl"
            q_table.to_pickle(MODEL_DIR / name)
            print(f"📦 存檔：{name}")

    return q_table

if __name__ == "__main__":
    df = pd.read_csv("data/train.csv")
    q_table = train_q_table(df)
    q_table.to_pickle(MODEL_DIR / "final.pkl")
    print("\n✅ 最終 Q-table：")
    print(q_table)

