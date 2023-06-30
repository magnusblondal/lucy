from dataclasses_json import dataclass_json
from dataclasses import dataclass
from datetime import datetime

from typing import List
@dataclass_json
@dataclass
class Position:
    side: str               #"short",
    symbol: str             #"pf_atomusd",
    price: float              #13.311,
    fillTime: str               #"2023-03-14T19:58:27.996Z",
    size: float               #30,
    unrealizedFunding: float              #5.231501383548871E-4,
    pnlCurrency: str                #"USD"
    
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
    
    def is_short(self):
        return self.side == 'short'