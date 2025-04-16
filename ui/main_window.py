from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from ui.input_panel import InputPanel
from ui.display_panel import DisplayPanel
from data.config_loader import load_config
from data.data_manager import DataManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.setWindowTitle("AI 賽車下注工具")

        self.config = load_config()
        self.input_panel = InputPanel(self.config)
        self.display_panel = DisplayPanel()

        save_button = QPushButton("儲存資料")
        save_button.clicked.connect(self.save_data)

        layout = QVBoxLayout()
        layout.addWidget(self.input_panel)
        layout.addWidget(self.display_panel)
        layout.addWidget(save_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def save_data(self):
        data = self.input_panel.get_input_data()
        self.data_manager.append(
            round_num=data["round"],
            bet=data["bets"],
            winner=data["winner"]
        )
        self.display_panel.append_text(f"資料已儲存：{data}")

