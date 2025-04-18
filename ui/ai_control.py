from PySide6.QtWidgets import (
    QWidget, QLabel, QSpinBox, QHBoxLayout, QVBoxLayout,
    QPushButton, QComboBox
)
from PySide6.QtCore import QDateTime


class Ai_Control(QWidget):
    def __init__(self):
        super().__init__()
        but1 = QPushButton()
        but2 = QPushButton()
        but3 = QPushButton()
        but4 = QPushButton()
        but1.setText("開始ai決策推薦")
        but2.setText("選擇權重")
        but3.setText("開始訓練")
        but4.setText("修改參數")
        main_layout = QHBoxLayout()
        main_layout.addWidget(but1)
        main_layout.addWidget(but2)
        main_layout.addWidget(but3)
        main_layout.addWidget(but4)
        self.setLayout(main_layout)
        
