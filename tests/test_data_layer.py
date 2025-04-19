import pandas as pd
from data.dataset_split import split
from pathlib import Path
from data.feature_builder import build_features

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def test_feature_and_split():
    log_file = DATA_DIR / "game_log.csv"
    train, test = split(log_file, 0.8)

    # 1. 確保欄位存在
    for col in ["wine_type", "diff", "rolling_sum_5"]:
        assert col in train.columns

    # 2. rolling_sum_5 應在 0~5
    assert train["rolling_sum_5"].between(0, 5).all()

    # 3. diff 只會是 -1/0/1
    assert train["diff"].isin([-1, 0, 1]).all()

    # 4. 切分比例
    assert len(train) + len(test) == len(build_features(pd.read_csv(log_file)))

if __name__ == "__main__":
    from pathlib import Path
    log = Path(__file__).parent / "game_log.csv"
    train, test = split(log)
    print("train:", train.shape, "test:", test.shape)
    print(train.tail(3))

