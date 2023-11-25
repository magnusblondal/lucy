from lucy.application.trading.exchange import Exchange
from lucy.model.symbol import Symbol

from ..usecase import Usecase


class Sell(Usecase):
    def handle(self, symbol: Symbol, qty: float):
        '''Sell a symbol'''
        if qty == 0:
            positions = Exchange().positions()
            pos = [p for p in positions if p.symbol == symbol]
            if len(pos) == 0:
                return None
            for p in pos:
                order = Exchange().close(p)
                return order
        else:
            order = Exchange().short_market(symbol, qty)
            return order
