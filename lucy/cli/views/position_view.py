from typing import List
from rich import print
# from rich import inspect
# from rich.panel import Panel
from rich.table import Table
from ..models.position import Position

from .view import View

class PositionsView(View):
    def listi(self, positions: List[Position], header: str=None) -> None:
        table = Table()
        if header:
            table.title = header

        cols = ["Symbol", "Side", "Price", "Size", "Unrealized Funding", "PnL Curr.", "Fill Time", "Last Price", "PnL"]
        for c in cols:
            table.add_column(f"[grey54]{c}")

        for o in positions:
            price  = "{:>12}".format(f"{o.price:.2f}")
            size  = "{:>8}".format(f"{o.size}")
            unrealizedFunding  = "{:>16}".format(f"{o.unrealizedFunding:.16f}")
            last_price = "{:>12}".format(f"{o.ticker.last:.2f}")
            pnl = "{:>12}".format(f"{o.pnl():.2f}")
            table.add_row(o.symbol, o.side, price, size, unrealizedFunding, o.pnlCurrency, o.fillTime, last_price, pnl)
        print(table)
