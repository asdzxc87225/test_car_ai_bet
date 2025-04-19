import argparse
from pathlib import Path
import pandas as pd
from agent.trainer import QLearner
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="訓練 Q-learning 模型")
    parser.add_argument("--input", type=str, default="data/train.csv", help="訓練資料路徑")
    parser.add_argument("--output", type=str, default="", help="輸出模型路徑（可自訂）")
    parser.add_argument("--episodes", type=int, default=900, help="訓練回合數")
    return parser.parse_args()

def main():
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else Path(
        f"data/models/ql_{datetime.now().strftime('%H%M%S')}.pkl"
    )

    # 載入資料
    print(f"📥 讀取訓練資料：{input_path}")
    df = pd.read_csv(input_path)

    # 初始化 QLearner 並訓練
    learner = QLearner()
    print(f"🎯 開始訓練（{args.episodes} 回合）...")
    learner.train(df, episodes=args.episodes)

    # 儲存結果
    output_path.parent.mkdir(exist_ok=True)
    learner.save(output_path)
    print(f"✅ 模型已儲存至：{output_path}")

if __name__ == "__main__":
    main()

