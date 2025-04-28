from PySide6.QtWidgets import QWidget, QVBoxLayout

from ui.components.input_panel import InputPanel
#from ui.components.display_panel import DisplayPanel
from ui.pages.ai_control import Ai_Control
from data.config_loader import load_config

class BettingPage(QWidget):
    def __init__(self):
        super().__init__()
        print("ste")
        self.config = load_config()

        self.input_panel = InputPanel(self.config)
        self.ai_control = Ai_Control()
        #self.display_panel = DisplayPanel(self.config)

        layout = QVBoxLayout()
        layout.addWidget(self.input_panel)
        layout.addWidget(self.ai_control)
        #layout.addWidget(self.display_panel)
        self.setLayout(layout)


