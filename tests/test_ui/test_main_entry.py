import pytest
import sys
from PySide6.QtWidgets import QApplication

# 確保 PySide 應用可以初始化
@pytest.fixture(scope="module")
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    return app

def test_main_window_launches(app):
    """
    測試 main.py 能正常啟動主視窗而不崩潰
    """
    try:
        from main import MainWindow  # 假設你的 UI 主窗口叫這個
        window = MainWindow()
        window.show()
    except Exception as e:
        pytest.fail(f"主視窗啟動失敗：{e}")

