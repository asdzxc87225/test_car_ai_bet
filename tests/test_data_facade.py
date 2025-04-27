from data.data_facade import DataFacade

def test_load_game_log():
    facade = DataFacade("data/raw/game_log.csv", "data/models/104900.pkl")
    df = facade.get_game_log()
    assert not df.empty 
    print("✅ 測試通過：成功讀取 game_log")
    q_table = facade.get_q_table()
    print("✅ 測試通過：成功讀取 q_table")
if __name__ == "__main__":
    test_load_game_log()
