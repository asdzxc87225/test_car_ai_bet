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
        # 修改原本快取
    old_game_log = facade.get_game_log()
    old_features = facade.get_features()

    # 模擬外部更新資料（手動 reload）
    facade.reload()

    new_game_log = facade.get_game_log()
    new_features = facade.get_features()

    # 測試 reload 是否有成功刷新資料（可以簡單用 shape 或 id 來確認）
    assert id(old_game_log) != id(new_game_log)
    assert id(old_features) != id(new_features)
    '''    print("✅ 測試通過：reload 成功刷新資料！")
    new_entry = {
        'timestamp': 000000,   # 或自己產生
        'round': 1234,
        'bet': [0, 100, 0, 0, 0, 0, 0, 0],  # 下注100在第1台車
        'winner': 1,
    }

    facade.append_game_log(new_entry)

    features = facade.get_features()
    print(features.tail())

    print("✅ 測試通過：成功追加下注資料並更新 features")
'''

if __name__ == "__main__":
    test_load_game_log()
