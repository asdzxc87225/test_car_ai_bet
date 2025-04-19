from pathlib import Path
import pandas as pd
from data.feature_builder import build_features

def merge_csv_files(csv_paths: list[Path]) -> pd.DataFrame:
    print(f"🔗 合併資料檔案：{[p.name for p in csv_paths]}")
    df_all = pd.concat([pd.read_csv(p) for p in csv_paths], ignore_index=True)
    df_all["timestamp"] = pd.to_datetime(df_all["timestamp"])
    df_all.sort_values("timestamp", inplace=True)
    return df_all

def split_dataset(df: pd.DataFrame, train_ratio=0.8):
    df_feat = build_features(df)
    n = int(len(df_feat) * train_ratio)
    return df_feat.iloc[:n], df_feat.iloc[n:]

def main():
    # ✅ 你可以改成你目前的檔名
    source_files = [
        Path("data/game_log.csv"),
        Path("data/game_log1.csv")
    ]
    save_dir = Path("data")

    # 合併
    df_merged = merge_csv_files(source_files)

    # 特徵 + 分割
    train_df, test_df = split_dataset(df_merged, train_ratio=0.8)

    # 儲存
    save_dir.mkdir(exist_ok=True)
    train_df.to_csv(save_dir / "train.csv", index=False)
    test_df.to_csv(save_dir / "test.csv", index=False)

    print(f"✅ 資料處理完成，共 {len(df_merged)} 筆，已儲存：")
    print(f"  → 訓練集：{len(train_df)} 筆 ➜ data/train.csv")
    print(f"  → 測試集：{len(test_df)} 筆 ➜ data/test.csv")

if __name__ == "__main__":
    main()

