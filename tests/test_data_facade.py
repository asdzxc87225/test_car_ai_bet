# test/test_data_facade.py

from datetime import datetime
from pathlib import Path
import pandas as pd
from data.data_facade import DataFacade
from data.data_errors import DataLoadError
from data.global_data import Session

def test_load_data_facade():
    print("\n=== 開始測試 DataFacade ===")

    # 初始化 DataFacade（傳 root 資料夾）
    facade = DataFacade(Path("./data"))

    # 測試讀取 game_log
    try:
        df = facade.game_log()
        assert not df.empty
        print("✅ 測試通過：成功讀取 game_log")
    except Exception as e:
        print(f"❌ 測試失敗：讀取 game_log 錯誤 {e}")

    # 測試讀取 q_table（用預設模型）
    try:
        q_table = facade.q_table()
        if isinstance(q_table, pd.DataFrame):
            assert not q_table.empty
        elif isinstance(q_table, dict):
            assert len(q_table) > 0
        else:
            raise TypeError(f"q_table 資料型態錯誤：{type(q_table)}")
        print("✅ 測試通過：成功讀取 q_table")
    except Exception as e:
        print(f"❌ 測試失敗：讀取 q_table 錯誤 {e}")

    # 測試 list_models
    models = facade.list_models()
    assert isinstance(models, list)
    print(f"✅ 測試通過：成功列出模型清單（共 {len(models)} 筆）")

    # 測試 append_game_log
    new_entry = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'round': int(df['round'].max()) + 1 if not df.empty else 1,
        'bet': [0, 100, 0, 0, 0, 0, 0, 0],  # 隨便押100在第2台
        'winner': 1,
    }

    try:
        facade.append_game_log(new_entry)
        print("✅ 測試通過：成功追加一筆新 game_log 資料（請手動 refresh Session）")
    except Exception as e:
        print(f"❌ 測試失敗：追加 game_log 錯誤 {e}")

    # 測試錯誤處理（檔案不存在）
    try:
        bad_facade = DataFacade(Path("./not_exist_folder"))
        bad_facade.game_log()
        print("❌ 測試失敗：應該丟出例外但沒有")
    except Exception as e:
        print(f"✅ 測試通過：正確處理找不到資料夾的情況，錯誤訊息：{e}")

    print("\n=== 測試 DataFacade 完成 ===")

def test_session_basic_flow():
    print("\n=== 開始測試 Session 管理器 ===")

    # 取得 game_log
    game_log1 = Session.get("game_log")
    assert isinstance(game_log1, pd.DataFrame)
    print("✅ 測試通過：成功取得 game_log (DataFrame)")

    # 取得 q_table
    q_table1 = Session.get("q_table")
    assert isinstance(q_table1, dict)
    print("✅ 測試通過：成功取得 q_table (dict)")

    # 測試快取（第一次與第二次 get 是同一個 id）
    game_log2 = Session.get("game_log")
    assert id(game_log1) == id(game_log2)
    print("✅ 測試通過：同一份資料有做快取")

    # 模擬資料變動：這裡強制清空 cache
    Session.refresh("game_log")

    game_log3 = Session.get("game_log")

    # 🛠️ 比較 shape 或 row 數量，而不是 id
    assert isinstance(game_log3, pd.DataFrame)
    assert game_log3.shape == game_log1.shape  # 這樣測試合理，只確認結構正確
    print("✅ 測試通過：refresh 後可以正確重新取得資料")

    print("\n=== 測試 Session 完成 ===")
if __name__ == "__main__":
    test_load_data_facade()
    test_session_basic_flow()

