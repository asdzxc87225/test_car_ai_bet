from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QSpinBox, QGroupBox,
    QSizePolicy
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = [
    'Noto Serif CJK JP',
    '0xProto Nerd Font Mono',
]

from stats.stats_controller import StatsController
from data.global_data import Session


class BehaviorTab(QWidget):
    def __init__(self):
        super().__init__()

        # 資料設定區塊
        self.data_group = QGroupBox("資料設定")
        data_layout = QHBoxLayout()

        self.file_selector = QComboBox()
        self.file_selector.addItem("game_log.csv")
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

        # 分析按鈕區
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

        # 圖表顯示區
        self.chart_group = QGroupBox("分析結果")
        chart_layout = QVBoxLayout()
        self.canvas = FigureCanvas(Figure(figsize=(6, 4)))
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.setMinimumHeight(350)
        self.ax = self.canvas.figure.add_subplot(111)
        chart_layout.addWidget(self.canvas)
        self.chart_group.setLayout(chart_layout)

        # 組合整體畫面
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.data_group)
        main_layout.addWidget(self.action_group)
        main_layout.addWidget(self.chart_group)
        self.setLayout(main_layout)

        # 綁定事件
        self.load_button.clicked.connect(self.load_and_prepare)
        self.btn_win_rate.clicked.connect(self.plot_win_rate)
        self.btn_roi.clicked.connect(self.plot_roi)
        self.btn_bet_dist.clicked.connect(self.plot_bet_dist)
        self.btn_state_heat.clicked.connect(self.plot_state_heat)

    def load_and_prepare(self):
        try:
            df = Session.get("game_log")
            max_round = int(df["round"].max())
            self.start_round.setMaximum(max_round)
            self.end_round.setMaximum(max_round)
            print(f"✅ 資料載入成功，最大回合數：{max_round}")
        except Exception as e:
            print(f"❌ 載入資料失敗：{e}")

    def _run_analysis(self, metric_name: str):
        df = Session.get("game_log")
        if df is None or df.empty:
            print("⚠️ 尚未載入資料")
            return None, {"status": "error", "msg": "資料未載入"}

        # 篩選回合範圍
        start = self.start_round.value()
        end = self.end_round.value()
        if start > 0 or end > 0:
            df = df[(df["round"] >= start) & (df["round"] <= (end if end > 0 else df["round"].max()))]

        try:
            result = StatsController.run_by_name(metric_name, df)
            return result.get("fig"), result.get("meta", {})
        except Exception as e:
            return None, {"status": "error", "msg": str(e)}

    def plot_win_rate(self):
        self.ax.clear()
        fig, meta = self._run_analysis("win_rate_by_type")
        self._handle_plot_result(fig, meta)

    def plot_roi(self):
        self.ax.clear()
        fig, meta = self._run_analysis("roi_curve")
        self._handle_plot_result(fig, meta)

    def plot_bet_dist(self):
        self.ax.clear()
        fig, meta = self._run_analysis("bet_distribution")
        self._handle_plot_result(fig, meta)

    def plot_state_heat(self):
        self.ax.clear()
        fig, meta = self._run_analysis("state_heatmap")  # YAML 中需要設這項目
        self._handle_plot_result(fig, meta)

    def _handle_plot_result(self, fig, meta):
        if meta.get("status") == "ok" and fig:
            self._render_figure(fig)
        else:
            print(f"❌ 分析失敗：{meta.get('msg')}")


    def _render_figure(self, fig):
        self.chart_layout.removeWidget(self.canvas)
        self.canvas.setParent(None)
        self.canvas = FigureCanvas(fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.setMinimumHeight(350)
        self.chart_layout.addWidget(self.canvas)
        self.canvas.draw()
        self.canvas.updateGeometry()
        self.chart_layout.activate()

