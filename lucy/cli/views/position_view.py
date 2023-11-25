from typing import List
from rich import print
from rich.table import Table
from lucy.cli.views.order_view import OrderView
from lucy.model.position import Position, Positions
from lucy.model.symbol import Symbol

from .view import View


class PositionsView(View):
    def listi(self, positions: List[Position], header: str = None) -> None:
        table = Table()
        if header:
            table.title = header

        cols = ["Symbol", "Side", "Price", "Size", "Unrealized Funding",
                "PnL Curr.", "Fill Time", "Last Price", "PnL"]
        for c in cols:
            table.add_column(f"[grey54]{c}")

        for o in positions:
            price = "{:>12}".format(f"{o.price:.2f}")
            size = "{:>8}".format(f"{o.size}")
            unrealizedFunding = "{:>16}".format(f"{o.unrealizedFunding:.16f}")
            last_price = "{:>12}".format(f"{o.ticker.last:.2f}")
            pnl = "{:>12}".format(f"{o.pnl():.2f}")
            table.add_row(o.symbol, o.side, price, size, unrealizedFunding,
                          o.pnlCurrency, o.fillTime, last_price, pnl)
        print(table)

    def summary(
        self,
        positions: Positions,
        indents: int = 0,
        verbose: bool = False
    ) -> None:
        s = f"{self.emp('Positions:')} {len(positions)} {self.emp('Profit:')} ${positions.profit():.6f}"
        print(self.indent(s, indents))

    def lines(
        self,
        positions: Positions,
        indents: int = 0,
        show_signals: bool = False,
        verbose: bool = False
    ) -> None:
        self.summary(positions, indents)
        for pos in sorted(positions, key=lambda p: p.created_at):
            self.line(pos, indents, verbose)

            # --- Orders ---
            OrderView().lines(pos.orders, indents + 1, verbose, show_signals)

    def line(
        self,
        position: Position,
        indents: int = 0,
        verbose: bool = False
    ) -> None:
        open_closed = self.open_or_closed(position.is_open(), False)
        qty = self.dim('Qty:', str(position.open_qty()))
        profit = f"{self.dim('Profit:')} ${position.profit:.2f} {position.profit_pct:.2f}%"
        verb = f" {self.dim('created', str(position.created_at))}"
        verb = verb if verbose else ""
        id = self.dim(str(position.id))
        posStr = f"{open_closed} {position.symbol} {self.dim('Side:')} {position.side} {qty} {profit}  {id} {verb}"
        print(self.indent(posStr))

    def debug(
        self,
        bot: str,
        symbol: Symbol,
        positions: Positions,
        mssg: str
    ) -> None:
        bot = self.emp(bot)
        name = "{:<10}".format(bot)
        sym = "{:<10}".format(str(symbol))
        pos = "{:<2}".format(len(positions))
        opn = "{:<2}".format(positions.num_open())
        open = self.dim('Open:', opn)
        clsd = "{:<2}".format(positions.num_closed())
        closed = self.dim('Closed:', clsd)
        print(f"{name} {sym} Positions: {pos} {open} {closed} {mssg}")

