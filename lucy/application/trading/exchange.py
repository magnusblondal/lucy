from datetime import datetime
from enum import Enum
import json
from typing import List

import pandas as pd

from lucy.model.interval import Interval
from lucy.model.symbol import Symbol

from .flex import Account
from .kraken_futures_api import FuturesApi
from .kraken_api import KrakenApi

from .open_order import OpenOrder, OrderResults, OrderEvent
from .open_position import OpenPosition
from .execution import Execution
from .ticker import Ticker
from .instrument import Instrument, Instruments
from lucy.main_logger import MainLogger
import lucy.application.utils.dtm_utils as dtm
from config import settings


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
        public = settings.api_key
        private = settings.api_secret
        self.futures_api = FuturesApi(path, public, private)
        self.kraken_api = KrakenApi()
        self.logger = MainLogger.get_logger(__name__)

    def long_market(
        self,
        symbol: Symbol,
        size: float,
        client_order_id: str = "",
        reduce_only: bool = False
    ) -> OrderResults:
        return self._place_market_order(
            symbol,
            'buy',
            size,
            client_order_id,
            reduce_only
        )

    def short_market(
        self,
        symbol: Symbol,
        size: float,
        client_order_id: str = "",
        reduce_only: bool = False
    ):
        return self._place_market_order(
            symbol,
            'sell',
            size,
            client_order_id,
            reduce_only
        )

    def long_lmt(
        self,
        symbol: Symbol,
        size: float,
        limit_price: float,
        stop_price: float = None,
        client_order_id: str = ""
    ) -> OrderResults:
        # orderType = OrderType.LIMIT if stop_price is None else OrderType.STOP
        return self._place_limit_order(
            symbol,
            'buy',
            size,
            limit_price,
            client_order_id
        )

    def short_lmt(
        self,
        symbol: Symbol,
        size: float,
        limit_price: float,
        client_order_id: str = ""
    ) -> OrderResults:
        return self._place_limit_order(
            symbol,
            'sell',
            size,
            limit_price,
            client_order_id
        )

    def _place_market_order(
        self,
        symbol: Symbol,
        side: str,
        size: float,
        client_order_id: str = "",
        reduce_only: bool = False
    ) -> OrderResults:
        self.logger.info(f"Placing market order {side} {size} {symbol}")
        return self._place_order(
            OrderType.RKET,
            symbol,
            side,
            size,
            limit_price=None,
            client_order_id=client_order_id,
            reduce_only=reduce_only
        )
        # TODO: Handle this
        #         Sell Market pf_ethusd 0.05235602094240838

    def _place_limit_order(
        self,
        symbol: Symbol,
        side: str,
        size: float,
        limit_price: float,
        client_order_id: str = ""
    ) -> OrderResults:
        return self._place_order(
            OrderType.LIMIT,
            symbol,
            side,
            size,
            limit_price,
            client_order_id
        )

    def _place_order(
        self,
        order_type: OrderType,
        symbol: Symbol,
        side: str,
        size: float,
        limit_price: float,
        client_order_id: str = "",
        reduce_only: bool = False
    ) -> OrderResults:
        order = self.futures_api.send_order(
            order_type.value,
            str(symbol),
            side,
            size,
            limit_price,
            stopPrice=None,
            clientOrderId=client_order_id,
            reduce_only=reduce_only
        )
        res = json.loads(order)
        results = self._parse_order_results(res)
        return results

        # success = res["result"] == 'success'
        # if success:
        #     sendStatus = res['sendStatus']
        #     orderEvents = sendStatus['orderEvents']

        #     inf = orderEvents[0] # ['order']
        #     order = OrderEvent.from_dict(inf)
        # else:
        #     order = None
        # return OrderResults(success, order)

        # success = res["result"] == 'success'
        # if success:
        #     sendStatus = res['sendStatus']
        #     orderEvents = sendStatus['orderEvents']
        #     inf = orderEvents[0]['order']
        #     order = OrderEvent.from_dict(inf)
        # else:
        #     order = None
        # return OrderResults(success, order)

    def close(self, position: OpenPosition) -> OrderResults:
        '''
        Loka opinni stöðu
        '''
        if position.is_short():
            res = self.long_market(
                position.symbol, position.size, reduce_only=True)
        else:
            res = self.short_market(
                position.symbol, position.size, reduce_only=True)
        return res

    def cancel(self, order_id) -> None:
        '''
        Hætta við öll tilboð fyrir tiltekið order_id
        '''
        self.futures_api.cancel_order(order_id)

    def cancel_for_symbol(self, symbol: Symbol):
        '''
        Hætta við öll tilboð fyrir tiltekið symbol
        '''
        self.futures_api.cancel_all_orders(str(symbol))

    def cancel_all(self) -> None:
        '''Hætta við öll tilboð'''
        self.futures_api.cancel_all_orders()

    def edit(
        self,
        size: float,
        limit_price: float,
        stop_price: float = None,
        order_id: str = None,
        client_order_id: str = None
    ) -> None:
        '''Breyta opnu tilboði.'''
        if client_order_id is None and order_id is None:
            print('Vantar annad hvort order_id eða client_order_id')
            return

        if client_order_id is not None:
            id = f"cliOrdId={client_order_id}"
        else:
            id = f"orderId={order_id}"

        postBody = "%s&limitPrice=%s&size=%s" % (
            id, limit_price, size)

        if stop_price is not None:
            postBody = postBody + f"&stopPrice={stop_price}"
        self.futures_api.edit_order(postBody)

    def open_orders(self) -> List[OpenOrder]:
        '''Öll gild/opin tilboð'''
        orders = self.futures_api.get_openorders()
        res = json.loads(orders)

        success = res["result"] == 'success'
        if success:
            return [OpenOrder.from_dict(o) for o in res["openOrders"]]
        return orders

    def positions(self) -> List[OpenPosition]:
        '''Allar opnar stöður'''
        pos = self.futures_api.get_openpositions()
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
        '''Staða tiltekins tilboðs'''
        orders = self.futures_api.get_order_status(order_id)
        res = json.loads(orders)
        # success = res["result"] == 'success'
        os = res["orders"][0]
        o = os['order']

        quantity = float(o['quantity'])
        filled = float(o['filled'])
        unfilled = quantity - filled

        oo = OpenOrder(order_id=o['orderId'],
                       symbol=o['symbol'],
                       side=o['side'],
                       orderType=o['type'],
                       limitPrice=float(o['limitPrice']),
                       unfilledSize=unfilled,
                       receivedTime='',
                       status=os['status'],
                       filledSize=filled,
                       reduceOnly=o['reduceOnly'],
                       lastUpdateTime=o['lastUpdateTimestamp'],
                       cliOrdId=o['cliOrdId']
                       )
        return oo

    def executions(
        self,
        since: datetime,
        before: datetime = None,
        limit: int = 1000
    ):
        '''Executions á gefnu tímabili'''
        timestamp = since.timestamp()
        milliseconds = int(timestamp * 1000)
        xs = self.futures_api.get_executions(
            since=milliseconds, before=before, limit=limit)
        executedOrders = [x['event']['execution']['execution'] for x in xs]
        return [Execution.from_kraken(x) for x in executedOrders]

    def executions_by_exchage_ids(
        self,
        exchange_ids: list[str],
        since: datetime,
        before: datetime = None,
        limit: int = 1000
    ):
        xs = self.executions(since, before, limit)
        return [x for x in xs if x.orderUid in exchange_ids]

    def accounts(self) -> List[Account]:
        return self.futures_api.get_accounts()

    def tickers(self) -> list[Ticker]:
        res = self.futures_api.get_tickers()
        res = json.loads(res)
        ts = res['tickers']
        return [Ticker.from_kraken(t) for t in ts]

    def tickers_for_symbols(self, symbols: list[str]) -> dict[Ticker]:
        ts = self.tickers()
        xs = [t for t in ts if t.symbol in symbols]
        return dict([(x.symbol, x) for x in xs])

    def instruments(self) -> Instruments:
        res = self.futures_api.get_instruments()
        res = json.loads(res)
        return Instruments([
            Instrument.from_kraken(i)
            for i in res['instruments']
        ])

    def ohlc(
        self,
        symbol: Symbol,
        interval: Interval,
        tick_type: str = "trade",
        since: int = 0
    ) -> pd.DataFrame:
        '''
        tick_type:  "spot", "mark", "trade"
        from_time:  epoch timestamp
        '''
        if since == 0:
            since = dtm.since_max_candles(interval)

        try:
            res = self.futures_api.ohlc(
                symbol, interval.resolution(), tick_type, since)
            if res.get("candles") is None:
                self.logger.error(f"No candles received; {res})")
                return pd.DataFrame([])

            data = res['candles']
            ohlc = pd.DataFrame(
                data,
                columns=['time', 'open', 'high', 'low', 'close', 'volume'])
            ohlc['time'] = pd.to_datetime(ohlc['time'], unit='ms')
            ohlc = ohlc.set_index('time', drop=True)
            ohlc['open'] = ohlc['open'].astype(float)
            ohlc['close'] = ohlc['close'].astype(float)
            ohlc['high'] = ohlc['high'].astype(float)
            ohlc['low'] = ohlc['low'].astype(float)
            ohlc['volume'] = ohlc['volume'].astype(float)
            return ohlc
        except Exception as e:
            print(e)
            self.logger.error(e)
            return pd.DataFrame([])

    # Þessi sækir í regular api
    # def ohlc(self, symbol: str, interval: int, since: int = 0) -> pd.DataFrame:
    #     res = self.kraken_api.ohlc(symbol, interval, since)
    #     if 'result' not in res.keys():
    #         print('Villa við að sækja gögn')
    #         print(res)
    #         return pd.DataFrame([])

    #     data = res['result']
    #     data = [v for (k, v) in data.items() if k != 'last'][0]
    #     ohlc = pd.DataFrame(data, columns=['time',
    #     'open', 'high', 'low', 'close', 'vwap','volume', 'count'])
    #     ohlc['time']    = pd.to_datetime(ohlc['time'], unit='s')
    #     ohlc            = ohlc.set_index('time', drop=True)
    #     ohlc['open']    = ohlc['open'].astype(float)
    #     ohlc['close']   = ohlc['close'].astype(float)
    #     ohlc['high']    = ohlc['high'].astype(float)
    #     ohlc['low']     = ohlc['low'].astype(float)
    #     ohlc['vwap']    = ohlc['vwap'].astype(float)
    #     ohlc['volume']  = ohlc['volume'].astype(float)
    #     ohlc['count']   = ohlc['count'].astype(int)
    #     return ohlc

    def _parse_order_results(self, res):
        success = res["result"] == 'success'

        if not success:
            return None

        if 'sendStatus' in res.keys():
            sendStatus = res['sendStatus']
            if 'orderEvents' in sendStatus.keys():
                orderEvents = sendStatus['orderEvents']
                inf = orderEvents[0]
                if 'executionId' in inf.keys():
                    oe = OrderEvent.from_dict(inf['orderPriorExecution'])
                    return OrderResults(success, oe)

        # inf = orderEvents[0] # ['order']
        # order = OrderEvent.from_dict(inf)
        # return OrderResults(success, order)

        # success = res["result"] == 'success'
        # if success:
        #     sendStatus = res['sendStatus']
        #     orderEvents = sendStatus['orderEvents']
        #     inf = orderEvents[0]['order']
        #     order = OrderEvent.from_dict(inf)
        # else:
        #     order = None
        # return OrderResults(success, order)

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

