# stats/dispatcher.py

from stats.hooks import behavior_hook, entropy_hook, qtable_hook

# 註冊表：type-method → callable
DISPATCH_TABLE = {
    ("behavior", "win_rate"): behavior_hook.win_rate,
    ("behavior", "roi"): behavior_hook.roi,
    ("behavior", "bet_distribution"): behavior_hook.bet_distribution,
    ("q_table", "max_q"): qtable_hook.max_q,
    ("q_table", "q_gap"): qtable_hook.q_gap,
    ("q_table", "strategy_entropy"): qtable_hook.strategy_entropy,
    ("entropy", "entropy_histogram"): entropy_hook.entropy_histogram,
    # 如有需要再加入其他 hook
}


def get_callable(mtype: str, method: str):
    key = (mtype, method)
    if key not in DISPATCH_TABLE:
        raise ValueError(f"[Dispatcher] 未找到對應分析函式：({mtype}, {method})")
    return DISPATCH_TABLE[key]

