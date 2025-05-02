from PySide6.QtWidgets import (
    QWidget, QLabel, QSpinBox, QHBoxLayout, QVBoxLayout,
    QPushButton, QComboBox
)
from PySide6.QtCore import QDateTime
from ui.components.hotkey_manager import register_hotkeys
from datetime import datetime
from data.global_data import Session
from data.global_data import CONFIG
from data.global_data import DATA_FACADE



class InputPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.car_names = list(CONFIG["bet_vector"]["cars"].values())
        self.df = Session.get("game_log")
        self.bets = []
        self.current_step = 20
        self.current_round = len(self.df) + 1

        self.round_label = QLabel(f"🎯 目前回合數：{self.current_round}")
        self.winner_selector = QComboBox()

        self.setup_ui()
        register_hotkeys(self, {
            "increase": self.increase_bet,
            "decrease": self.decrease_bet,
            "clear": self.clear_bets,
            "submit":self.submit_bet,
            "winner_select": self.select_winner,
        })
        self.installEventFilter(self)

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.round_label)
        main_layout.addLayout(self.create_bet_inputs())
        main_layout.addLayout(self.create_controls())
        self.setLayout(main_layout)
            # 🔽 加上儲存按鈕
        save_button = QPushButton("儲存資料")
        save_button.clicked.connect(self.submit_bet)
        main_layout.addWidget(save_button)
    def create_bet_inputs(self):
        layout = QHBoxLayout()
        for _, name in CONFIG["bet_vector"]["cars"].items():
            vbox = QVBoxLayout()
            vbox.addWidget(QLabel(name))
            spin = QSpinBox()
            spin.setRange(0, 100000)
            spin.setSingleStep(self.current_step)
            self.bets.append(spin)
            vbox.addWidget(spin)
            layout.addLayout(vbox)
        return layout
    def create_controls(self):
        layout = QHBoxLayout()

        # 單位按鈕
        button_layout = QHBoxLayout()
        for amount in [20, 100, 500, 1000, 5000]:
            btn = QPushButton(f"單位：{amount}")
            btn.clicked.connect(lambda _, a=amount: self.set_bet_step(a))
            button_layout.addWidget(btn)

        # 勝出車輛選擇器
        winner_layout = QVBoxLayout()
        winner_layout.addWidget(QLabel("勝出的車"))
        for name in self.car_names:
            self.winner_selector.addItem(name)
        self.winner_selector.setCurrentIndex(0)
        winner_layout.addWidget(self.winner_selector)

        layout.addLayout(button_layout)
        layout.addLayout(winner_layout)
        return layout
    def select_winner(self, index):
        if 0 <= index < self.winner_selector.count():
            self.winner_selector.setCurrentIndex(index)
            print(f"🎯 勝者切換為：{self.car_names[index]}")


    def set_bet_step(self, step):
        pass 
        """設定所有 SpinBox 的加減單位"""
        self.current_step = step
        for spin in self.bets:
            spin.setSingleStep(step)
        print(f"🎯 已設定下注單位為：{step}")

    def next_round(self):
        pass 
        """送出資料後回合數自動 +1"""
        self.current_round += 1
        self.round_label.setText(f"🎯 目前回合數：{self.current_round}")

    def get_input_data(self):
        pass 
        time_now = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        bets = [spin.value() for spin in self.bets]
        winner_index = self.car_names.index(self.winner_selector.currentText())
        return {
            "time": time_now,
            "round": self.current_round,
            "bets": bets,
            "winner": winner_index
        }
    def increase_bet(self, index):
        pass 
        if 0 <= index < len(self.bets):
            self.bets[index].setValue(self.bets[index].value() + self.current_step)

    def decrease_bet(self, index):
        pass 
        if 0 <= index < len(self.bets):
            self.bets[index].setValue(max(0, self.bets[index].value() - self.current_step))

    def clear_bets(self):
        for spin in self.bets:
            spin.setValue(0)
        print("🧹 已清除所有下注")
    def submit_bet(self):
        """提交下注資料，儲存到 DataManager，並自動進入下一回合"""
        data = self.get_input_data()
        new_entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'round': data["round"],
            'bet': data["bets"],  # 下注100在第1台車
            'winner': data["winner"],
            }
        DATA_FACADE.append_game_log(new_entry)
        self.next_round()








