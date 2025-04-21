from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QSpinBox, QGroupBox, QFrame
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.rc('font', family='Noto Serif CJK JP')

class BehaviorTab(QWidget):
    def __init__(self):
        super().__init__()

        # 區塊一：資料控制區
        self.data_group = QGroupBox("資料設定")
        data_layout = QHBoxLayout()

        self.file_selector = QComboBox()
        self.file_selector.addItem("game_log.csv")  # 之後改為自動讀取
        self.start_round = QSpinBox()
        self.end_round = QSpinBox()
        self.start_round.setPrefix("起始：")
        self.end_round.setPrefix("結束：")
        self.load_button = QPushButton("載入並分析")

        data_layout.addWidget(QLabel("資料檔案："))
        data_layout.addWidget(self.file_selector)
        data_layout.addWidget(self.start_round)
        data_layout.addWidget(self.end_round)
        data_layout.addWidget(self.load_button)
        self.data_group.setLayout(data_layout)

        # 區塊二：分析按鈕區
        self.action_group = QGroupBox("分析項目")
        action_layout = QHBoxLayout()

        self.btn_win_rate = QPushButton("勝率分析")
        self.btn_roi = QPushButton("投報率分析")
        self.btn_bet_dist = QPushButton("下注分佈")
        self.btn_state_heat = QPushButton("狀態熱圖")

        action_layout.addWidget(self.btn_win_rate)
        action_layout.addWidget(self.btn_roi)
        action_layout.addWidget(self.btn_bet_dist)
        action_layout.addWidget(self.btn_state_heat)
        self.action_group.setLayout(action_layout)

        # 區塊三：圖表顯示區（空畫布）
        self.chart_group = QGroupBox("分析結果")
        chart_layout = QVBoxLayout()
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.ax = self.canvas.figure.add_subplot(111)
        chart_layout.addWidget(self.canvas)
        self.chart_group.setLayout(chart_layout)

        # 組合整體版面
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.data_group)
        main_layout.addWidget(self.action_group)
        main_layout.addWidget(self.chart_group)

        self.setLayout(main_layout)

