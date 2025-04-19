# agent/ai_action.py
from pathlib import Path
from typing import Any, Hashable
from datetime import datetime
import pandas as pd, pickle, logging

SMALL_CARS = {0, 1, 2, 3}
ACTION_MAP: dict[Hashable, int] = {
    0: 0, 1: 1,               # 已是整數的仍可映射
    "押小車": 1,
    "押大車": 0,
    }

# ---------- 工具：由 Q 值決定最佳動作 ----------
def _to_int_action(label: Hashable) -> int:
    """
    將 idxmax() 得到的欄名 label 轉成整數動作 id
    若無法對應 → 拋 TypeError
    """
    if isinstance(label, int):
        return label
    if label in ACTION_MAP:
        return ACTION_MAP[label]
    raise TypeError(f"動作欄名 {label!r} 無法轉成整數 id，請更新 ACTION_MAP")

def _action_by_row_max(df: pd.DataFrame | pd.Series) -> int:
    """
    • Series  → 直接 idxmax()，再轉整數
    • DataFrame → 每列 idxmax() → value_counts() 投票 → 轉整數
    """
    if isinstance(df, pd.Series):
        best = df.idxmax()
        return _to_int_action(best)

    votes = df.apply(lambda row: row.idxmax(), axis=1)
    best = votes.value_counts().idxmax()
    return _to_int_action(best)

class AIPredictor:
    """載模型 → 準備特徵 → 預測 → 追加真實 winner"""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.log_file = self.data_dir / "game_log.csv"
        self.model_dir = self.data_dir / "models"
        self.q_table: pd.DataFrame | None = None
        self.model_name: str | None = None

    # ---------- 公開方法 ----------
    def load_model(self, model_name: str):
        path = self.model_dir / model_name
        with path.open("rb") as fh:
            self.q_table = pickle.load(fh)
        self.model_name = model_name
        logging.debug("模型載入：%s", model_name)
        return self

    def predict(self):
        """回傳 (suggestion:int, state tuple, last5_df)"""
        if self.q_table is None:
            raise RuntimeError("請先呼叫 load_model()")

        df = self._prepare_log()
        if len(df) < 5:
            raise ValueError("game_log.csv 少於 5 筆資料")

        last5 = df.tail(5)
        print(last5)
        wine_type, diff, rsum = map(int,
                                    last5.iloc[-1][["wine_type",
                                                    "diff",
                                                    "rolling_sum_5"]])


        slice_df = self._safe_slice(diff, rsum)

        if slice_df is None or slice_df.empty:
            logging.debug("無對應狀態 (%s, %s)，fallback → 押小車", diff, rsum)
            suggestion = 1
        else:
            suggestion = _action_by_row_max(slice_df)

        state = (wine_type, diff, rsum)
        print(state)
        return suggestion, state, last5

    def append_winner(self, winner_car: int):
        """把真實勝利車號寫回 game_log.csv"""
        df = pd.read_csv(self.log_file)
        new_row = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "round": df["round"].max() + 1 if not df.empty else 1,
            "bet": "",  # 如需存下注金額可自行補
            "winner": winner_car,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(self.log_file, index=False)
        logging.debug("追加 winner=%s 至 game_log.csv", winner_car)

    # ---------- 私有方法 ----------
    def _prepare_log(self) -> pd.DataFrame:
        df = pd.read_csv(self.log_file)

        df["wine_type"] = df["winner"].apply(
            lambda x: 1 if x in SMALL_CARS else 0)
        df["diff"] = df["wine_type"].diff().fillna(0).astype(int)
        df["rolling_sum_5"] = (df["wine_type"]
                               .rolling(5).sum())
        return df

    def _safe_slice(self, diff: int, rsum: int):
        """根據層級切 slice；若不存在回 None"""
        if self.q_table is None or self.q_table.index is None:
            raise RuntimeError("請先 load_model()，且模型必須有索引")
        try:
            # --- 三層 (wine, diff, rsum) ----------------
            if self.q_table.index.nlevels == 3:
                return self.q_table.loc[(slice(None), diff, rsum)]

            # --- 兩層 (diff, rsum) ----------------------
            elif self.q_table.index.nlevels == 2:
                return self.q_table.loc[(diff, rsum)]

            # --- 單層，元素為 2‑tuple (diff, rsum) -------
            elif self.q_table.index.nlevels == 1:
                first = self.q_table.index[0]
                if isinstance(first, tuple) and len(first) == 2:
                    self.q_table.index = pd.MultiIndex.from_tuples(
                        self.q_table.index,
                        names=["diff", "rolling_sum_5"])
                    logging.debug("單層 tuple index 轉為 MultiIndex(2)")
                    return self._safe_slice(diff, rsum)
                # 若是 3‑tuple (wine, diff, rsum) 亦可擴充同理
                raise ValueError("單層索引格式無法解析為 (diff, rsum)")

            else:
                raise ValueError("Q‑table 索引層級僅支援 1, 2, 3")

        except KeyError:
            return None

