import pandas as pd
import numpy as np
import pickle
from pathlib import Path

ACTIONS = [0, 1]  # 0: 不下注, 1: 下注
MODEL_PATH = Path("data/models/107140.pkl")
TEST_PATH = Path("data/train.csv")


def load_model(path: Path) -> pd.DataFrame:
    with path.open("rb") as f:
        return pickle.load(f)


def choose_action(state, q_table) -> int:
    if state in q_table.index:
        return int(q_table.loc[state].idxmax())
    return 1  # fallback：預設下注小車


def evaluate(q_table: pd.DataFrame, test_df: pd.DataFrame) -> dict:
    test_df = test_df.copy()
    test_df["action"] = 0
    test_df["reward"] = 0

    correct = 0
    total_bets = 0
    total_reward = 0

    for i in range(len(test_df) - 1):
        now = test_df.iloc[i]
        nxt = test_df.iloc[i + 1]

        state = (int(now["diff"]), int(now["rolling_sum_5"]))
        action = choose_action(state, q_table)
        test_df.at[i, "action"] = action

        if action == 1:
            reward = 20 if nxt["wine_type"] == 1 else -80
            total_reward += reward
            total_bets += 1
            if reward > 0:
                correct += 1
            test_df.at[i, "reward"] = reward

    return {
        "總樣本數": len(test_df),
        "下注次數": total_bets,
        "命中次數": correct,
        "命中率": correct / total_bets if total_bets else 0,
        "總報酬": total_reward,
    }, test_df


if __name__ == "__main__":
    print("📥 載入模型與測試集...")
    q_table = load_model(MODEL_PATH)
    test_df = pd.read_csv(TEST_PATH)
    print(q_table.index)
     # 🔧 插入：修正 q_table 索引格式為 MultiIndex
    if isinstance(q_table.index[0], tuple):
        q_table.index = pd.MultiIndex.from_tuples(q_table.index, names=["diff", "rolling_sum_5"])

    print("🔍 開始驗證...")
    metrics, result_df = evaluate(q_table, test_df)

    print("\n📊 評估結果：")
    for k, v in metrics.items():
        print(f"{k}：{v}")

    # 若需要輸出詳細結果
    result_df.to_csv("data/eval_result.csv", index=False)
    print("\n✅ 結果已儲存至 data/eval_result.csv")

