from dataclasses_json import dataclass_json
from dataclasses import dataclass
from .ticker import Ticker


@dataclass_json
@dataclass
class OpenPosition:
    side: str                   # "short",
    symbol: str                 # "pf_atomusd",
    price: float                # 13.311,
    fillTime: str               # "2023-03-14T19:58:27.996Z",
    size: float                 # 30,
    unrealizedFunding: float    # 5.231501383548871E-4,
    pnlCurrency: str            # "USD"

    def is_short(self):
        return self.side == 'short'

    def set_ticker(self, ticker: Ticker):
        self.ticker = ticker

    def ticker(self) -> Ticker:
        return self.ticker

    def pnl(self) -> float:
        sde = 1 if self.side == 'long' else -1
        return self.size * (self.ticker.last - self.price) * sde

        # "result":"success",
        # "openPositions":[
        #     {
        #         "side":"short",
        #         "symbol":"pf_atomusd",
        #         "price":13.311,
        #         "fillTime":"2023-03-14T19:58:27.996Z",
        #         "size":30,
        #         "unrealizedFunding":5.231501383548871E-4,
        #         "pnlCurrency":"USD"
        #     }
        # ],
        # "serverTime":"2023-03-14T19:58:27.996Z"

