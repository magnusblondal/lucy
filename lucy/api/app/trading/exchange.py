from datetime import datetime
from enum import Enum
import json
from typing import List

from .flex import Account
from .kraken_futures_api import FuturesApi
from .open_order import OpenOrder, OrderResults, OrderEvent
from .open_position import OpenPosition
from .execution import Execution
from .ticker import Ticker
from .instrument import Instrument, Instruments

class OrderType(Enum):
    LIMIT = 'lmt'
    POST = 'post'
    MARKET = 'mkt'
    STOP = 'stp'
    TAKE_PROFIT = 'take_profit'
    IMMEDIATE_OR_CANCEL = 'ioc'

class Exchange:
    def __init__(self) -> None:
        path = "https://futures.kraken.com/"
        public = "3EWPFVk88Cmol8hw8falnfA67Q5RAhnT8jysgfif9gnKmhf0KacIddHA"
        private = "D06lgIZD5y/9z6bZL17S7SioS0zwEEQGQH0T7+kVfto1CePZbvzR7UQUoKZzBT/uWEyVy/vmwislBLfCc9/a7Ip2"
        self.api = FuturesApi(path, public, private)
    
    def long_market(self, symbol: str, size: float, client_order_id: str=None, reduce_only: bool=False) -> OrderResults:
        return self._place_market_order(symbol, 'buy', size, client_order_id, reduce_only)

    def short_market(self, symbol: str, size: float, client_order_id: str=None, reduce_only: bool=False):
        return self._place_market_order(symbol, 'sell', size, client_order_id, reduce_only)

    def long_lmt(self, symbol: str, size: float, limit_price: float, stop_price: float = None, client_order_id: str=None) -> OrderResults:
        orderType = OrderType.LIMIT if stop_price is None else OrderType.STOP
        return self._place_limit_order(symbol, 'buy', size, limit_price, client_order_id)

    def short_lmt(self, symbol: str, size: float, limit_price: float, client_order_id: str=None) -> OrderResults:
        return self._place_limit_order(symbol, 'sell', size, limit_price, client_order_id)


    def _place_market_order(self, symbol, side, size, client_order_id: str=None, reduce_only: bool=False) -> OrderResults:
        print(f"Placing market order {side} {size} {symbol}")
        res = self._place_order(OrderType.MARKET, symbol, side, size, limit_price=None, client_order_id=client_order_id, reduce_only=reduce_only)
        print(res)
        # TODO: Handle this
        #         Sell Market pf_ethusd 0.05235602094240838
        # Placing market order sell 0.05235602094240838 pf_ethusd
        # {'result': 'success', 'sendStatus': {'status': 'invalidSize'}, 'serverTime': '2023-06-30T17:04:07.001Z'}
        success = res["result"] == 'success'
        if success:
            # {'result': 'success', 'sendStatus': {'status': 'invalidSize'}, 'serverTime': '2023-05-27T17:21:57.429Z'} TODO: Handle this
            sendStatus = res['sendStatus']
            orderEvents = sendStatus['orderEvents']
            inf = orderEvents[0]['orderPriorExecution']
            order = OrderEvent.from_dict(inf)
        else:
            order = None
        return OrderResults(success, order)


    def _place_limit_order(self, symbol: str, side: str, size: float, limit_price: float, client_order_id: str=None) -> OrderResults:
        res = self._place_order(OrderType.LIMIT, symbol, side, size, limit_price, client_order_id)
        success = res["result"] == 'success'
        if success:
            sendStatus = res['sendStatus']
            orderEvents = sendStatus['orderEvents']
            inf = orderEvents[0]['order']
            order = OrderEvent.from_dict(inf)
        else:
            order = None
        return OrderResults(success, order)


    def _place_order(self, order_type: OrderType, symbol: str, side: str, size: float, limit_price: float, client_order_id: str=None, reduce_only: bool=False) -> OrderResults:
        order = self.api.send_order(order_type.value, symbol, side, size, limit_price, stopPrice=None, clientOrderId=client_order_id, reduce_only=reduce_only)
        return json.loads(order)


    def close(self, position: OpenPosition) -> OrderResults:
        '''
        Loka opinni stöðu
        '''
        if position.is_short():
            res = self.long_market(position.symbol, position.size, reduce_only=True)
        else:
            res = self.short_market(position.symbol, position.size, reduce_only=True)
        return res

    def cancel(self, order_id) -> None:
        '''
        Hætta við öll tilboð fyrir tiltekið order_id
        '''
        self.api.cancel_order(order_id)

    def cancel_for_symbol(self, symbol):
        '''
        Hætta við öll tilboð fyrir tiltekið symbol
        '''
        self.api.cancel_all_orders(symbol)

    def cancel_all(self) -> None:
        '''Hætta við öll tilboð'''
        self.api.cancel_all_orders()

    def edit(self, size: float,  limit_price: float, stop_price: float = None, order_id: str = None, client_order_id: str = None) -> None:
        '''Breyta opnu tilboði.'''
        if client_order_id is None and order_id is None:
            print('Verður að gefa upp annað hvort order_id eða client_order_id')
            return

        if client_order_id is not None:
            id = f"cliOrdId={client_order_id}"
        else:
            id = f"orderId={order_id}"

        postBody = "%s&limitPrice=%s&size=%s" % (
            id, limit_price, size)
        
        if stop_price is not None:
            postBody = postBody + f"&stopPrice={stop_price}"
        self.api.edit_order(postBody)

    def open_orders(self) -> List[OpenOrder]:
        '''Öll gild/opin tilboð'''
        orders = self.api.get_openorders()
        res = json.loads(orders)

        success = res["result"] == 'success'
        if success:
            return [OpenOrder.from_dict(o) for o in res["openOrders"]]
        return orders

    def positions(self) -> List[OpenPosition]:
        '''Allar opnar stöður'''
        pos = self.api.get_openpositions()
        res = json.loads(pos)
        success = res["result"] == 'success'
        ps = res['openPositions']
        if success:
            ps = [OpenPosition.from_dict(p) for p in ps]
            symbols = [p.symbol for p in ps]
            tickers = self.tickers_for_symbols(symbols)
            for p in ps:
                p.ticker = tickers[p.symbol]
            return ps
        return pos
    
    def order_status(self, order_id: str) -> OpenOrder:
        orders = self.api.get_order_status(order_id)
        res = json.loads(orders)
        success = res["result"] == 'success'
        os = res["orders"][0]
        o = os['order']

        quantity = float(o['quantity'])
        filled = float(o['filled'])
        unfilled = quantity - filled

        oo = OpenOrder( order_id = o['orderId'], 
            symbol = o['symbol'],
            side = o['side'],
            orderType = o['type'],
            limitPrice = float(o['limitPrice']),
            unfilledSize = unfilled,
            receivedTime = '',
            status = os['status'],
            filledSize = filled,
            reduceOnly = o['reduceOnly'],
            lastUpdateTime = o['lastUpdateTimestamp'],
            cliOrdId = o['cliOrdId']
            )
        return oo
    
    def executions(self, since: datetime, before: datetime = None, limit: int = 1000):
        '''Executions á gefnu tímabili'''     
        timestamp = since.timestamp()
        milliseconds = int(timestamp * 1000)
        xs = self.api.get_executions(since=milliseconds, before=before, limit=limit)
        executedOrders = [x['event']['execution']['execution'] for x in xs]
        return [Execution.from_kraken(x) for x in executedOrders]

    def executions_by_exchage_ids(self, exchange_ids: list[str], since: datetime, before: datetime = None, limit: int = 1000):    
        xs = self.executions(since, before, limit)
        return [x for x in xs if x.orderUid in exchange_ids] 
        
    def accounts(self) -> List[Account]:
        return self.api.get_accounts()

    def tickers(self) -> list[Ticker]:
        res = self.api.get_tickers()
        res = json.loads(res)
        ts = res['tickers'] 
        return [Ticker.from_kraken(t) for t in ts]
        
    def tickers_for_symbols(self, symbols: list[str]) -> dict[Ticker]:
        ts = self.tickers()
        xs = [t for t in ts if t.symbol in symbols]
        return dict([(x.symbol, x) for x in xs])

    def instruments(self) -> Instruments:
        res = self.api.get_instruments()
        res = json.loads(res)
        return Instruments([Instrument.from_kraken(i) for i in res['instruments']])

# {
#     "result":"success",
#     "serverTime":"2023-03-15T15:12:15.241Z",
#     "orders":[
#         {
#             "order":{
#                 "type":"ORDER",
#                 "orderId":"910d02f3-5b5f-4eab-b156-06162abd41d7",
#                 "cliOrdId":"Hohoho4",
#                 "symbol":"pf_atomusd",
#                 "side":"buy",
#                 "quantity":5,
#                 "filled":0,
#                 "limitPrice":2,
#                 "reduceOnly":false,
#                 "timestamp":"2023-03-15T15:05:50.905Z",
#                 "lastUpdateTimestamp":"2023-03-15T15:05:50.905Z"
#             },
#             "status":"ENTERED_BOOK",
#             "updateReason":null,
#             "error":null
#         }
#     ]
# }