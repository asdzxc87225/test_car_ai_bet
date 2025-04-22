from data.config_loader import load_config
from data.data_facade import DataFacade
from data.Analytics_page.behavior_analyzer import BehaviorAnalyzer
from data.Analytics_page.behavior_plotter import plot_state_reward_heatmap
import matplotlib.pyplot as plt

df = DataFacade().get_game_log()
print(df.head())
config = load_config()

analyzer = BehaviorAnalyzer(df, config)
profit_df = analyzer.calc_profit_win_rate()
print(profit_df.head())

fig = plot_state_reward_heatmap(profit_df)
fig.show()
plt.show()

