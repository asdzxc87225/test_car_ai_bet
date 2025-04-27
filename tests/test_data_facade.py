from data.data_facade import DataFacade

def test_load_game_log():
    facade = DataFacade("data/raw/game_log.csv", "data/models/104900.pkl")
    df = facade.get_game_log()
    assert not df.empty 
    print("✅ 測試通過：成功讀取 game_log")
    q_table = facade.get_q_table()
    print("✅ 測試通過：成功讀取 q_table")
    features = facade.get_features()
    print(features.head())

    assert 'diff' in features.columns
    assert 'rolling_sum_5' in features.columns
    assert 'wine_type' in features.columns
    print("✅ 測試通過：特徵加工正確完成！")

    # 測試 copy（試圖修改副本，看原資料有沒有被動到）
    features['test_col'] = 123
    features2 = facade.get_features()
    assert 'test_col' not in features2.columns

    print("✅ 測試通過：get_features 正常提供副本且安全！")
if __name__ == "__main__":
    test_load_game_log()
