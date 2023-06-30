
from ...trading.pairs_usd_pf import *
from ...trading.exchange import Exchange

from ..usecase import Usecase

class Sell(Usecase):
    def handle(self, symbol: str, qty: float):
        '''Sell a symbol'''
        s = pair_symbol(symbol)
        if qty == 0:
            positions = Exchange().positions()
            pos = [p for p in positions if p.symbol == s]
            if len(pos) == 0:
                return None
            for p in pos:
                order = Exchange().close(p)
                return order
        else:
            order = Exchange().short_market(s, qty)
            return order

