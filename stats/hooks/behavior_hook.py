# stats/hooks/behavior_hook.py

from data.behavior_logic import (
    calc_win_rate,
    calc_roi_curve,
    calc_bet_distribution,
    calc_state_heatmap,
)

# 提供 Dispatcher 註冊用的函式對應
win_rate = calc_win_rate
roi = calc_roi_curve
bet_distribution = calc_bet_distribution
state_heatmap = calc_state_heatmap

