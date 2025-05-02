# scripts/evaluate_q_table.py

import pandas as pd
import matplotlib.pyplot as plt
from core.ai_action import AIPredictor
from data.global_data import DATA_FACADE, Session
import argparse
from pathlib import Path


def evaluate_q_table(q_table=None):
    df = DATA_FACADE.game_log()
    df = DATA_FACADE.build_features(df)

    if q_table is None:
        q_table = Session.get("q_table")

    predictor = AIPredictor(q_table)
    rewards = []
    cumulative_rewards = []
    actions = []
    total_bets = 0
    total_hits = 0
    x_data, y_data = [], []

    for frame in range(5, len(df)):
        try:
            diff = int(df.iloc[frame]["diff"])
            rsum = int(df.iloc[frame]["rolling_sum_5"])
            wine_type = int(df.iloc[frame]["wine_type"])
            suggestion = predictor.predict_action((diff, rsum))
        except Exception as e:
            print(f"[WARN] Prediction failed at round {frame}: {e}")
            continue

        if suggestion == 1:
            total_bets += 1
            if wine_type == 1:
                reward = 20
                total_hits += 1
            else:
                reward = -80
        else:
            reward = 0

        rewards.append(reward)
        cumulative_rewards.append(sum(rewards))
        x_data.append(frame)
        y_data.append(cumulative_rewards[-1])
        actions.append(suggestion)

    # 儲存為靜態圖
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    ax.plot(x_data, y_data, color='blue')
    ax.set_title("Cumulative Reward")
    ax.set_xlabel("Round")
    ax.set_ylabel("Cumulative Reward")
    ax.set_xlim(0, len(df))
    ax.set_ylim(min(y_data) - 50, max(y_data) + 50)
    Path("plots").mkdir(parents=True, exist_ok=True)
    plt.savefig("plots/eval_cumulative_reward.png", bbox_inches='tight')
    print("[INFO] Saved evaluation curve to plots/eval_cumulative_reward.png")
    plt.close()

    roi = sum(rewards) / total_bets if total_bets else 0
    hit_rate = total_hits / total_bets if total_bets else 0
    coverage = total_bets / (len(df) - 5)

    print("\nModel Evaluation Result")
    print("------------------------")
    print(f"Total Bets     : {total_bets}")
    print(f"Total Hits     : {total_hits}")
    print(f"Hit Rate       : {hit_rate:.2%}")
    print(f"ROI            : {roi:.2f}")
    print(f"Coverage       : {coverage:.2%}")
    print("------------------------")


def load_q_table_by_name(model_name):
    file_path = Path("data/models") / f"{model_name}"
    if not file_path.exists():
        raise FileNotFoundError(f"Model not found: {file_path}")
    return DATA_FACADE.q_table(model_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Q-table performance")
    parser.add_argument("--model", type=str, help="Model filename (without .pkl)")
    args = parser.parse_args()

    if args.model:
        q_table = load_q_table_by_name(args.model)
    else:
        q_table = None

    evaluate_q_table(q_table)

