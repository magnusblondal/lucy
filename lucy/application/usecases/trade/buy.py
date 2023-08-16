
from ..usecase import Usecase

from lucy.application.trading.pairs_usd_pf import *
from lucy.application.trading.exchange import Exchange

class Buy(Usecase):
    def handle(self, symbol: str, qty: float):
        '''Buy a symbol'''
        s = pair_symbol(symbol)
        order = Exchange().long_market(s, qty)
        return order            
    