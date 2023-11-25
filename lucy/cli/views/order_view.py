from lucy.cli.views.fill_view import FillsView
from lucy.cli.views.signal_view import SignalView

from lucy.model.order import Order, Orders
from .view import View


class OrderView(View):
    def summary(
        self,
        orders: Orders,
        indents: int = 0,
        verbose: bool = False
    ) -> None:
        afp = self.dim("Avg entry price:",
                       f"{orders.avg_accumulation_fill_price():.3f}")
        acp = self.dim('Avg close price:',
                       f"{orders.avg_close_fill_price():.3f}")
        qty = self.dim('Qty:', f"{orders.total_qty()}")
        ss = f"{afp} {acp} {qty}"
        s = self.dim('Orders: ', str(len(orders)))
        mssg = f"{s} {ss}"
        print(self.indent(mssg, indents))

    def lines(
        self,
        orders: Orders,
        indents: int = 0,
        verbose: bool = False,
        show_signals: bool = False
    ) -> None:
        fillsView = FillsView()
        self.summary(orders, indents, verbose)
        for o in sorted(orders, key=lambda o: o.created_at):
            self._line(o, indents, verbose)
            for f in o.fills:
                fillsView.line(f, indents, verbose, self.dim("Fill:"))
            if show_signals:
                SignalView().line(o.signal, indents, verbose)

    def _line(self, order: Order, indents: int = 0, verbose: bool = False):
        o = order
        pric = self.left_pad(f"{o.price:.3f}", 9)
        qty = "{:<6}".format(o.qty)
        sid = self.emp(o.side.upper())
        reduce = 'Reduce only ' if o.reduce_only else ''

        typ = self.dim('type:', o.type)
        filled = self.dim('filled:', str(o.filled))
        limit_price = self.dim('limit price:', f"{o.limit_price:.2f}")

        id = self.dim(str(o.id))
        # client_id = self.dim('cli_ord_id:', o.cli_ord_id) if o.cli_ord_id else ''
        pos_id = self.dim('pos id:', str(o.position_id))
        bot_id = self.dim('bot id:', str(o.bot_id))
        exch_id = self.dim('exch id:', o.exchange_id)
        verb = f" {o.symbol} {pos_id} {bot_id} {exch_id}" if verbose else ''

        p = f"{sid} {qty} at {pric} {o.order_type} {filled}  {limit_price} {reduce}{typ}  {id}{verb}"
        print(self.indent(p, indents + 1))

