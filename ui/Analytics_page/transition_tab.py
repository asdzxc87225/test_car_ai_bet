from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QSpinBox, QGroupBox
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
class TransitionTab(QWidget):
    def __init__(self):
        super().__init__()

        # 區塊一：資料控制區
        self.data_group = QGroupBox("資料設定")
        data_layout = QHBoxLayout()

        self.file_selector = QComboBox()
        self.file_selector.addItem("transition_matrix.csv")  # 之後可擴充自動讀取
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

        self.btn_plot_matrix = QPushButton("顯示轉移矩陣")
        self.btn_plot_matrix.clicked.connect(self.plot_placeholder_matrix)  # 🔹 測試用 callback
        action_layout.addWidget(self.btn_plot_matrix)

        self.action_group.setLayout(action_layout)

        # 區塊三：圖表顯示區（空畫布）
        self.chart_group = QGroupBox("分析結果")
        chart_layout = QVBoxLayout()
        self.canvas = FigureCanvas(Figure(figsize=(6, 4)))
        self.ax = self.canvas.figure.add_subplot(111)
        chart_layout.addWidget(self.canvas)
        self.chart_group.setLayout(chart_layout)

        # 組合整體版面
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.data_group)
        main_layout.addWidget(self.action_group)
        main_layout.addWidget(self.chart_group)

        self.setLayout(main_layout)
    def plot_placeholder_matrix(self):
        """ 測試用：畫出一個 5x5 隨機矩陣熱圖 """
        import numpy as np
        import seaborn as sns

        self.ax.clear()
        dummy_data = np.random.rand(5, 5)
        sns.heatmap(dummy_data, annot=True, fmt=".2f", ax=self.ax, cmap="YlGnBu")
        self.ax.set_title("測試熱圖 (假資料)")
        self.canvas.draw()



