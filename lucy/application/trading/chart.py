import pandas as pd

import matplotlib.pyplot as plt


def chart(name: str, dfc: pd.DataFrame, signals_df: list[tuple[str, pd.DataFrame]] = None):  # type: ignore
    signals_df = signals_df or []
    num_signals = len(signals_df)
    top_height = 4
    subplot_height = 2 

    num_rows = num_signals + 2
    height = top_height + (subplot_height * num_signals)
    plt.figure(figsize=(20, height))

    ax1 = plt.subplot2grid((num_rows, 1), (0, 0), rowspan=2)
    ax1.plot(dfc)    
    ax1.legend(dfc.columns)
    ax1.set_title(name)

    i = 2
    for nm, ind in signals_df:
        ax2 = plt.subplot2grid((num_rows, 1), (i, 0), rowspan=1)
        ax2.plot(ind)
        plt.title(nm)
        plt.plot(ind)
        i += 1
    plt.tight_layout()
    # plt.show()
    path = '/mnt/c/lucy_charts/'
    plt.savefig(f"{path}{name}.png")
    plt.close()
