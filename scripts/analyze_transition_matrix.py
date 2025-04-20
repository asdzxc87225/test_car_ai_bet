import pandas as pd
from collections import defaultdict

# 讀取訓練資料
df = pd.read_csv("data/train.csv")

# 建立狀態轉移次數計數器
transition_counts = defaultdict(lambda: defaultdict(int))

# 顯示前幾筆確認狀態欄位存在
print(df[["diff", "rolling_sum_5"]].head())
# 計算狀態轉移次數
for i in range(len(df) - 1):
    s1 = (int(df.iloc[i]["diff"]), int(df.iloc[i]["rolling_sum_5"]))
    s2 = (int(df.iloc[i + 1]["diff"]), int(df.iloc[i + 1]["rolling_sum_5"]))
    transition_counts[s1][s2] += 1

# 顯示其中一個 state 的轉移情況（debug用）
some_state = list(transition_counts.keys())[0]
print(f"{some_state} 轉移到：{transition_counts[some_state]}")

