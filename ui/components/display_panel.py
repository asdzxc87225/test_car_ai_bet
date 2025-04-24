from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from data.stat_calculator import calculate_game_stats
import pandas as pd


class DisplayPanel(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        self.setLayout(layout)

    def update_stats_display(self):
        try:
            df = pd.read_csv(self.config["data_file"])
            car_names = list(self.config["bet_vector"]["cars"].values())
            html = calculate_game_stats(df, car_names)
            self.text.setHtml(html)
        except Exception as e:
            self.text.setHtml(f"❌ 統計錯誤：{e}")

    def append_text(self, text):
        self.text.append(text)
