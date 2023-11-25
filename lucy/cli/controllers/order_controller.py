from lucy.application.trading.exchange import Exchange
from lucy.application.usecases.trade.sell import Sell
from lucy.application.usecases.trade.buy import Buy
from lucy.cli.views.open_order_view import OpenOrderView
from lucy.model.symbol import Symbol


class OrderController:
    def __init__(self):
        self.view = OpenOrderView()

    def market_order(self, symbol: Symbol, qty: float, short: bool = False):
        '''Create a market order'''
        symbol = symbol if isinstance(symbol, Symbol) else Symbol(symbol)
        if short:
            print(f"Short Market {symbol} {qty}")
            order = Exchange().short_market(symbol, qty)
        else:
            order = Exchange().long_market(symbol, qty)
            print(f"Long Market {symbol} {qty}")
        print(order)

    def buy(self, symbol: Symbol, qty: float):
        '''Buy a symbol'''
        symbol = symbol if isinstance(symbol, Symbol) else Symbol(symbol)
        order = Buy().handle(symbol, qty)
        self.view.confirmation(f"Long Market '{symbol}' {qty}")
        print(order)

    def sell(self, symbol: Symbol, qty: float):
        '''Sell a symbol'''
        symbol = symbol if isinstance(symbol, Symbol) else Symbol(symbol)
        order = Sell().handle(symbol, qty)
        if order is None:
            self.view.warning(f"No position open for '{symbol}'")
        else:
            self.view.confirmation(f"Sell order '{symbol}' {qty}")
            print(order)

    def open_orders(self):
        '''List open orders'''
        orders = Exchange().open_orders()
        self.view.listi(orders, 'Open Orders')

    def close(self, symbol: Symbol):
        '''Close a position for a symbol'''
        symbol = symbol if isinstance(symbol, Symbol) else Symbol(symbol)
        posiions = Exchange().positions()
        pos = [p for p in positions if p.symbol == symbol]
        if len(pos) == 0:
            print(f"No position for {symbol}")
            return
        for p in pos:
            # TODO: klára
            order = Exchange().close(p)

    def limit_order(
        self,
        symbol: Symbol,
        qty: float,
        price: float,
        short: bool = False
    ):
        '''Create a limit order'''
        symbol = symbol if isinstance(symbol, Symbol) else Symbol(symbol)
        if short:
            print(f"Short Limit {symbol} {qty}")
            order = Exchange().short_lmt(symbol, qty, price)
        else:
            print(f"Long Limit {symbol} {qty}")
            order = Exchange().long_lmt(symbol, qty, price)
            # TODO: klára

    def cancel(self, symbol: Symbol = None):
        '''Cancel an order for a symbol, or all orders'''
        if not symbol:
            # cancel all orders
            orders = Exchange().open_orders()
            for o in orders:
                order = Exchange().cancel(o.order_id)
                print(order)
        else:
            symbol = symbol if isinstance(symbol, Symbol) else Symbol(symbol)
            orders = Exchange().open_orders()
            for o in orders:
                if o.symbol == symbol:
                    order = Exchange().cancel(o.order_id)
                    # print(order)

    def edit(self, order_id: str, qty: float, price: float):
        '''Edit an order'''
        order = Exchange().edit(qty, price, order_id=order_id)
        self.view.confirmation(f"Edit {order_id} {qty} {price}")
        # print(order)
        # TODO: klára

    def order_status(self, order_id: str):
        '''Get order status'''
        order = Exchange().order_status(order_id)
        # print(order)
        # TODO: klára
