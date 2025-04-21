from PySide6.QtWidgets import (
    QMainWindow, 
    QTabWidget
)

from ui.betting_page import BettingPage
from ui.analytics_page import AnalyticsPage
from ui.training_page import TrainingPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI 賽車下注工具")

        self.tabs = QTabWidget()
        self.tabs.addTab(BettingPage(), "🎮 下注頁")
        self.tabs.addTab(AnalyticsPage(), "📈 資料分析")
        self.tabs.addTab(TrainingPage(), "🧠 模型訓練")
        self.setCentralWidget(self.tabs)


        #排版設定

        '''
        layout = QVBoxLayout()
        layout.addWidget(self.input_panel)
        layout.addWidget(self.ai_control)
        layout.addWidget(self.display_panel)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        '''

