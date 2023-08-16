from datetime import datetime

class Ticker:
    tag: str                        # "perpetual"
    pair: str                       # "COMP:USD"
    symbol: str                     # "pf_compusd"
    markPrice: float                # 29.705
    bid: float                      # 29.66
    bidSize: int                    # 112
    ask: float                      # 29.744
    askSize: float                  # 3.7
    vol24h: int                     # 26
    volumeQuote: float              # 751.0782
    openInterest: float             # 615.60000000000
    open24h: float                  # 28.71
    indexPrice: float               # 29.729
    last: float                     # 29.173
    lastTime: datetime              # "2023-06-21T05:02:49.789Z"
    lastSize: float                 # 8.8
    suspended: bool                 # false
    fundingRate: float              # -0.000172151152270824
    fundingRatePrediction: float    # -0.000444202863504177
    postOnly: bool                  # false


    @staticmethod
    def from_kraken(ticker) -> 'Ticker':
        t = Ticker()
        t.tag = ticker["tag"]               if "tag" in ticker.keys() else ""
        t.pair = ticker["pair"]             if "pair" in ticker.keys() else ""
        t.symbol = ticker["symbol"]         if "symbol" in ticker.keys() else ""
        t.markPrice = ticker["markPrice"]   if "markPrice" in ticker.keys() else 0
        t.bid = ticker["bid"]               if "bid" in ticker.keys() else 0
        t.bidSize = ticker["bidSize"]       if "bidSize" in ticker.keys() else 0
        t.ask = ticker["ask"]               if "ask" in ticker.keys() else 0
        t.askSize = ticker["askSize"]       if "askSize" in ticker.keys() else 0
        t.vol24h = ticker["vol24h"]             if "vol24h" in ticker.keys() else 0
        t.volumeQuote = ticker["volumeQuote"]   if "volumeQuote" in ticker.keys() else 0
        t.openInterest = ticker["openInterest"] if "openInterest" in ticker.keys() else 0
        t.open24h = ticker["open24h"]           if "open24h" in ticker.keys() else 0
        t.indexPrice = ticker["indexPrice"]     if "indexPrice" in ticker.keys() else 0
        t.last = ticker["last"]                 if "last" in ticker.keys() else 0
        t.lastTime = ticker["lastTime"]         if "lastTime" in ticker.keys() else 0
        t.lastSize = ticker["lastSize"]         if "lastSize" in ticker.keys() else 0
        t.suspended = ticker["suspended"]       if "suspended" in ticker.keys() else False
        t.fundingRate = ticker["fundingRate"]   if "fundingRate" in ticker.keys() else 0
        t.fundingRatePrediction = ticker["fundingRatePrediction"] if "fundingRatePrediction" in ticker.keys() else 0
        t.postOnly = ticker["postOnly"]         if "postOnly" in ticker.keys() else False
        return t