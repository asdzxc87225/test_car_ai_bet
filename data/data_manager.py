import pandas as pd
from pathlib import Path
from datetime import datetime
import ast
from .config_loader import  load_config

config = load_config()
DATA_FILE = Path(config["data_file"])
COLUMNS = config["columns"]

class DataManager:
    def __init__(self):
        self.columns = COLUMNS
        self._ensure_file()

    def _ensure_file(self):
        if not DATA_FILE.exists():
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(DATA_FILE, index=False)

    def append(self, round_num: int, bet: list, winner: int):
        df = pd.read_csv(DATA_FILE)
        new_row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "round": round_num,
            "bet": bet,
            "winner": winner
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        print("✅ 已新增資料：", new_row)

    def read(self):
        df = pd.read_csv(DATA_FILE, converters={"bet": ast.literal_eval})
        return df

