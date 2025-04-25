# agent/trainer.py

import pickle
import numpy as np
from pathlib import Path
import random

class QLearner:
    def __init__(self, epsilon=0.9, alpha=0.1, gamma=0.95):
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.q_table = {}  # 統一用 dict 儲存，key=state, value=[Q(0), Q(1)]

        # 訓練紀錄
        self.total_reward = 0
        self.max_drawdown = 0
        self.roi = 0.0
        self.hit_rate = 0.0

    def _get_state(self, row):
        """由資料列建立狀態 key"""
        return (row.get('diff', 0), row.get('rolling_sum_5', 0))

    def _choose_action(self, state):
        """依照 epsilon-greedy 選擇動作"""
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0]

        q_values = self.q_table[state]
        q_diff = abs(q_values[1] - q_values[0])
        confidence = min(q_diff, 1.0)  # 將信心值壓在 [0,1]

        if np.random.rand() < self.epsilon * (1 - confidence):
            return np.random.choice([0, 1])  # 探索多一點
        else:
            return int(q_values[1] > q_values[0])  # 選擇較大 Q


    def _update_q_value(self, state, action, reward, next_state):
        """更新 Q 值"""
        if next_state not in self.q_table:
            self.q_table[next_state] = [0.0, 0.0]

        predict = self.q_table[state][action]
        target = reward + self.gamma * max(self.q_table[next_state])
        self.q_table[state][action] += self.alpha * (target - predict)

    def _get_reward(self, row, action):
        """定義獎勵"""
        return 1 if (action == 1 and row.get('wine_type', 0) == 1) else -1

    def train(self, df, episodes=1000, on_step=None):
        total_hits = 0
        total_bets = 0
        cumulative_reward = 0
        max_cum_reward = 0

        n_data = len(df)
        MAX_FAIL = 5

        for ep in range(episodes):
            start_idx = random.randint(0, n_data - 1)
            step_limit = random.randint(10, 30)
            idx = start_idx
            steps = 0
            fail_count = 0 
            while steps < step_limit and fail_count < MAX_FAIL:
                row = df.iloc[idx]
                state = self._get_state(row)
                action = self._choose_action(state)
                reward = self._get_reward(row, action)
                next_idx = (idx + 1) % n_data
                next_row = df.iloc[next_idx]
                next_state = self._get_state(next_row)

                self._update_q_value(state, action, reward, next_state)

                cumulative_reward += reward
                total_bets += 1
                if reward > 0:
                    total_hits += 1
                else:
                    fail_count += 1


                max_cum_reward = max(max_cum_reward, cumulative_reward)
                self.max_drawdown = max(self.max_drawdown, max_cum_reward - cumulative_reward)

                idx = next_idx
                steps += 1


            if on_step and ep % 100 == 0:
                on_step(f"第 {ep} 輪完成，累積獎勵 {cumulative_reward}")

        # 訓練結束統計
        self.total_reward = cumulative_reward
        self.roi = cumulative_reward / total_bets if total_bets else 0
        self.hit_rate = total_hits / total_bets if total_bets else 0

        if on_step:
            on_step("✅ 訓練完成")

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self.q_table, f)

    def load(self, path):
        with open(path, "rb") as f:
            self.q_table = pickle.load(f)

