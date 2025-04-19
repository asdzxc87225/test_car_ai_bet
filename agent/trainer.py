import pandas as pd
import numpy as np
import pickle
from pathlib import Path

ACTIONS = [0, 1]  # 0: 不下注, 1: 下注

class QLearner:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.9):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = pd.DataFrame(columns=ACTIONS)

    def build_q_table(self, states):
        self.q_table = pd.DataFrame(
            0,
            index=pd.MultiIndex.from_tuples(states, names=["diff", "rolling_sum_5"]),
            columns=ACTIONS
        )
        self.q_table.sort_index(inplace=True)  # 加速搜尋效能

    def choose_action(self, state):
        if (np.random.uniform() < self.epsilon) or (state not in self.q_table.index):
            return np.random.choice(ACTIONS)
        return self.q_table.loc[state].idxmax()

    def get_reward(self, state, action, next_row):
        next_state = (int(next_row["diff"]), int(next_row["rolling_sum_5"]))
        wine_type = int(next_row["wine_type"])
        print(action)
        if action == 1:
            reward = 20 if wine_type == 1 else -80
        else:
            reward = 0
        return next_state, reward

    def train(self, df, episodes=900):
        states = list(zip(df["diff"], df["rolling_sum_5"]))
        self.build_q_table(states)

        for ep in range(episodes):
            for i in range(len(df) - 1):
                s_row = df.iloc[i]
                s_next = df.iloc[i + 1]
                state = (int(s_row["diff"]), int(s_row["rolling_sum_5"]))
                action = self.choose_action(state)
                next_state, reward = self.get_reward(state, action, s_next)

                s_diff, s_sum = state
                n_diff, n_sum = next_state

                if (n_diff, n_sum) not in self.q_table.index:
                    self.q_table.loc[(n_diff, n_sum), :] = 0.0

                predict_raw = self.q_table.loc[(s_diff, s_sum), action]
                predict = float(predict_raw.iloc[0]) if isinstance(predict_raw, pd.Series) else float(predict_raw)

                max_q_values = self.q_table.loc[(n_diff, n_sum)] if (n_diff, n_sum) in self.q_table.index else pd.Series([0.0])
                if isinstance(max_q_values, pd.DataFrame):
                    max_next = float(max_q_values.iloc[0].max())
                else:
                    max_next = float(max_q_values.max())

                target = reward + self.gamma * max_next
                new_value = predict + self.alpha * (target - predict)
                self.q_table.loc[(s_diff, s_sum), action] = float(new_value)

    def save(self, path: Path):
        with path.open("wb") as f:
            pickle.dump(self.q_table, f)

    def load(self, path: Path):
        with path.open("rb") as f:
            self.q_table = pickle.load(f)

