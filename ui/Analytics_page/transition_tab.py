from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QSpinBox, QGroupBox
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from data.Analytics.transition_analyzer import TransitionAnalyzer
from data.Analytics.transition_plotter import TransitionPlotter
from data.Analytics.transition_matrix_builder import build_transition_matrix
from data.global_data import  DATA_FACADE
from data.global_data import  Session
from data.feature_builder import FeatureBuilder

class TransitionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.data_center = DATA_FACADE
        self.analyzer = None
        self.plotter = TransitionPlotter()

        # 區塊一：資料控制區
        self.data_group = QGroupBox("資料設定")
        data_layout = QHBoxLayout()

        self.file_selector = QComboBox()
        self.file_selector.addItem("game_log.csv")  # 之後可擴充自動讀取
        self.start_round = QSpinBox()
        self.end_round = QSpinBox()
        self.start_round.setPrefix("起始：")
        self.end_round.setPrefix("結束：")
        self.load_button = QPushButton("載入並分析")
        self.load_button.clicked.connect(self.load_and_analyze)

        data_layout.addWidget(QLabel("資料檔案："))
        data_layout.addWidget(self.file_selector)
        data_layout.addWidget(self.load_button)
        self.data_group.setLayout(data_layout)

         # 區塊二：分析按鈕區
        self.action_group = QGroupBox("分析項目")
        action_layout = QHBoxLayout()

        self.btn_plot_matrix = QPushButton("顯示轉移矩陣")
        self.btn_plot_freq = QPushButton("狀態出現頻率")
        self.btn_plot_entropy = QPushButton("狀態熵分佈")

        self.btn_plot_matrix.clicked.connect(self.plot_placeholder_matrix)  # 🔹 測試用 callback
        self.btn_plot_freq.clicked.connect(self.plot_placeholder_freq)
        self.btn_plot_entropy.clicked.connect(self.plot_placeholder_entropy)

        action_layout.addWidget(self.btn_plot_matrix)
        action_layout.addWidget(self.btn_plot_freq)
        action_layout.addWidget(self.btn_plot_entropy)

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
    def load_and_analyze(self):
        try:
            df_log = Session.get("game_log")  # ← 改成從 Session 拿
            features = FeatureBuilder.build_features(df_log)  # 2. 做特徵工程
            df_matrix = build_transition_matrix(features)  # 3. 再建轉移矩陣
            self.analyzer = TransitionAnalyzer(df_matrix)
            self.plotter = TransitionPlotter()
            print("✅ Transition matrix loaded.")
        except Exception as e:
            print(f"❌ 讀取轉移矩陣失敗：{e}")

    def plot_placeholder_matrix(self):
        if not self.analyzer:
            print("⚠️ 尚未載入資料")
            return
        df = self.analyzer.get_matrix()
        fig = self.plotter.plot_transition_matrix(df)
        self._render_figure(fig)

    def plot_placeholder_freq(self):
        if not self.analyzer:
            print("⚠️ 尚未載入資料")
            return
        df_freq = self.analyzer.calc_frequency()
        fig = self.plotter.plot_frequency_matrix(df_freq)
        self._render_figure(fig)

    def plot_placeholder_entropy(self):
        if not self.analyzer:
            print("⚠️ 尚未載入資料")
            return
        df_entropy = self.analyzer.calc_entropy()
        fig = self.plotter.plot_entropy_bar(df_entropy)
        self._render_figure(fig)


    def _render_figure(self, fig):
        self.canvas.figure.clf()
            # 移除原本的畫布元件
        self.chart_group.layout().removeWidget(self.canvas)
        self.canvas.setParent(None)

        # 用新圖建立新的畫布
        self.canvas = FigureCanvas(fig)
        self.canvas.draw()
        self.chart_group.layout().addWidget(self.canvas)


