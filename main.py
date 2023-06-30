from kraken_futures_api import FuturesApi
from decimal import Decimal
from flex import Flex, FlexCurr
import json
from cli.services.trading.exchanges.pairs_usd_pf import *
from cli.services.trading.exchange import Exchange
from views.open_order_view import OpenOrderView
from views.position_view import PositionsView
import math

path = "https://futures.kraken.com/"
public = "3EWPFVk88Cmol8hw8falnfA67Q5RAhnT8jysgfif9gnKmhf0KacIddHA"
private = "D06lgIZD5y/9z6bZL17S7SioS0zwEEQGQH0T7+kVfto1CePZbvzR7UQUoKZzBT/uWEyVy/vmwislBLfCc9/a7Ip2"

symbol = BTC # DOT



# apinn = FuturesApi(path, public)
# instruments = apinn.get_instruments()
# tickers = apinn.get_tickers()
# hist = apinn.get_history(symbol)
# market_price = apinn.get_market_price(symbol)
# get_market_executions = apinn.get_market_executions(symbol, limit=10)
# market_orders = apinn.get_market_orders(symbol, limit=10)
# ob = apinn.get_orderbook(symbol)
# print(ob)

api_priv = FuturesApi(path, public, private)
fills = api_priv.get_fills()
# print('--- Fills ---')
# print(fills)

accounts = api_priv.get_accounts()
res = json.loads(accounts)
accounts_results = res['result']
accs = res['accounts']
flex = accs['flex']
f = Flex(flex)

balance = f.balanceValue
risk_level = Decimal(10 / 100)
max_at_risk = balance * risk_level

limit_price = Decimal(11)
sl = Decimal(10.55)

diff = abs(limit_price - sl)
x = max_at_risk / diff

print(f"Balance: \t{balance:.2f}")
print(f"Risk: \t{risk_level}")
print(f"Max at risk: \t{max_at_risk}")
print(f"Limit price: \t{limit_price}")
print(f"SL: \t{sl}")

# print(f"Diff: \t{diff}")
print(f"MAX QTY: \t{math.floor(x)}")




# Enum: "market" "limit" "stop-loss" "take-profit" "stop-loss-limit" "take-profit-limit" "settle-position"
orderType = "limit"

# Enum: "buy" "sell"
type = "buy"
side = type

volume = 5
size = volume

symbol = ATOM
price = 10.1
limitPrice = price
leverage = ''

exch = Exchange()
# edit = exch.edit(7, 9, client_order_id="Hohoho3")
# print(edit)

# order = exch.long_lmt(ATOM, 6, 3, client_order_id="Hohoho5")
# sh = exch.short_lmt(ATOM, 5, 23)
# print(sh)

o = exch.long_market(ATOM, 5)
# o = exch.short_market(ATOM, 10)
print(o)

# exch.cancel_all()




# status = exch.order_status('910d02f3-5b5f-4eab-b156-06162abd41d7')
# print(status)

# cl = exch.close(positions[0])
# print(cl)

# print(order)
# exch.cancel("fe406278-a7e9-450a-8a41-3335f546497f")

# Symbols
# The system identifies cash accounts, margin accounts, futures contracts and indices through ticker symbols. 
# Please refer to the platform documentation for details on the ticker symbol syntax. The following shows some sample ticker symbols.

# Example Symbols	Description
# xbt	Bitcoin
# xrp	Ripple XRP
# fi_xbtusd	Bitcoin-Dollar Futures Margin Account
# fi_xrpusd	Ripple-Dollar Futures Margin Account
# fi_xbtusd_180615	Bitcoin-Dollar Futures, maturing at 16:00 London time on 15 June 2018
# fi_xrpusd_180615	Ripple-Dollar Futures, maturing at 16:00 London time on 15 June 2018
# fi_xrpxbt_180615	Ripple-Bitcoin Futures, maturing at 16:00 London time on 15 June 2018
# in_xbtusd	Bitcoin-Dollar Real-Time Index
# rr_xbtusd	Bitcoin-Dollar Reference Rate
# in_xrpusd	Ripple-Dollar Real-Time Index



# API URLs
# To access the HTTP API's endpoints, HTTP calls need to be sent to endpoints under:

# https://futures.kraken.com/derivatives/api/v3/
# https://futures.kraken.com/api/history/v2/
# https://futures.kraken.com/api/charts/v1/
# To subscribe to a WebSocket feed, establish a WebSocket connection to:

# wss://futures.kraken.com/ws/v1


# The servers to connect through whitelisted addresses are as follows:

# https://api.futures.kraken.com
# wss://api.futures.kraken.com
