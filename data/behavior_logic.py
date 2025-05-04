# data/behavior_logic.py

import pandas as pd
from matplotlib.figure import Figure

from data.feature_builder import FeatureBuilder
from data.odds_mapper import OddsMapper
from data.reward_calculator import RewardCalculator
from data.Analytics import behavior_plotter as bp


def calc_win_rate(df: pd.DataFrame) -> dict:
    """
    計算累積勝率折線圖，並包裝回傳統一格式
    """
    try:
        df = FeatureBuilder.build_features(df)
        df = OddsMapper.attach_odds(df)
        df = RewardCalculator.attach_reward(df)

        fig: Figure = bp.plot_cumulative_win_rate(df)

        return {
            "fig": fig,
            "data": df,
            "meta": {"status": "ok", "msg": "勝率分析完成"}
        }
    except Exception as e:
        return {
            "fig": None,
            "data": None,
            "meta": {"status": "error", "msg": str(e)}
        }

def calc_roi_curve(df: pd.DataFrame) -> dict:
    """
    計算投報率折線圖，回傳統一格式
    """
    try:
        df = FeatureBuilder.build_features(df)
        df = OddsMapper.attach_odds(df)
        df = RewardCalculator.attach_reward(df)

        # 🔧 確保包含 reward 欄位
        if "reward" not in df.columns:
            raise ValueError("缺少 reward 欄位，無法計算 ROI")

        # ✅ 計算 ROI：累積獎勵除以回合數
        df["roi"] = df["reward"].cumsum() / (df.index + 1)

        fig = bp.plot_roi_line(df)

        return {
            "fig": fig,
            "data": df,
            "meta": {"status": "ok", "msg": "投報率分析完成"}
        }
    except Exception as e:
        return {
            "fig": None,
            "data": None,
            "meta": {"status": "error", "msg": str(e)}
        }

def calc_bet_distribution(df: pd.DataFrame) -> dict:
    """
    計算下注分佈圖，回傳統一格式
    """
    try:
        df = FeatureBuilder.build_features(df)
        df = OddsMapper.attach_odds(df)
        df = RewardCalculator.attach_reward(df)

        # 若無法從 CONFIG 取得標籤，可先用預設標籤
        car_labels = {
            "0": "聯結機", "1": "大卡車", "2": "特斯拉", "3": "野馬",
            "4": "保時捷", "5": "賓士大G", "6": "麥克拉倫", "7": "藍博基尼"
        }

        fig: Figure = bp.plot_bet_distribution(df, car_labels)

        return {
            "fig": fig,
            "data": df,
            "meta": {"status": "ok", "msg": "下注分佈分析完成"}
        }
    except Exception as e:
        return {
            "fig": None,
            "data": None,
            "meta": {"status": "error", "msg": str(e)}
        }


def calc_state_heatmap(df: pd.DataFrame) -> dict:
    """
    繪製 (diff, rolling_sum_5) 狀態與 reward 的熱圖
    """
    try:
        df = FeatureBuilder.build_features(df)
        df = OddsMapper.attach_odds(df)
        df = RewardCalculator.attach_reward(df)

        # ✅ 若 reward 存在，就複製為 profit 供熱圖使用
        if "reward" not in df.columns:
            raise ValueError("缺少 reward 欄位，無法計算 profit")
        df["profit"] = df["reward"]

        fig: Figure = bp.plot_state_reward_heatmap(df)

        return {
            "fig": fig,
            "data": df,
            "meta": {"status": "ok", "msg": "狀態熱圖分析完成"}
        }
    except Exception as e:
        return {
            "fig": None,
            "data": None,
            "meta": {"status": "error", "msg": str(e)}
        }


