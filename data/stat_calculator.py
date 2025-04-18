# data/stat_calculator.py
import pandas as pd
import ast

def calculate_game_stats(df, car_names):
    if len(df) < 2:
        return "📭 尚無足夠資料顯示統計"

    prev_row = df.iloc[-2]
    now_row = df.iloc[-1]

    try:
        prev_bets = ast.literal_eval(prev_row["bet"])
        now_bets = ast.literal_eval(now_row["bet"])
        assert len(prev_bets) == len(now_bets) == len(car_names)
    except Exception as e:
        return f"❌ 解析下注資料失敗：{e}"

    diff = [now - prev for now, prev in zip(now_bets, prev_bets)]
    recent_df = df.tail(5)
    winner_counts = recent_df["winner"].value_counts().to_dict()
    rates = {
        car_names[i]: f"{(winner_counts.get(i, 0) / len(recent_df)) * 100:.1f}%"
        for i in range(len(car_names))
    }

    # HTML 格式排版
    table_rows = "\n".join([
        f"<tr><td>{car_names[i]}: {diff[i]:+}</td><td>{car_names[i]}: {now_bets[i]}</td><td>{car_names[i]}: {rates[car_names[i]]}</td></tr>"
        for i in range(len(car_names))
    ])
    
    html = f"""
    <h3>🧾 上場統計分析</h3>
    <p><b>🕑 上一場贏家：</b>{car_names[prev_row['winner']]}</p>
    <table border="1" cellspacing="5" cellpadding="5">
        <tr>
            <th>💥 差分</th>
            <th>📊 總額</th>
            <th>🚗 大車率 (近5場)</th>
        </tr>
        {table_rows}
    </table>
    """
    return html

