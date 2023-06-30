from typing import List

from rich import print
from rich.table import Table

from ..models.open_order import OpenOrder
from .view import View

class OpenOrderView(View):
    def listi(self, orders: List[OpenOrder], header: str=None) -> None:
        table = Table()
        if header:
            table.title = header

        for c in ['Symbol', 'Side', 'Gerð', 'Limit verð', 'Unfilled', 'Filled', 'order_id', 'Client order id']:
            table.add_column(f"{self.COLUMN_HEADER_COL}{c}")
            
        for o in orders:
            price  = "{:>12}".format(f"{o.limitPrice:.2f}")
            unfilled  = "{:>8}".format(f"{o.unfilledSize}")
            filled  = "{:>6}".format(f"{o.filledSize}")
            table.add_row(o.symbol, o.side, o.orderType, price, unfilled, filled, o.order_id, o.cliOrdId)

        print(table)