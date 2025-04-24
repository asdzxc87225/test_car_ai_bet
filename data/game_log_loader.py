from pathlib import Path
import pandas as pd

def load_game_log(csv_path: Path, *, min_rows=5) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    if len(df) < min_rows:
        raise ValueError(f"game log rows < {min_rows}")
    return df

