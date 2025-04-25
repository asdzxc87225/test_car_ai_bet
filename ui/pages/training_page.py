#/pages/training_page.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFormLayout, QGroupBox, QTextEdit, QMessageBox
)
from PySide6.QtCore import QThread, QTimer, QMetaObject, Qt, Q_ARG
from datetime import datetime
from controllers.model_training_controller import TrainerWorker
from core import model_logger


class TrainingPage(QWidget):
    def __init__(self):
        super().__init__()
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

    def _append_log(self, msg: str):
        QMetaObject.invokeMethod(
            self.log_display,
            "append",
            Qt.QueuedConnection,
            Q_ARG(str, f"[訓練中] {msg}")
        )

    def _on_train_clicked(self):
        try:
            import threading
            print(f"[on_train_finished] 執行緒：{threading.current_thread().name}")
            model_name = self.input_model_name.text()
            episodes = int(self.input_episodes.text())
            epsilon = float(self.input_epsilon.text())
            alpha = float(self.input_alpha.text())
            gamma = float(self.input_gamma.text())

            self.train_button.setEnabled(False)
            self.log_display.append(f"\n▶ 開始訓練 {model_name}...")
            # ✅ 建立 Worker 與 Thread（使用不易衝突的變數名）
            self.training_thread = QThread(self)
            self.training_worker = TrainerWorker(model_name, episodes, epsilon, alpha, gamma)
            self.training_worker.moveToThread(self.training_thread)

# ✅ 正確地將 worker.run 綁在 QThread 啟動上
            self.training_thread.started.connect(self.training_worker.run)

# ✅ 進度與完成訊號
            self.training_worker.progress.connect(self._append_log)
            self.training_worker.finished.connect(lambda result: self._on_train_finished_defer(result))
            self.training_worker.finished.connect(self.training_thread.quit)
            self.training_worker.finished.connect(self.training_worker.deleteLater)
            self.training_thread.finished.connect(self.training_thread.deleteLater)

# ✅ 錯誤處理
            self.training_worker.error.connect(self._on_train_finished)
            self.training_worker.error.connect(self.training_thread.quit)

# ✅ 啟動 thread（之後 Qt 自動執行 run）
            self.training_thread.start()
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"訓練失敗：{e}")

    def _on_train_finished_defer(self, result):
        QTimer.singleShot(0, lambda: self._on_train_finished(result))
    def _on_train_finished(self, result):
        self.train_button.setEnabled(True)

        model_name = self.input_model_name.text()

        record = {
            "model_name": model_name,
            "episodes": int(self.input_episodes.text()),
            "epsilon": float(self.input_epsilon.text()),
            "alpha": float(self.input_alpha.text()),
            "gamma": float(self.input_gamma.text()),
            "roi": result.get("roi", 0.0),
            "hit_rate": result.get("hit_rate", 0.0),
            "total_reward": result.get("total_reward", 0),
            "max_drawdown": result.get("max_drawdown", 0),
            "timestamp": datetime.now().isoformat()
        }

        # ✅ 用 import 進來的 model_logger，不要用 self.
        model_logger.log_model(record)

        self.log_display.append(
            f"✅ 完成訓練：ROI={record['roi']:.3f} 命中率={record['hit_rate']:.2%}\n"
        )

