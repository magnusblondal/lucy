from datetime import datetime


def val_or_empty(prop: str, ticker) -> str:
    return ticker["prop"] if "prop" in ticker.keys() else ""


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
        t.tag = val_or_empty("tag", ticker)
        t.pair = val_or_empty("pair", ticker)
        t.symbol = val_or_empty("symbol", ticker)
        t.markPrice = val_or_empty("markPrice", ticker)
        t.bid = val_or_empty("bid", ticker)
        t.bidSize = val_or_empty("bidSize", ticker)
        t.ask = val_or_empty("ask", ticker)
        t.askSize = val_or_empty("askSize", ticker)
        t.vol24h = val_or_empty("vol24h", ticker)
        t.volumeQuote = val_or_empty("volumeQuote", ticker)
        t.openInterest = val_or_empty("openInterest", ticker)
        t.open24h = val_or_empty("open24h", ticker)
        t.indexPrice = val_or_empty("indexPrice", ticker)
        t.last = val_or_empty("last", ticker)
        t.lastTime = val_or_empty("lastTime", ticker)
        t.lastSize = val_or_empty("lastSize", ticker)
        t.suspended = val_or_empty("suspended", ticker)
        t.fundingRate = val_or_empty("fundingRate", ticker)
        t.fundingRatePrediction = val_or_empty("fundingRatePrediction", ticker)
        t.postOnly = val_or_empty("postOnly", ticker)
        return t
