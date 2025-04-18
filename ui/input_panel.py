from PySide6.QtWidgets import (
    QWidget, QLabel, QSpinBox, QHBoxLayout, QVBoxLayout,
    QPushButton, QComboBox
)
from PySide6.QtCore import QDateTime
import pandas as pd
import os


class InputPanel(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.bets = []
        self.car_names = list(config["bet_vector"]["cars"].values())
        self.current_step = 20  # 初始下注單位為 20
        self.current_round = 1  # 初始回合數
        self.round_label = QLabel()  # 顯示回合數的 Label

        self.update_round_from_csv()

        main_layout = QVBoxLayout()

        # ======= 加入回合數顯示 =======
        main_layout.addWidget(self.round_label)

        bet_layout = QHBoxLayout()

        # 建立每台車的下注 SpinBox
        for i, name in self.config["bet_vector"]["cars"].items():
            car_box = QVBoxLayout()
            car_box.addWidget(QLabel(name))
            spin = QSpinBox()
            spin.setRange(0, 100000)
            spin.setSingleStep(self.current_step)
            self.bets.append(spin)
            car_box.addWidget(spin)
            bet_layout.addLayout(car_box)

        # 控制下注單位的按鈕與勝出選擇
        control_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # 建立「設定下注單位」的按鈕
        for amount in [20, 100, 500, 1000, 5000]:
            btn = QPushButton(f"單位：{amount}")
            btn.clicked.connect(lambda _, a=amount: self.set_bet_step(a))
            button_layout.addWidget(btn)

        # 勝出車輛選擇器
        winner_layout = QVBoxLayout()
        winner_layout.addWidget(QLabel("勝出的車"))
        self.winner_selector = QComboBox()
        for name in self.car_names:
            self.winner_selector.addItem(name)
        winner_layout.addWidget(self.winner_selector)

        control_layout.addLayout(button_layout)
        control_layout.addLayout(winner_layout)

        # 組合 layout
        main_layout.addLayout(bet_layout)
        main_layout.addLayout(control_layout)
        self.setLayout(main_layout)

    def update_round_from_csv(self):
        """從 CSV 檔讀取最後一筆回合數 +1"""
        file_path = os.path.join("data", "game_log.csv")
        self.current_round = 1  # 預設回合數為 1
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                if "round" in df.columns and not df.empty:
                    last_round = int(df["round"].iloc[-1])
                    self.current_round = last_round + 1
            except Exception as e:
                print("❗讀取回合數失敗：", e)

        self.round_label.setText(f"🎯 目前回合數：{self.current_round}")

    def next_round(self):
        """每次送出資料後手動呼叫此方法來自動 +1 並更新畫面"""
        self.current_round += 1
        self.round_label.setText(f"🎯 目前回合數：{self.current_round}")

    def set_bet_step(self, step):
        """設定所有 SpinBox 的加減單位"""
        self.current_step = step
        for spin in self.bets:
            spin.setSingleStep(step)
        print(f"🎯 已設定下注單位為：{step}")

    def get_input_data(self):
        time_now = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        bets = [spin.value() for spin in self.bets]
        winner_name = self.winner_selector.currentText()
        winner_index = self.car_names.index(winner_name)
        return {
            "time": time_now,
            "round": self.current_round,
            "bets": bets,
            "winner": winner_index
        }

