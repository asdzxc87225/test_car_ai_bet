from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton

from ui.input_panel import InputPanel
from ui.ai_control import Ai_Control
from ui.display_panel import DisplayPanel
from ui.hotkey_manager import register_hotkeys

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
        register_hotkeys(self, {
            "submit": self.save_data,
        })

        save_button = QPushButton("儲存資料")
        save_button.clicked.connect(self.save_data)

        #排版設定
        layout = QVBoxLayout()
        layout.addWidget(self.input_panel)
        layout.addWidget(save_button)
        layout.addWidget(self.ai_control)
        layout.addWidget(self.display_panel)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def save_data(self):
        data = self.input_panel.get_input_data()
        self.input_panel.next_round()
        self.data_manager.append(
            round_num=data["round"],
            bet=data["bets"],
            winner=data["winner"]
        )
        self.display_panel.update_stats_display()
        self.display_panel.append_text(f"資料已儲存：{data}")

