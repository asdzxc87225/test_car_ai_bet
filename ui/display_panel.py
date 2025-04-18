from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
import pandas as pd
import ast


class DisplayPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        self.setLayout(layout)

    def append_text(self, text):
        self.text.append(text)
    def update_from_log_file(self, config):
        """
        自動讀取最新的 game_log.csv 並顯示統計資料
        """
        try:
            df = pd.read_csv(config["data_file"])
            car_names = list(config["bet_vector"]["cars"].values())
            self.update_stats_display(df, car_names)
        except Exception as e:
            self.append_text(f"❌ 無法讀取統計資料：{e}")


    def update_stats_display(self, game_log_df, car_names):
        if len(game_log_df) < 2:
            self.text.setHtml("<i>📭 尚無足夠資料顯示統計</i>")
            return

        prev_row = game_log_df.iloc[-2]
        now_row = game_log_df.iloc[-1]

        try:
            prev_bets = ast.literal_eval(prev_row["bet"])
            now_bets = ast.literal_eval(now_row["bet"])
        except Exception as e:
            self.text.setHtml(f"<b>❌ 解析下注資料失敗：</b>{e}")
            return

        diff = [now - prev for now, prev in zip(now_bets, prev_bets)]
        recent_df = game_log_df.tail(5)
        winner_counts = recent_df["winner"].value_counts().to_dict()
        rates = {
            car_names[i]: f"{(winner_counts.get(i, 0) / len(recent_df)) * 100:.1f}%" 
            for i in range(len(car_names))
        }

        # 用 HTML 表格方式左右排版
        table_rows = ""
        for i in range(len(car_names)):
            table_rows += f"""
            <tr>
                <td>{car_names[i]}: {diff[i]:+}</td>
                <td>{car_names[i]}: {now_bets[i]}</td>
                <td>{car_names[i]}: {rates[car_names[i]]}</td>
            </tr>
            """

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

        self.text.setHtml(html)
