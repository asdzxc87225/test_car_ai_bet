from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class DisplayPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        layout = QVBoxLayout()
        layout.addWidget(self.text)
        self.setLayout(layout)

    def append_text(self, text):
        self.text.append(text)

