#controllers/mod# controllers/model_training_controller.py
from PySide6.QtCore import QObject, Signal

class TrainerWorker(QObject):
    finished = Signal(dict)
    error = Signal(str)
    progress = Signal(str)  # ✅ 加這一行（如果還沒加）

    def __init__(self, model_name, episodes, epsilon, alpha, gamma):
        super().__init__()
        self.model_name = model_name
        self.episodes = episodes
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def run(self):
        try:
            import threading
            print(f"[run] 執行緒：{threading.current_thread().name}")
            from core.q_trainer import train_model
            result = train_model(
                self.model_name,
                self.episodes,
                self.epsilon,
                self.alpha,
                self.gamma,
                on_step=lambda msg: self.progress.emit(msg)  # ✅ 關鍵補上
            )
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
