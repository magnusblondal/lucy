from rich import inspect

from api.app.trading.pairs_usd_pf import *
from api.app.trading.exchange import Exchange

from api.app.usecases.trade.sell import Sell
from api.app.usecases.trade.buy import Buy

from cli.views.open_order_view import OpenOrderView
import api.app.events.bus as bus

class OrderController:
    view:OpenOrderView = OpenOrderView()

    def market_order(self, symbol: str, qty: float, short: bool = False):
        '''Create a market order'''
        s = pair_symbol(symbol)
        if short:
            print(f"Short Market {s} {qty}")
            order = Exchange().short_market(s, qty)
        else:
            order = Exchange().long_market(s, qty)
            print(f"Long Market {s} {qty}")
        print(order)
    
    def buy(self, symbol: str, qty: float):
        '''Buy a symbol'''
        order = Buy().handle(symbol, qty)
        self.view.confirmation(f"Long Market '{symbol}' {qty}")
        print(order)

    def sell(self, symbol: str, qty: float):
        '''Sell a symbol'''
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
    
    def close(self, symbol: str):
        '''Close a position for a symbol'''
        s = pair_symbol(symbol)
        positions = Exchange().positions()
        pos = [p for p in positions if p.symbol == s]
        if len(pos) == 0:
            print(f"No position for {s}")
            return
        for p in pos:
            order = Exchange().close(p)
            print(order)

    def limit_order(self, symbol: str, qty: float, price: float, short: bool = False):
        '''Create a limit order'''
        s = pair_symbol(symbol)
        if short:
            print(f"Short Limit {s} {qty}")
            order = Exchange().short_lmt(s, qty, price)
        else:
            print(f"Long Limit {s} {qty}")
            order = Exchange().long_lmt(s, qty, price)
        print(order)
    
    def cancel(self, symbol: str):
        '''Cancel an order'''
        if symbol == "":
            orders = Exchange().open_orders()
            for o in orders:
                order = Exchange().cancel(o.order_id)
                print(order)
        else:
            s = pair_symbol(symbol)
            orders = Exchange().open_orders()
            for o in orders:
                if o.symbol == s:
                    order = Exchange().cancel(o.order_id)
                    print(order)
    
    def edit(self, order_id: str, qty: float, price: float):
        '''Edit an order'''
        order = Exchange().edit(qty, price, order_id=order_id)
        self.view.confirmation(f"Edit {order_id} {qty} {price}")
        print(order)
    
    def order_status(self, order_id: str):
        '''Get order status'''
        order = Exchange().order_status(order_id)
        print(order)
