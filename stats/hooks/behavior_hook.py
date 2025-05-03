# stats/hooks/behavior_hook.py

def win_rate(df):
    import matplotlib.pyplot as plt

    try:
        result_df = df.copy()
        result_df["win"] = (result_df["bet"] == result_df["winner"]).astype(int)
        grouped = result_df.groupby("round")["win"].mean().reset_index()

        fig, ax = plt.subplots()
        grouped.plot(x="round", y="win", ax=ax)
        ax.set_title("Win Rate by Round")
        ax.set_ylabel("Win Rate")
        ax.set_xlabel("Round")

        return {
            "data": grouped,
            "fig": fig,
            "meta": {"status": "ok", "msg": "勝率分析完成"}
        }

    except Exception as e:
        return {
            "data": None,
            "fig": None,
            "meta": {"status": "error", "msg": str(e)}
        }

def roi(df):
    import matplotlib.pyplot as plt
    import numpy as np

    try:
        df = df.copy()
        df["payout"] = np.where(df["bet"] == df["winner"], df["odds"], 0)
        df["roi"] = df["payout"].cumsum() / (df.index + 1)

        fig, ax = plt.subplots()
        df["roi"].plot(ax=ax)
        ax.set_title("ROI Curve")
        ax.set_ylabel("ROI")
        ax.set_xlabel("Round")

        return {
            "data": df[["roi"]],
            "fig": fig,
            "meta": {"status": "ok", "msg": "投報率分析完成"}
        }

    except Exception as e:
        return {
            "data": None,
            "fig": None,
            "meta": {"status": "error", "msg": str(e)}
        }


def bet_distribution(df):
    import matplotlib.pyplot as plt

    try:
        bet_counts = df["bet"].value_counts().sort_index()

        fig, ax = plt.subplots()
        bet_counts.plot(kind="bar", ax=ax)
        ax.set_title("Bet Distribution")
        ax.set_xlabel("Car ID")
        ax.set_ylabel("Count")

        return {
            "data": bet_counts.reset_index().rename(columns={"index": "car", "bet": "count"}),
            "fig": fig,
            "meta": {"status": "ok", "msg": "下注分佈完成"}
        }

    except Exception as e:
        return {
            "data": None,
            "fig": None,
            "meta": {"status": "error", "msg": str(e)}
        }


