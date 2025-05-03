import sys
import pytest

# 若在無 GUI 環境下，跳過測試
skip_ui = not hasattr(sys, "getwindowsversion") and "linux" in sys.platform

@pytest.mark.skipif(skip_ui, reason="CI 或無 GUI 環境下無法啟動 Qt")
def test_main_window_launches():
    # 🔥 注意：import 放在函式內部
    from PySide6.QtWidgets import QApplication
    from main import MainWindow

    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.show()

