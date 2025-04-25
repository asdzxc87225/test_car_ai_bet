# agent/trainer.py
from pathlib import Path
import pandas as pd
import numpy as np
import pickle
from collections import defaultdict

class QLearner:
    def __init__(self, epsilon=0.9, alpha=0.1, gamma=0.95):
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.q_table = {}  # Q-table 初始化為空字典

        # 用於績效評估
        self.total_reward = 0
        self.max_drawdown = 0
        self.roi = 0.0
        self.hit_rate = 0.0

    def train(self, df, episodes=1000, on_step=None):
        total_hit = 0
        total_bet = 0
        max_reward = 0
        current_reward = 0
        import threading
        print(f"[QLearner.train] 執行緒：{threading.current_thread().name}")

        for i in range(episodes):
            for idx, row in df.iterrows():
                state = self._get_state(row)
                action = self._choose_action(state)
                reward = self._get_reward(row, action)
                next_state = self._get_state(row, next_step=True)

                # 更新 Q 值
                self._update_q_value(state, action, reward, next_state)

                # 統計績效
                current_reward += reward
                total_bet += 1
                if reward > 0:
                    total_hit += 1

                max_reward = max(max_reward, current_reward)
                self.max_drawdown = max(self.max_drawdown, max_reward - current_reward)

            # 每 N 輪輸出進度
            if on_step and i % 100 == 0:
                on_step(f"第 {i} 輪訓練中... 總獎勵：{current_reward}")

        # 訓練完成後的指標記錄
        self.total_reward = current_reward
        self.roi = current_reward / total_bet if total_bet else 0
        self.hit_rate = total_hit / total_bet if total_bet else 0

        if on_step:
            on_step("✅ 訓練完成")

    def _get_state(self, row, next_step=False):
        # 根據 row 產生狀態，預留 next_step=True 給需要轉移邏輯用
        return (row.get("diff", 0), row.get("rolling_sum_5", 0))

    def _choose_action(self, state):
        import random
        if state not in self.q_table:
            self.q_table[state] = [0, 0]  # 初始化動作空間（0: 不下注, 1: 下小車）

        if random.random() < self.epsilon:
            return random.choice([0, 1])
        else:
            return int(self.q_table[state][1] > self.q_table[state][0])

    def _get_reward(self, row, action):
        # 根據是否選中小車贏得報酬，這邏輯可改
        if action == 1 and row.get("wine_type", 0) == 1:
            return 1
        else:
            return -1

    def _update_q_value(self, state, action, reward, next_state):
        if next_state not in self.q_table:
            self.q_table[next_state] = [0, 0]

        predict = self.q_table[state][action]
        target = reward + self.gamma * max(self.q_table[next_state])
        self.q_table[state][action] += self.alpha * (target - predict)

    def save(self, path):
        import pickle
        with open(path, "wb") as f:
            pickle.dump(self.q_table, f)

    def load(self, path):
        import pickle
        with open(path, "rb") as f:
            self.q_table = pickle.load(f)

