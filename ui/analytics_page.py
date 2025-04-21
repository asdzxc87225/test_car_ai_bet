from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AnalyticsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("📊 資料視覺化與統計分析頁（待建置）"))
        self.setLayout(layout)

