
from ..usecase import Usecase
from lucy.model.symbol import Symbol
from lucy.application.trading.exchange import Exchange

class Buy(Usecase):
    def handle(self, symbol: Symbol, qty: float):
        '''Buy a symbol'''
        order = Exchange().long_market(Symbol, qty)
        return order            
    