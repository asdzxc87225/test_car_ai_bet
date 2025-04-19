from data.dataset_split import split
from pathlib import Path

train, test = split(Path("data/game_log.csv"))
print("train:", train.shape)
print("test:", test.shape)
print(train.tail(3))
