from os import wait
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QFileDialog,
    QHBoxLayout, QVBoxLayout, QMessageBox, QInputDialog,
    QComboBox
)
from ui.components.hotkey_manager import register_hotkeys
from core.ai_action import AIPredictor
from data.global_data import DATA_FACADE

MODEL_DIR = Path("data/models")
DATA_DIR = Path("data")


class Ai_Control(QWidget):
    """AI 控制面板（OOP 版）"""

    def __init__(self):
        super().__init__()
        register_hotkeys(self, {
            "ai_run": self.on_predict,
        })
        # ----------------- AI Agent -----------------
        self.data = DATA_FACADE
        self.model_list = self.data.list_models()
        self.model_name = self.model_list[0]
        print(self.model_name)
        q_table = self.data.get_q_table()
        self.agent = AIPredictor(q_table, self.data, model_name=self.model_name)

        # ----------------- Widgets ------------------
        self.btn_predict = QPushButton("AI 決策推薦")
        self.combo_model = QComboBox()
        self.combo_model.addItems(self.model_list)
        self.lbl_show = QLabel("尚未預測")


        # ----------------- Layout -------------------
        row = QHBoxLayout()
        row.addWidget(self.btn_predict)
        row.addWidget(self.combo_model)
        main = QVBoxLayout(self)
        main.addLayout(row)
        main.addWidget(self.lbl_show)
        # ----------------- Signals ------------------
        self.btn_predict.clicked.connect(self.on_predict)
        self.combo_model.currentTextChanged.connect(self.on_choose_model)

    # ==================================================
    # Slots
    # ==================================================

    def on_predict(self):
        try:
            sug, state, _ = self.agent.predict()
            sug = int(sug)
            state = tuple(int(x) for x in state)
        except Exception as e:
            QMessageBox.critical(self, "預測失敗", str(e))
            return
        txt = "小車" if sug == 1 else "大車"
        self.lbl_show.setText(
            f"AI 建議：{txt}  (state={state})\n模型：{self.agent.model_name}")

    def on_choose_model(self, fname: str):
        try:
            self.data.set_q_table(fname)
            q_table = self.data.get_q_table()
            self.agent = AIPredictor(q_table, self.data, model_name=fname)
            self.lbl_show.setText(f"✅ 已切換模型：{fname}")
        except Exception as e:
            QMessageBox.warning(self, "載入失敗", str(e))

