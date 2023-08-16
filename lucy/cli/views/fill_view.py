from rich import print
# from rich import inspect
# from rich.panel import Panel
from rich.table import Table
from lucy.application.trading.feeds.fills import Fill, Fills

from .view import View

class FillsView(View):
    def summary(self, fills: Fills, indents:int = 0, verbose: bool = False) -> None:
        print(self.indent(f"Fills: {len(fills)}", indents))

    def lines(self, fills: Fills, indents:int = 0, verbose:bool = False) -> None:
        self.summary(fills, indents, verbose)
        for f in fills:
            id = self.dim('id:', f.id)
            order_id = self.dim('order id:', f.order_id)
            cli_ord_id = self.dim('cli id:', f.cli_ord_id)
            position_id = self.dim('pos id:', str(f.position_id))
            instrument = self.dim(f.instrument)

            verb = f"{instrument} {id} {order_id} {cli_ord_id} {position_id}"

            price = self.dim('price:', self.left_pad(f"{f.price:.3f}", 6))
            buy = "Buy " if f.buy else 'Sell'
            qty = self.dim('qty', str(f.qty))
            remaining = self.dim('remaining:' , str(f.remaining_order_qty))
            fill_type = self.dim('fill type:', f.fill_type)
            fee = f"{f.fee_paid} {f.fee_currency}"
            fee = self.dim('fee: ', fee)
            taker_order_type = self.dim('taker order type:', f.taker_order_type)
            order_type = self.dim('order type:', f.order_type)
            p = f"{price} {buy} {qty} {remaining} {fill_type} {fee} {taker_order_type} {order_type}  {f.time}"
            print(self.indent(p, indents + 1))
            if verbose:
                print(self.indent(verb, indents + 2))

    def line(self, fill: Fill, indents:int = 0, verbose:bool = False, prefix: str = '') -> None:
        prefix = f"{prefix} " if prefix else ""
        id = self.dim('id:', fill.id)
        order_id = self.dim('order id:', fill.order_id)
        cli_ord_id = self.dim('cli id:', fill.cli_ord_id)
        position_id = self.dim('pos id:', str(fill.position_id))
        instrument = self.dim(fill.instrument)

        verb = f"{instrument} {id} {order_id} {cli_ord_id} {position_id}"

        price = self.dim('price:', self.left_pad(f"{fill.price:.3f}", 6))
        buy = "Buy " if fill.buy else 'Sell'
        qty = self.dim('qty', str(fill.qty))
        remaining = self.dim('remaining:' , str(fill.remaining_order_qty))
        fill_type = self.dim('fill type:', fill.fill_type)
        fee = f"{fill.fee_paid} {fill.fee_currency}"
        fee = self.dim('fee: ', fee)
        taker_order_type = self.dim('taker order type:', fill.taker_order_type)
        order_type = self.dim('order type:', fill.order_type)
        p = f"{prefix} {buy} {qty} {price} {remaining} {fill_type} {fee} {taker_order_type} {order_type}  {fill.time}"
        print(self.indent(p, indents + 1))
        if verbose:
            print(self.indent(verb, indents + 2))