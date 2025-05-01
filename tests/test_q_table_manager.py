import pytest
import pandas as pd
from core.q_table_manager import QTableManager

def test_init_q_table():
    manager = QTableManager()
    states = [(0, 0), (0, 1), (1, 0)]
    df = manager.init_q_table(states, 2)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (3, 2)
    assert df.index.names == ["diff", "rsum"]
    assert all(col in df.columns for col in [0, 1])
    assert (df.values == 0.0).all()

def test_init_q_table_from_range():
    manager = QTableManager()
    df = manager.init_q_table_from_range(range(2), range(3), 2)

    assert df.shape == (6, 2)  # 2 x 3 狀態組合
    assert df.index.names == ["diff", "rsum"]
    assert (df.values == 0.0).all()

def test_from_dict_auto_detect_n_actions():
    q_dict = {
        (0, 0): [0.1, 0.2],
        (1, 0): [0.3, 0.4],
    }
    manager = QTableManager()
    df = manager.from_dict(q_dict)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert list(df.loc[(0, 0)]) == [0.1, 0.2]
    assert list(df.loc[(1, 0)]) == [0.3, 0.4]

def test_from_dict_empty():
    manager = QTableManager()
    with pytest.raises(ValueError):
        manager.from_dict({})

def test_multiple_q_tables_with_different_shapes():
    manager = QTableManager()

    # 第一組 Q 表：3 states, 2 actions
    states1 = [(0, 0), (0, 1), (1, 0)]
    df1 = manager.init_q_table(states1, 2)
    assert df1.shape == (3, 2)
    assert (df1.values == 0.0).all()

    # 第二組 Q 表：6 states, 3 actions
    states2 = [(x, y) for x in range(2) for y in range(3)]
    df2 = manager.init_q_table(states2, 3)
    assert df2.shape == (6, 3)
    assert (df2.values == 0.0).all()

    # 確認 q_table 內容已被更新為第二組
    assert manager.q_table.equals(df2)

    # 驗證 meta 更新正確
    assert manager.meta["n_actions"] == 3
    assert manager.meta["n_states"] == 6

def test_from_dict_multiple_variants():
    manager = QTableManager()

    q_dict_2a = {
        (0, 0): [0.5, -0.2],
        (0, 1): [0.1, 0.9],
    }
    df_2a = manager.from_dict(q_dict_2a)
    assert df_2a.shape == (2, 2)

    q_dict_3a = {
        (0, 0): [0.1, 0.2, 0.3],
        (1, 1): [-1.0, 0.0, 1.0],
    }
    df_3a = manager.from_dict(q_dict_3a)
    assert df_3a.shape == (2, 3)

    # 再次確認 from_dict 不會殘留舊內容
    assert manager.q_table.equals(df_3a)
    assert list(df_3a.columns) == [0, 1, 2]
if __name__ == "__main__":
    test_init_q_table()
    test_init_q_table_from_range()
    test_from_dict_auto_detect_n_actions()
    test_from_dict_empty()
    test_multiple_q_tables_with_different_shapes()
    test_from_dict_multiple_variants()

    print("✅ 所有測試通過！")


