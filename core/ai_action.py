# core/ai_action.py
from pathlib import Path
from typing import Any, Hashable
import pandas as pd
import pickle
import logging
from data.global_data import Session
from data.feature_builder import  FeatureBuilder
from data.global_data import CONFIG
from data.global_data import DATA_FACADE
from scipy.special import softmax
import numpy as np


#from data.game_log_loader import load_game_log  # 🆕 我們之後會建立
#from data.q_table_manager import load_q_table   # 🆕 我們之後會建立

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
    def __init__(self, q_table: pd.DataFrame, model_name: str = "未知模型"):
        if isinstance(q_table, dict):
            q_table = pd.DataFrame.from_dict(q_table, orient="index")
            q_table.columns = [0, 1]
        self.q_table = q_table
        self.model_name = model_name
        self.entropy_threshold = 0.3  # 可調整參數
    def predict(self):
        """回傳 (suggestion:int, state tuple, last5_df)"""
        df = Session.get('game_log')
        df = FeatureBuilder.build_features(df)
        last5 = df.tail(5)

        wine_type, diff, rsum = map(int, last5.iloc[-1][["wine_type", "diff", "rolling_sum_5"]])
        state = (diff, rsum)
        slice_df = self._safe_slice(diff, rsum)

        if slice_df is None or slice_df.empty:
            logging.debug("無對應狀態 (%s, %s)，fallback → 押小車", diff, rsum)
            suggestion = 1
        else:
            # ---------- entropy-aware 策略 ----------
            if isinstance(slice_df, pd.Series):
                q_values = slice_df.to_numpy()
            elif isinstance(slice_df, pd.DataFrame):
                q_values = slice_df.iloc[-1].to_numpy()
            else:
                logging.warning(f"[AIPredictor] Q 值格式無法辨識：{type(slice_df)}")
                q_values = np.array([0.0, 0.0])  # 預設保守

            entropy = self._calculate_entropy(q_values)
            logging.info(f"[AIPredictor] Q值：{q_values}, entropy: {entropy:.4f}")

            if entropy > self.entropy_threshold:
                logging.info(f"高 entropy={entropy:.3f} → 保守策略：押小車")
                suggestion = 1
            else:
                suggestion = _action_by_row_max(slice_df)

        return suggestion, (wine_type, diff, rsum), last5

    def _calculate_entropy(self, q_values: list[float]) -> float:
        probs = softmax(q_values)
        return -np.sum(probs * np.log(probs + 1e-8))

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

