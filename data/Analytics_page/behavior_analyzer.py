import pandas as pd

class BehaviorAnalyzer:
    """
    玩家下注行為分析模組
    - 傳入 DataFrame 與設定檔（含賠率）
    - 提供勝率、盈虧分析功能
    """

    def __init__(self, df: pd.DataFrame, config: dict):
        self.df = df.copy()
        self.odds = {int(k): v for k, v in config["bet_vector"]["odd"].items()}

    # ======================================
    # 🧰 資料轉換工具
    # ======================================

    @staticmethod
    def parse_bet(bet) -> dict:
        """將 bet 欄位統一轉為 {int: value} 格式"""
        if isinstance(bet, str):
            bet = eval(bet)
        if isinstance(bet, list):
            return {i: v for i, v in enumerate(bet)}
        if isinstance(bet, dict):
            return {int(k): v for k, v in bet.items()}
        raise ValueError(f"無法解析下注格式: {bet}")

    # ======================================
    # 📊 分析函數：勝率
    # ======================================

    def calc_win_rate(self) -> pd.DataFrame:
        """
        計算是否押中獲勝車
        回傳欄位：round, is_win, cumulative_win_rate
        """
        results = []

        for _, row in self.df.iterrows():
            try:
                winner = int(row["winner"])
                bet_dict = self.parse_bet(row["bet"])
                is_win = int(winner in bet_dict and bet_dict[winner] > 0)
                results.append({
                    "round": row["round"],
                    "is_win": is_win
                })
            except Exception as e:
                print(f"⚠️ 解析失敗 round={row.get('round', '?')} 錯誤：{e}")
                results.append({
                    "round": row.get("round", -1),
                    "is_win": 0
                })

        result_df = pd.DataFrame(results)
        result_df["cumulative_win_rate"] = result_df["is_win"].expanding().mean()
        return result_df

    # ======================================
    # 💰 分析函數：盈虧與 ROI
    # ======================================

    def calc_profit_win_rate(self) -> pd.DataFrame:
        """
        計算每局盈虧情況與 ROI（投報率）
        只要 profit > 0 視為「贏」
        """
        results = []

        for _, row in self.df.iterrows():
            try:
                winner = int(row["winner"])
                bet_dict = self.parse_bet(row["bet"])

                total_bet = sum(bet_dict.values())
                income = bet_dict[winner] * self.odds[winner] if winner in bet_dict else 0
                profit = income - total_bet
                is_win = int(profit > 0)
                roi = income / total_bet if total_bet > 0 else 0
                results.append({
                    "round": row["round"],
                    "total_bet": total_bet,
                    "income": income,
                    "profit": profit,
                    "is_win": is_win,
                    "roi": roi,
                    "bet": row.get("bet"),  # 👈 必須補上！
                    "diff": row.get("diff"),
                    "rolling_sum_5": row.get("rolling_sum_5")
                })
           

            except Exception as e:
                print(f"⚠️ 計算失敗 round={row.get('round', '?')} 錯誤：{e}")
                results.append({
                    "round": row.get("round", -1),
                    "total_bet": 0,
                    "income": 0,
                    "profit": 0,
                    "is_win": 0,
                    "roi": 0
                })

        result_df = pd.DataFrame(results)
        result_df["cumulative_win_rate"] = result_df["is_win"].expanding().mean()
        return result_df

