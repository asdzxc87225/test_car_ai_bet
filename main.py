# main.py
from data.data_manager import DataManager

def main():
    print("🔄 模擬單一下注紀錄流程")

    # 初始化資料管理器
    dm = DataManager()

    # 模擬一筆資料：第 1 回合下注
    round_num = 1
    bet = [0, 10, 0, 5, 0, 0, 0, 0]
    winner = 1

    # 寫入資料
    dm.append(round_num, bet, winner)

    # 顯示最新資料
    df = dm.read()
    print("\n📈 最新資料紀錄：")
    print(df.tail())

if __name__ == "__main__":
    main()

