# ui/Analytics_page/q_table_tab.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QComboBox, QLineEdit, QGroupBox, QStackedWidget, QMessageBox
)
from pathlib import Path
from data.Analytics import q_table_plotter as plotter
from data.Analytics import q_table_analyzer as analyzer

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class QTableTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.q_table = None
        self.selected_model_path = None
        self._init_ui()
        self._load_model_list()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self._create_control_panel())
        layout.addWidget(self._create_option_panel())

        self.chart_area = QStackedWidget()
        self.chart_area.addWidget(QLabel("這裡會顯示圖表（尚未實作）"))
        layout.addWidget(self.chart_area)

        self.setLayout(layout)

    def _create_control_panel(self):
        group = QGroupBox("資料控制區")
        layout = QHBoxLayout()

        self.model_selector = QComboBox()
        self.model_selector.addItem("選擇模型")
        layout.addWidget(QLabel("Q-table 模型："))
        layout.addWidget(self.model_selector)


        group.setLayout(layout)
        return group

    def _create_option_panel(self):
        group = QGroupBox("分析項目")
        layout = QHBoxLayout()

        self.btn_max_q = QPushButton("max(Q)")
        self.btn_confidence = QPushButton("Q 差值")
        self.btn_strategy = QPushButton("策略分佈")

        self.btn_max_q.clicked.connect(self._on_show_max_q)
        self.btn_confidence.clicked.connect(self._on_show_confidence)
        self.btn_strategy.clicked.connect(self._on_show_strategy)

        layout.addWidget(self.btn_max_q)
        layout.addWidget(self.btn_confidence)
        layout.addWidget(self.btn_strategy)

        layout.addWidget(QLabel("信心門檻："))
        self.threshold_input = QLineEdit("0.8")
        self.threshold_input.setFixedWidth(50)
        layout.addWidget(self.threshold_input)

        group.setLayout(layout)
        return group

    def _load_model_list(self):
        model_dir = Path("data/models/")
        if not model_dir.exists():
            QMessageBox.warning(self, "錯誤", "找不到 models/ 資料夾")
            return

        self.model_selector.clear()
        self.model_selector.addItem("請選擇模型")

        for file in model_dir.glob("*.pkl"):
            self.model_selector.addItem(file.name, userData=str(file))

        self.model_selector.currentIndexChanged.connect(self._on_model_selected)

    def _on_model_selected(self, index):
        if index <= 0:
            self.selected_model_path = None
        else:
            self.selected_model_path = self.model_selector.itemData(index)
            self._on_load_clicked()  # ✅ 自動載入 Q-table！


    def _on_load_clicked(self):
        if not self.selected_model_path:
            QMessageBox.warning(self, "錯誤", "請先選擇模型")
            return
        try:
            self.q_table = analyzer.load_q_table(self.selected_model_path)
        except Exception as e:
            QMessageBox.critical(self, "讀取失敗", f"發生錯誤：{e}")

    def _on_show_max_q(self):
        if self.q_table is None or self.q_table.empty:
            self._warn_no_q_table()
            return
        data = analyzer.compute_max_q(self.q_table)
        self._show_chart(data, "Max Q")

    def _on_show_confidence(self):
        if self.q_table is None or self.q_table.empty:
            self._warn_no_q_table()
            return
        data = analyzer.compute_q_confidence(self.q_table)
        self._show_chart(data, "Q 差值")

    def _on_show_strategy(self):
        if self.q_table is None or self.q_table.empty:
            self._warn_no_q_table()
            return
        data = analyzer.compute_argmax_action(self.q_table)
        self._show_chart(data, "策略分佈")

    def _show_chart(self, data, title):
        while self.chart_area.count():
            widget = self.chart_area.widget(0)
            self.chart_area.removeWidget(widget)
            widget.deleteLater()

        fig = Figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        plotter.plot_heatmap(data, title, ax=ax)
        canvas = FigureCanvas(fig)
        self.chart_area.addWidget(canvas)
        self.chart_area.setCurrentWidget(canvas)

    def _warn_no_q_table(self):
        QMessageBox.warning(self, "錯誤", "請先載入 Q-table")
