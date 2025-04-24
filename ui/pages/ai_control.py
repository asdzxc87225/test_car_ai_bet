from os import wait
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QFileDialog,
    QHBoxLayout, QVBoxLayout, QMessageBox, QInputDialog
)
from core.ai_action import AIPredictor
from ui.components.hotkey_manager import register_hotkeys

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
        print(DATA_DIR)
        self.agent = AIPredictor(DATA_DIR).load_model("104900.pkl")

        # ----------------- Widgets ------------------
        self.btn_predict = QPushButton("AI 決策推薦")
        self.btn_model   = QPushButton("選擇權重")
        self.btn_commit  = QPushButton("寫入勝利車")
        self.lbl_show    = QLabel("尚未預測")

        # ----------------- Layout -------------------
        row = QHBoxLayout()
        for b in (self.btn_predict, self.btn_model, self.btn_commit):
            row.addWidget(b)
        main = QVBoxLayout(self)
        main.addLayout(row)
        main.addWidget(self.lbl_show)

        # ----------------- Signals ------------------
        self.btn_predict.clicked.connect(self.on_predict)
        self.btn_model.clicked.connect(self.on_choose_model)
        self.btn_commit.clicked.connect(self.on_commit_winner)

    # ==================================================
    # Slots
    # ==================================================
    def on_predict(self):
        try:
            sug, state, _ = self.agent.predict()
            # 轉成 Python int，避免 QLabel 顯示 numpy 型別
            sug = int(sug)
            state = tuple(int(x) for x in state)
        except Exception as e:
            QMessageBox.critical(self, "預測失敗", str(e))
            return
        txt = "小車" if sug == 1 else "大車"
        self.lbl_show.setText(
            f"AI 建議：{txt}  (state={state})\n模型：{self.agent.model_name}")

    def on_choose_model(self):
        fname, _ = QFileDialog.getOpenFileName(
            self, "選擇模型", str(MODEL_DIR), "PKL Files (*.pkl)")
        if fname:
            try:
                self.agent.load_model(Path(fname).name)
            except Exception as e:
                QMessageBox.warning(self, "載入失敗", str(e))
                return
            self.lbl_show.setText(f"已切換模型：{self.agent.model_name}")

    def on_commit_winner(self):
        car_no, ok = QInputDialog.getInt(self, "輸入勝利車號", "0–7：", 0, 0, 7, 1)
        if ok:
            try:
                self.agent.append_winner(car_no)
            except Exception as e:
                QMessageBox.warning(self, "寫入失敗", str(e))
                return
            QMessageBox.information(self, "完成", "已寫入 game_log.csv")
            self.lbl_show.setText("已追加資料，可再次預測")

