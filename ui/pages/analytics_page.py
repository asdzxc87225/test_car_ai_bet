from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel
from ui.Analytics_page.behavior_tab import BehaviorTab
from ui.Analytics_page.transition_tab import TransitionTab
from ui.Analytics_page.q_table_tab import QTableTab



class TrainingTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🏋️‍♂️ 這裡是模型訓練紀錄頁"))
        self.setLayout(layout)

class AnalyticsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()
        self.tabs.addTab(QTableTab(), "Q 表分析")
        self.tabs.addTab(TransitionTab(), "馬可夫鏈分析")
        self.tabs.addTab(BehaviorTab(), "玩家行為分析")
        self.tabs.addTab(TrainingTab(), "模型訓練紀錄")

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)
