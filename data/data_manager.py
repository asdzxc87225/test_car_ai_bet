import pandas as pd
from pathlib import Path
from datetime import datetime
import ast
from .config_loader import  load_config
import os

config = load_config()
DATA_FILE = Path(config["data_file"])
COLUMNS = config["columns"]

class DataManager:
    def __init__(self):
        self.columns = COLUMNS
        self.file_path = DATA_FILE
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
    def get_next_round(self):
        if os.path.exists(self.file_path):
            try:
                df = pd.read_csv(self.file_path)
                if "round" in df.columns and not df.empty:
                    return int(df["round"].iloc[-1]) + 1
            except Exception as e:
                print("❗讀取回合數失敗：", e)
        return 1

