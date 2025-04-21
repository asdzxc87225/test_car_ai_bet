from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton

from ui.input_panel import InputPanel
from ui.ai_control import Ai_Control
from ui.display_panel import DisplayPanel

from data.config_loader import load_config
from data.data_manager import DataManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI 賽車下注工具")

        self.data_manager = DataManager()
        self.config = load_config()#引入設定檔
        self.input_panel = InputPanel(self.config)#下注界面
        self.ai_control = Ai_Control()#Ai控制界面
        self.display_panel = DisplayPanel(self.config)#資料顯示界面


        #排版設定
        layout = QVBoxLayout()
        layout.addWidget(self.input_panel)
        layout.addWidget(self.ai_control)
        layout.addWidget(self.display_panel)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


