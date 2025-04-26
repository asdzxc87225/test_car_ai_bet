# core/ai_action.py
from pathlib import Path
from typing import Any, Hashable
import pandas as pd
import pickle
import logging
from data.game_log_loader import load_game_log  # 🆕 我們之後會建立
from data.q_table_manager import load_q_table   # 🆕 我們之後會建立

SMALL_CARS = {0, 1, 2, 3}

ACTION_MAP: dict[Hashable, int] = {
    0: 0, 1: 1,
    "押小車": 1,
    "押大車": 0,
}

# ---------- 工具：由 Q 值決定最佳動作 ----------
def _to_int_action(label: Hashable) -> int:
    if isinstance(label, int):
        return label
    if label in ACTION_MAP:
        return ACTION_MAP[label]
    raise TypeError(f"動作欄名 {label!r} 無法轉成整數 id，請更新 ACTION_MAP")

def _action_by_row_max(df: pd.DataFrame | pd.Series) -> int:
    if isinstance(df, pd.Series):
        best = df.idxmax()
        return _to_int_action(best)

    votes = df.apply(lambda row: row.idxmax(), axis=1)
    best = votes.value_counts().idxmax()
    return _to_int_action(best)

# ---------- AI 模型：Q 表預測 ----------
class AIPredictor:
    def __init__(self, q_table: pd.DataFrame, data_facade, model_name: str = "未知模型"):
        if isinstance(q_table, dict):
            q_table = pd.DataFrame.from_dict(q_table, orient="index")
            q_table.columns = [0, 1]
        self.q_table = q_table
        self.data_facade = data_facade
        self.model_name = model_name

    def predict(self):
        """回傳 (suggestion:int, state tuple, last5_df)"""
        df = self.data_facade.get_game_log()

        last5 = df.tail(5)

        wine_type, diff, rsum = map(int, last5.iloc[-1][["wine_type", "diff", "rolling_sum_5"]])
        slice_df = self._safe_slice(diff, rsum)

        if slice_df is None or slice_df.empty:
            logging.debug("無對應狀態 (%s, %s)，fallback → 押小車", diff, rsum)
            suggestion = 1
        else:
            suggestion = _action_by_row_max(slice_df)

        state = (wine_type, diff, rsum)
        return suggestion, state, last5

    def _safe_slice(self, diff: int, rsum: int):
        if self.q_table is None or self.q_table.index is None:
            raise RuntimeError("Q 表尚未載入")

        try:
            if self.q_table.index.nlevels == 3:
                return self.q_table.loc[(slice(None), diff, rsum)]
            elif self.q_table.index.nlevels == 2:
                return self.q_table.loc[(diff, rsum)]
            elif self.q_table.index.nlevels == 1:
                first = self.q_table.index[0]
                if isinstance(first, tuple) and len(first) == 2:
                    self.q_table.index = pd.MultiIndex.from_tuples(self.q_table.index, names=["diff", "rolling_sum_5"])
                    return self._safe_slice(diff, rsum)
                raise ValueError("單層索引格式無法解析為 (diff, rsum)")
            else:
                raise ValueError("Q 表索引層級不支援")
        except KeyError:
            return None

