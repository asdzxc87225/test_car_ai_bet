from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class TrainingPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("🤖 模型訓練與驗證頁（待建置）"))
        self.setLayout(layout)

