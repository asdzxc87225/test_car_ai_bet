from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QWidget

# 每台車的快捷鍵對應編號（0~7）
KEY_CAR_MAP = {
    "1": 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
}

def register_hotkeys(widget: QWidget, handlers: dict):
    """
    註冊快捷鍵。

    handlers:
        可包含下列任意 key 對應的 callable：
        {
            "increase": Callable[[car_id], None],
            "decrease": Callable[[car_id], None],
            "clear": Callable[[], None],
            "submit": Callable[[], None],
        }
    """
    # 加注快捷鍵：Shift + 數字鍵
    if "increase" in handlers:
        for key, car_id in KEY_CAR_MAP.items():
            shortcut = QShortcut(QKeySequence(f"Shift+{key}"), widget)
            shortcut.activated.connect(lambda cid=car_id: handlers["increase"](cid))

    # 減注快捷鍵：Ctrl + 數字鍵
    if "decrease" in handlers:
        for key, car_id in KEY_CAR_MAP.items():
            shortcut = QShortcut(QKeySequence(f"Ctrl+{key}"), widget)
            shortcut.activated.connect(lambda cid=car_id: handlers["decrease"](cid))

    # 清除下注：Backspace
    if "clear" in handlers:
        QShortcut(QKeySequence("Backspace"), widget).activated.connect(handlers["clear"])

    # 儲存下注：Enter
    if "submit" in handlers:
        QShortcut(QKeySequence("Return"), widget).activated.connect(handlers["submit"])
    if "ai_run" in handlers:
        QShortcut(QKeySequence("a"), widget).activated.connect(handlers["ai_run"])

