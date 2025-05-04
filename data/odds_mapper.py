# data/odds_mapper.py

import pandas as pd

class OddsMapper:
    DEFAULT_ODDS = {
        0: 5,  # 聯結機
        1: 5,  # 大卡車
        2: 5,  # 特斯拉
        3: 5,  # 野馬
        4: 10, # 保時捷
        5: 15, # 賓士大G
        6: 25, # 麥克拉倫
        7: 45, # 藍博基尼
    }

    @classmethod
    def attach_odds(cls, df: pd.DataFrame, odds_dict: dict = None) -> pd.DataFrame:
        """
        根據得獎車號對應賠率，加上 'odds' 欄位
        """
        df = df.copy()
        mapping = odds_dict or cls.DEFAULT_ODDS
        df['odds'] = df['winner'].map(mapping)
        return df

