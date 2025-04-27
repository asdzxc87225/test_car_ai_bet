# data/dataset_split.py
from pathlib import Path
import pandas as pd
from data.feature_builder import build_features

def split(log_path: Path,
          train_ratio: float = 0.8,
          out_dir: Path | None = None):
    """
    讀 game_log.csv → 加特徵 → 切成 train.csv / test.csv
    回傳 (train_df, test_df)
    """
    out_dir = out_dir or log_path.parent
    df = build_features(pd.read_csv(log_path))

    cut = int(len(df) * train_ratio)
    train_df, test_df = df.iloc[:cut], df.iloc[cut:]

    train_df.to_csv(out_dir / "train.csv", index=False)
    test_df .to_csv(out_dir / "test.csv",  index=False)
    return train_df, test_df

