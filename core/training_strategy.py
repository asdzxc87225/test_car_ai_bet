from abc import ABC, abstractmethod
import numpy as np
from typing import Any

class TrainingStrategy(ABC):
    def __init__(self, n_actions: int):
        self.n_actions = n_actions

    @abstractmethod
    def choose_action(self, state: Any, q_values: list[float], epsilon: float) -> int:
        """決定動作（探索或利用）"""
        pass

    @abstractmethod
    def compute_reward(self, row: dict, action: int) -> float:
        """計算指定動作對應的獎勵"""
        pass


class TwoActionStrategy(TrainingStrategy):
    def __init__(self):
        super().__init__(n_actions=2)

    def choose_action(self, state, q_values, epsilon):
        if np.random.rand() < epsilon:
            return np.random.choice([0, 1])
        return int(np.argmax(q_values))

    def compute_reward(self, row, action: int) -> float:
        wine_type = row.get("wine_type", 0)
        if action == 1:  # 押小車
            return 20 if wine_type == 1 else -40
        else:  # 不下注 / 觀望
            return 0

