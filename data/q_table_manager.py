import pickle
import pandas as pd
from pathlib import Path

def load_q_table(path: Path) -> pd.DataFrame:
    with open(path, "rb") as f:
        return pickle.load(f)

def save_q_table(q_table: pd.DataFrame, path: Path):
    with open(path, "wb") as f:
        pickle.dump(q_table, f)

