from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFormLayout, QGroupBox, QTextEdit, QMessageBox
)
from datetime import datetime

# 🔧 請依照實際模組路徑匯入
from core import model_logger, q_trainer

class TrainingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.q_table = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self._create_param_panel())
        layout.addWidget(self._create_log_panel())
        self.setLayout(layout)

    def _create_param_panel(self):
        group = QGroupBox("訓練參數與執行")
        layout = QFormLayout()

        self.input_model_name = QLineEdit(f"q_model_{datetime.now().strftime('%m%d_%H%M')}.pkl")
        self.input_episodes = QLineEdit("1000")
        self.input_epsilon = QLineEdit("0.9")
        self.input_alpha = QLineEdit("0.1")
        self.input_gamma = QLineEdit("0.95")

        self.train_button = QPushButton("開始訓練")
        self.train_button.clicked.connect(self._on_train_clicked)

        layout.addRow("模型名稱：", self.input_model_name)
        layout.addRow("訓練輪數：", self.input_episodes)
        layout.addRow("ε 探索率：", self.input_epsilon)
        layout.addRow("α 學習率：", self.input_alpha)
        layout.addRow("γ 折扣因子：", self.input_gamma)
        layout.addRow(self.train_button)

        group.setLayout(layout)
        return group

    def _create_log_panel(self):
        group = QGroupBox("訓練紀錄")
        layout = QVBoxLayout()

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)

        group.setLayout(layout)
        return group

    def _on_train_clicked(self):
        try:
            model_name = self.input_model_name.text()
            episodes = int(self.input_episodes.text())
            epsilon = float(self.input_epsilon.text())
            alpha = float(self.input_alpha.text())
            gamma = float(self.input_gamma.text())

            self.log_display.append(f"\n▶ 開始訓練 {model_name}...")
            stats = q_trainer.train_model(
                model_name=model_name,
                episodes=episodes,
                epsilon=epsilon,
                alpha=alpha,
                gamma=gamma
            )

            model_logger.log_model({
                "model_name": model_name,
                "episodes": episodes,
                "epsilon": epsilon,
                "alpha": alpha,
                "gamma": gamma,
                **stats
            })

            self.log_display.append(
                f"✅ 完成訓練：ROI={stats.get('roi'):.3f} 命中率={stats.get('hit_rate'):.2%}\n")

        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"訓練失敗：{e}")

