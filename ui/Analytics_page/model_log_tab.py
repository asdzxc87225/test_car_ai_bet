from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QGroupBox,QPushButton
)
from PySide6.QtCore import Qt
import json
from pathlib import Path

class ModelLogTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._load_logs()

    def _init_ui(self):
        layout = QVBoxLayout()
        refresh_button = QPushButton("🔄 更新模型紀錄")
        refresh_button.clicked.connect(self._load_logs)

        layout.addWidget(refresh_button)
        layout.addWidget(self._create_table_panel())
        self.setLayout(layout)

    def _create_table_panel(self):
        group = QGroupBox("模型訓練紀錄")
        layout = QVBoxLayout()

        self.columns = [
            ("timestamp", "時間"),
            ("model_name", "模型名稱"),
            ("episodes", "Episodes"),
            ("epsilon", "ε"),
            ("alpha", "α"),
            ("gamma", "γ"),
            ("roi", "ROI"),
            ("hit_rate", "命中率"),
            ("total_reward", "總獎勵"),
            ("max_drawdown", "最大回撤")
        ]

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels([col[1] for col in self.columns])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)
        group.setLayout(layout)
        return group

    def _load_logs(self):
        log_path = Path("data/models/model_log.json")
        if not log_path.exists():
            return

        with open(log_path, "r", encoding="utf-8") as f:
            logs = json.load(f)

        self.table.setRowCount(0)
        self.table.setRowCount(len(logs))
        for row, entry in enumerate(reversed(logs)):  # 最新在最上面
            self._insert_row(row, entry)

    def _insert_row(self, row, entry):
        for col, (key, _) in enumerate(self.columns):
            val = entry.get(key, "")
            if isinstance(val, float):
                if key == "hit_rate":
                    val = f"{val:.2%}"  # 百分比格式
                else:
                    val = f"{val:.3f}"
            item = QTableWidgetItem(str(val))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, col, item)