# {
#     'result': 'success',
#     'sendStatus':
#     {
#         'order_id': '6a50f30b-73e9-4f44-8d34-e39a73a9592b',
#         'cliOrdId': 'XWXvVxoQa6_3CBbvAXcPb',
#         'status': 'placed',
#         'receivedTime': '2023-07-13T08:26:43.059Z',
#         'orderEvents': [
#             {
#                 'executionId': '8562c94b-926a-4e5b-858d-98612af1845a',
#                 'price': 0.7298,
#                 'amount': 137.0,
#                 'orderPriorEdit': None,
#                 'orderPriorExecution':
#                 {
#                       'orderId': '6a50f30b-73e9-4f44-8d34-e39a73a9592b',
#                       'cliOrdId': 'XWXvVxoQa6_3CBbvAXcPb',
#                       'type': 'ioc',
#                       'symbol': 'pf_maticusd',
#                       'side': 'buy',
#                       'quantity': 137.0,
#                       'filled': 0,
#                       'limitPrice': 0.737,
#                       'reduceOnly': False,
#                       'timestamp': '2023-07-13T08:26:43.059Z',
#                       'lastUpdateTimestamp': '2023-07-13T08:26:43.059Z'
#                 },
#                 'takerReducedQuantity': None,
#                 'type': 'EXECUTION'
#             }
#         ]
#     },
#     'serverTime': '2023-07-13T08:26:43.061Z'
# }
