from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QSpinBox, QGroupBox,
    QFrame, QSizePolicy
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure
import matplotlib.font_manager as fm
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = [
    'Noto Serif CJK JP',
    '0xProto Nerd Font Mono',
]


from data.config_loader import load_config
from data.data_facade import DataFacade
from data.Analytics.behavior_analyzer import BehaviorAnalyzer
from data.Analytics import behavior_plotter as bp
from data.config_loader import load_config


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
        self.canvas = FigureCanvas(Figure(figsize=(6, 4)))
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.setMinimumHeight(350)
        self.ax = self.canvas.figure.add_subplot(111)
        chart_layout.addWidget(self.canvas)
        self.chart_group.setLayout(chart_layout)
        self.load_button.clicked.connect(self.load_and_analyze_data)
        self.btn_win_rate.clicked.connect(self.plot_win_rate)
        self.btn_roi.clicked.connect(self.plot_roi)
        self.btn_bet_dist.clicked.connect(self.plot_bet_dist)
        self.btn_state_heat.clicked.connect(self.plot_state_heat)

        # 組合整體版面
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.data_group)
        main_layout.addWidget(self.action_group)
        main_layout.addWidget(self.chart_group)

        self.setLayout(main_layout)
    def load_and_analyze_data(self):
        try:
            # 讀取設定與資料
            config = load_config()
            data_center = DataFacade()
            
            # TODO: 若支援多檔案可加入 self.file_selector.currentText()
            df = data_center.get_game_log()
            max_round = int(df["round"].max())
            self.start_round.setMaximum(max_round)
            self.end_round.setMaximum(max_round)

            
            # 切分資料範圍
            start = self.start_round.value()
            end = self.end_round.value()
            if start > 0 or end > 0:
                df = df[(df["round"] >= start) & (df["round"] <= end if end > 0 else df["round"].max())]

            # 執行分析
            analyzer = BehaviorAnalyzer(df, config)
            self.result_df = analyzer.calc_profit_win_rate()

            print("✅ 資料載入與分析完成，資料筆數：", len(self.result_df))

        except Exception as e:
            print(f"❌ 載入與分析資料失敗：{e}")
    def plot_win_rate(self):
        if self.result_df is None:
            print("⚠️ 尚未載入資料")
            return
        self.ax.clear()
        fig = bp.plot_cumulative_win_rate(self.result_df)
        self._render_figure(fig)

    def plot_roi(self):
        if self.result_df is None:
            print("⚠️ 尚未載入資料")
            return
        self.ax.clear()
        fig = bp.plot_roi_line(self.result_df)
        self._render_figure(fig)

    def plot_bet_dist(self):
        if self.result_df is None:
            print("⚠️ 尚未載入資料")
            return
        self.ax.clear()
        config = load_config()
        fig = bp.plot_bet_distribution(self.result_df, car_labels=config["bet_vector"]["cars"])
        self._render_figure(fig)

    def plot_state_heat(self):
        if self.result_df is None:
            print("⚠️ 尚未載入資料")
            return
        self.ax.clear()
        fig = bp.plot_state_reward_heatmap(self.result_df)

        # ✅ 檢查是否需要 legend
        handles, labels = fig.axes[0].get_legend_handles_labels()
        if not handles:
            fig.axes[0].legend_.remove() if fig.axes[0].legend_ else None

        self._render_figure(fig)
    def _render_figure(self, fig):
        # 🔁 1. 移除原本的畫布
        layout = self.chart_group.layout()
        layout.removeWidget(self.canvas)
        self.canvas.setParent(None)

        # ✅ 2. 建立新的畫布，指定新的 figure
        self.canvas = FigureCanvas(fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.setMinimumHeight(350)

        # ✅ 3. 加回 layout 並繪製
        layout.addWidget(self.canvas)
        self.canvas.draw()
        self.canvas.updateGeometry()
        layout.activate()
