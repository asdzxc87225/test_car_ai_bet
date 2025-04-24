# data/Analytics_page/q_table_plotter.py

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_heatmap(data: pd.Series, title: str, ax=None):
    """
    將 pd.Series (index: tuple(diff, rsum), value: 數值)
    畫成 2D heatmap。用於 max(Q)、Q 差值、策略分佈等。

    Args:
        data: pd.Series，index 為 (diff, rolling_sum_5) 的 tuple
        title: 圖表標題
        ax: 若提供 matplotlib.axes，會畫在上面；否則自建
    """
    if not isinstance(data.index[0], tuple) or len(data.index[0]) != 2:
        raise ValueError("資料 index 必須為 (diff, rolling_sum_5) 的 tuple")

    x_vals = sorted(set(i[0] for i in data.index))  # diff
    y_vals = sorted(set(i[1] for i in data.index))  # rolling_sum_5

    z = np.full((len(y_vals), len(x_vals)), np.nan)

    for (x, y), val in data.items():
        xi = x_vals.index(x)
        yi = y_vals.index(y)
        z[yi, xi] = val

    if ax is None:
        fig, ax = plt.subplots()

    cmap = "viridis" if data.dtype != "int" else "coolwarm"
    c = ax.imshow(z, origin="lower", cmap=cmap, aspect="auto")

    ax.set_xticks(np.arange(len(x_vals)))
    ax.set_yticks(np.arange(len(y_vals)))
    ax.set_xticklabels(x_vals)
    ax.set_yticklabels(y_vals)
    ax.set_title(title)
    ax.set_xlabel("diff")
    ax.set_ylabel("rolling_sum_5")

    #plt.colorbar(c, ax=ax)
    
    fig = ax.get_figure()
    fig.colorbar(c, ax=ax)
    return fig

