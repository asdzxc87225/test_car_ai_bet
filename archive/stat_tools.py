# data/stat_tools.py

import pandas as pd
import ast

def analyze_game_log(df: pd.DataFrame, car_names: list[str]) -> str:
    """
    統計最近一場資料與上一場資料的差異，計算下注差分、總額、大車出現率。
    回傳排版好的文字，供 DisplayPanel 顯示。
    """
    if len(df) < 2:
        return "📭 尚無足夠資料顯示統計"

    try:
        prev_row = df.iloc[-2]
        now_row = df.iloc[-1]

        prev_bets = ast.literal_eval(prev_row["bet"])
        now_bets = ast.literal_eval(now_row["bet"])

        if not isinstance(prev_bets, list) or not isinstance(now_bets, list):
            raise ValueError("下注資料不是列表格式")

        if len(prev_bets) != len(car_names) or len(now_bets) != len(car_names):
            raise ValueError("下注資料長度與車數不符")

    except Exception as e:
        return f"❌ 解析下注資料失敗：{e}"

    # 差分與總和
    diff = [now - prev for now, prev in zip(now_bets, prev_bets)]

    # 近五場大車出現率（假設大車為 index >= 4）
    recent_df = df.tail(5)
    winner_counts = recent_df["winner"].value_counts().to_dict()
    rates = {
        car_names[i]: f"{(winner_counts.get(i, 0) / len(recent_df)) * 100:.1f}%"
        for i in range(len(car_names))
    }

    # 排版文字，分三列顯示
    diff_text = "\n".join([f"{car_names[i]}: {value:+}" for i, value in enumerate(diff)])
    bet_text = "\n".join([f"{car_names[i]}: {value}" for i, value in enumerate(now_bets)])
    rate_text = "\n".join([f"{name}: {rate}" for name, rate in rates.items()])

    result = (
        f"🕑 上一場贏家：{car_names[prev_row['winner']]}\n\n"
        f"💥 上場下注差分：\n{diff_text}\n\n"
        f"📊 上場下注總額：\n{bet_text}\n\n"
        f"🚗 大車出現率（近5場）：\n{rate_text}"
    )

    return result

