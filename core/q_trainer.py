# core/q_trainer.py

from pathlib import Path
from data.data_facade import DataFacade
from agent.trainer import QLearner


def train_model(model_name, episodes, epsilon, alpha, gamma, on_step=None, save=True):
    import threading
    print(f"[train_model] 執行緒：{threading.current_thread().name}")
    """
    執行 Q-learning 訓練流程，支援進度回報與模型儲存。

    Args:
        model_name (str): 模型儲存檔案名稱
        episodes (int): 訓練輪數
        epsilon (float): 探索率
        alpha (float): 學習率
        gamma (float): 折扣因子
        on_step (callable | None): 每 N 輪回報的 callback
        save (bool): 是否儲存模型檔案

    Returns:
        dict: 訓練結果指標
    """

    # 1️⃣ 讀取資料
    df = DataFacade().get_game_log()

    # 2️⃣ 建立 QLearner
    learner = QLearner(epsilon=epsilon, alpha=alpha, gamma=gamma)

    # 3️⃣ 開始訓練（支援進度 callback）
    learner.train(df, episodes=episodes, on_step=on_step)

    # 4️⃣ 儲存模型（可關閉）
    if save:
        save_path = Path("data/models") / model_name
        learner.save(save_path)

    # 5️⃣ 回傳結果
    return extract_training_result(learner)


def extract_training_result(learner) -> dict:
    """將 QLearner 中的訓練指標統一回傳格式化"""
    return {
        "roi": getattr(learner, "roi", 0.0),
        "hit_rate": getattr(learner, "hit_rate", 0.0),
        "total_reward": getattr(learner, "total_reward", 0),
        "max_drawdown": getattr(learner, "max_drawdown", 0),
    }

