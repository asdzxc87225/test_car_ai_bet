# core/q_trainer.py
from core.training_strategy import TwoActionStrategy  # ⬅️ 補上 import
from pathlib import Path
from agent.trainer import QLearner
import threading
from data.global_data import Session
from data.feature_builder import FeatureBuilder

def train_model(model_name, episodes, epsilon, alpha, gamma, on_step=None, should_abort=None, save=True):
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
        should_abort (callable | None): 中途停止判斷
        save (bool): 是否儲存模型檔案

    Returns:
        dict: 訓練結果指標
    """

    # 1️⃣ 讀取資料
    df = Session.get("game_log")
    df_features = FeatureBuilder.build_features(df)
    print(df_features)
    df_features = df_features.dropna(subset=["diff", "rolling_sum_5"])

    # 2️⃣ 建立 QLearner
    learner = QLearner(
        epsilon=epsilon,
        alpha=alpha,
        gamma=gamma,
        strategy=TwoActionStrategy(),  # ✅ 注入預設策略
        )


    # 3️⃣ 開始訓練（支援進度回報與中止）
    learner.train(df_features, episodes=episodes, on_step=on_step, should_abort=should_abort)

    # 4️⃣ 訓練後判斷是否中止
    if getattr(learner, "aborted", False):
        return {
            "roi": 0.0,
            "hit_rate": 0.0,
            "total_reward": 0,
            "max_drawdown": 0,
            "status": "aborted"
        }

    # 5️⃣ 儲存模型（可關閉）
    if save:
        save_path = Path("data/models") / model_name
        learner.save(save_path)

    # 6️⃣ 回傳結果
    return extract_training_result(learner)

def extract_training_result(learner) -> dict:
    """將 QLearner 中的訓練指標統一回傳格式化"""
    return {
        "roi": getattr(learner, "roi", 0.0),
        "hit_rate": getattr(learner, "hit_rate", 0.0),
        "total_reward": getattr(learner, "total_reward", 0),
        "max_drawdown": getattr(learner, "max_drawdown", 0),
    }

