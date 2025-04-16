from PySide6.QtWidgets import QWidget, QLabel, QSpinBox, QHBoxLayout, QVBoxLayout, QSpinBox
from PySide6.QtCore import QDateTime

class InputPanel(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.bets = []

        layout = QVBoxLayout()
        self.round_input = QSpinBox()
        layout.addWidget(QLabel("回合數："))
        layout.addWidget(self.round_input)

        for i, name in self.config["bet_vector"]["cars"].items():
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(name))
            spin = QSpinBox()
            spin.setRange(0, 100)
            self.bets.append(spin)
            hbox.addWidget(spin)
            layout.addLayout(hbox)

        self.setLayout(layout)

    def get_input_data(self):
        time_now = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        bets = [spin.value() for spin in self.bets]
        return {
            "time": time_now,
            "round": self.round_input.value(),
            "bets": bets,
            "winner": ""  # 可後續新增
        }

