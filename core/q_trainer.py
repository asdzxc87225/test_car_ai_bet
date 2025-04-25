# core/q_trainer.py

from agent.trainer import QLearner  # ← 依你的實際位置修改
from pathlib import Path
import pandas as pd
from data.data_facade import DataFacade

def train_model(model_name, episodes, epsilon, alpha, gamma):
    """
    執行 Q-learning 訓練，儲存模型並回傳績效
    """

    # 這邊假設你已經有某種資料
    DataF = DataFacade()
    df = DataF.get_game_log()
    learner = QLearner(epsilon=epsilon, alpha=alpha, gamma=gamma)

    learner.train(df, episodes=episodes)

    save_path = Path("data/models") / model_name
    learner.save(save_path)

    # 假設你在 learner 裡可以拿到以下績效（視你實作為主）
    return {
        "roi": learner.roi if hasattr(learner, "roi") else 0.0,
        "hit_rate": learner.hit_rate if hasattr(learner, "hit_rate") else 0.0,
        "total_reward": getattr(learner, "total_reward", 0),
        "max_drawdown": getattr(learner, "max_drawdown", 0),
    }

