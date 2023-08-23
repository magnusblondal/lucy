from datetime import datetime, timedelta
from typing import Tuple
from pyparsing import Iterator

from lucy.model.order import Order, Orders
from lucy.model.domain_model import DomainModel
from lucy.model.id import Id
from lucy.model.signal import Signal, Signals

from lucy.application.events.some_events import PositionEntryEvent, AddFundsEvent, PositionExitEvent, SignalEvent, ProfitCalculatedEvent
from lucy.application.events.order_events import OrderCreatedEvent
from lucy.application.trading.exchange import Exchange
from lucy.application.trading.execution import Execution
from lucy.application.events.event import DomainEvent
from lucy.main_logger import MainLogger

from rich import inspect

from lucy.model.symbol import Symbol

class Position(DomainModel):
    
    def __init__(self, id: Id, bot_id: Id, symbol: Symbol, side:str, 
                 profit: float = 0.0, profit_pct:float = 0.0,
                 created_at: datetime = None) -> None:
        self.logger     = MainLogger.get_logger(__name__)
        self.bot_id     = bot_id
        self.symbol     = symbol if isinstance(symbol, Symbol) else Symbol(symbol)
        self.side       = side
        self.profit     = profit
        self.profit_pct = profit_pct
        self.created_at = created_at or None
        self.orders     = Orders()
        self.signals    = Signals()
        self.exchange   = Exchange()
        super().__init__(id)

    def events(self) -> list[DomainEvent]:
        evts = self._events or []
        self._events = []
        return evts     
    
    def _create_buy_order(self, qty: float, order_type: str, reduce_only: bool = False) -> Order:
        print(f"Long Market {self.symbol} {qty}")
        return self.exchange.long_market(self.symbol, qty, self.id.make_combined_id(), reduce_only).to_model(self.id, self.bot_id, reduce_only, order_type)

    def _create_sell_order(self, qty: float, order_type: str, reduce_only: bool = False) -> Order:
        print(f"Sell Market {self.symbol} {qty}")
        return self.exchange.short_market(self.symbol, qty, self.id.make_combined_id(), reduce_only).to_model(self.id, self.bot_id, reduce_only, order_type)
    # TODO: Taka á þessu:
    # {'result': 'success', 'sendStatus': {'status': 'wouldNotReducePosition'}, 'serverTime': '2023-07-19T00:27:27.482Z'}

    def fits_signal(self, signal: Signal) -> bool:
        same_symbols = self.symbol == signal.ticker
        same_side = self.side == signal.side 
        return same_symbols and same_side and self.is_open()
    
    def is_open(self):
        return self.orders.is_open()
    
    def is_long(self):
        return self.side.lower() == "long"
        
    def _entry_orders(self) -> Orders:
        return Orders([o for o in self.orders if not o.is_close_order() ])

    def open_qty(self):
        qty = [o.qty for o in self._entry_orders()]
        return sum(qty) if len(qty) > 0 else 0
    
    def _handle_order(self, signal: Signal, qty: float, order_type: str) -> Order:
        self.signals.append(signal)
        if self.is_long():
            order = self._create_buy_order(qty, order_type)
        else:
            order = self._create_sell_order(qty, order_type)  
        order.signal = signal
        self.orders.append(order)
        return order

    def entry(self, signal: Signal, entry_size: float):
        self._this_just_happened(SignalEvent(signal, self.id))
        qty = entry_size / signal.close
        qty = round(qty, 0)
        order = self._handle_order(signal, qty, 'entry')
        self._this_just_happened(PositionEntryEvent(self.id, self.bot_id, self.symbol, qty, self.side))
        self._this_just_happened(OrderCreatedEvent(order))
        # self._this_just_happened(OrderCreatedEvent(self.id, self.bot_id, 'entry', order))

    def can_add_safety_order(self, max_safety_orders: int) -> bool:
        return len(self.orders) <= max_safety_orders
    
    def add_funds(self, signal: Signal, so_size: float, max_safety_orders: int):
        print(f"Add funds {signal.id.id}")
        print(f"{signal.id.id} - {len(self.signals)}")
        self._this_just_happened(SignalEvent(signal, self.id))
        if not self.is_open():
            print(f"-> Position {self.id} handle {signal.signal_type} -- position is closed, cannot add funds")
            return
        
        if self.can_add_safety_order(max_safety_orders) == False:
            self.logger.info(f"Position {self.id} Max: {max_safety_orders} Orders: {len(self.orders)} -- Max safety order reached, cannot add funds")
            print(f"-> Position {self.id} Max: {max_safety_orders} Orders: {len(self.orders)} -- Max safety order reached, cannot add funds")
            return
            
        qty = round(so_size / signal.close)
        order = self._handle_order(signal, qty, 'add_funds')
        self._this_just_happened(OrderCreatedEvent(order ))      

    def close(self, signal: Signal):
        self._this_just_happened(SignalEvent(signal, self.id))
        if self.is_open():
            self.signals.append(signal)
            if self.is_long():
                order = self._create_sell_order(self.open_qty(), 'close', reduce_only=True)
            else:
                order = self._create_buy_order(self.open_qty(), 'close', reduce_only=True)
            self.orders.append(order)
            self._this_just_happened(PositionExitEvent(position_id=self.id))  
            self._this_just_happened(OrderCreatedEvent(order))      
        else:
            print(f"-> Bot {self.id} handle {signal.signal_type} -- position is not open, cannot close")
        
    def _min_max_dates(self) -> Tuple[datetime, datetime]:
        ts = [o.order_created_at for o in self.orders]
        return (min(ts), max(ts))

    def _exchange_order_ids(self) -> list[str]:
        return [o.exchange_id for o in self.orders]
    
    def _fetch_executions(self) -> list[Execution]:
        start, end = self._min_max_dates()
        since = start - timedelta(seconds=1)
        before = end  + timedelta(seconds=1)
        return self.exchange.executions_by_exchage_ids(self._exchange_order_ids(), since, before)
    
    def _avg_price(self, buys: list[Execution]) -> float:
        total_spent = sum([x.usdValue for x in buys])
        total_qty = sum([x.quantity for x in buys])
        return total_spent / total_qty
    
    def average_price(self) -> float:
        # TODO: nota executions úr grunni, frekar en að kalla eftir þeim
        # TODO: þetta er bara fyrir buy, þarf að bæta við fyrir sell
        executions = self._fetch_executions()
        buys = [x for x in executions if x.direction.lower() == "buy"]
        return self._avg_price(buys)
    
    def open_orders_count(self) -> int:
        return len(self._entry_orders())
    
    def last_order_price(self) -> float:
        return self.orders.last().price  # HUX: ætti þetta að vera frá fill?
    
    def is_audited(self) -> bool:
        return self.profit != 0.0
    
    def audit(self): # TODO: þetta er óþarfi, má kannski nota til að finna fills, ef það vantar
        if self.is_open():
            print(f"-> Position {self.id} audit -- position is open")
            return
        executions = self._fetch_executions()

        if len(self.orders) != len(executions):
            print(f"-> Position {self.id} audit -- order count mismatch -> {len(self.orders)} orders, {len(executions)} executions")
            return

        buys = [x for x in executions if x.direction.lower() == "buy"]
        sells = [x for x in executions if x.direction.lower() == "sell"]

        qty = sum([x.quantity for x in buys])
        
        avg_buy_price = self._avg_price(buys)
        avg_sell_price = self._avg_price(sells)
        price_diff = avg_sell_price - avg_buy_price
        self.profit = float(price_diff * qty)
        self.profit_pct = float((price_diff / avg_buy_price) * 100)

        print(f"-> Position {self.id} audit -- profit {self.profit} {self.profit_pct}")
        self._this_just_happened(ProfitCalculatedEvent(self.id, self.bot_id, self.profit, self.profit_pct))

    def calculate_profit_loss(self):
        if not self.orders.is_close_filled():
            print(f"-> Position {self.id} audit -- position is open")
            return
        profit, profit_pct, fees = self.orders.calculate_profit()
        self.profit = profit
        self.profit_pct = profit_pct
        self._this_just_happened(ProfitCalculatedEvent(self.id, self.bot_id, self.profit, self.profit_pct))
    
    def __str__(self) -> str:
        ss = '\n'.join([f"  {signal}" for signal in self.signals])
        os = '\n'.join([f"  {order}" for order in self.orders])
        pnl = f"PnL: {self.profit:.3f} {self.profit_pct:.2f}%"
        oc = "OPEN" if self.is_open() else "CLOSED"
        return f"Position {self.id} Bot: {self.bot_id}, {oc} {pnl} {self.created_at}\n{ss}\n{os}"
    
    
class Positions(list[Position]):
    def __init__(self, positions: list[Position] = None) -> None:
        super().__init__(positions or [])
    
    def create_new(self, signal: Signal) -> 'Position':
        symbol = signal.ticker if isinstance(signal.ticker, Symbol) else Symbol(signal.ticker)
        p = Position(Id(), signal.bot_id, symbol, signal.side)
        self.append(p)
        return p
    
    def has_open(self, symbol: Symbol) -> tuple[bool, Position]:
        symbol = symbol if isinstance(symbol, Symbol) else Symbol(symbol)
        for p in self:
            if p.symbol == symbol and p.is_open():
                return (True, p)
        return (False, None)
    
    def find_open_by_symbol(self, symbol: Symbol) -> Position:
        return next((p for p in self if p.symbol == symbol and p.is_open()), None)
    
    def is_empty(self) -> bool:
        return len(self) == 0
    
    def average_price_for(self, pair:str):
        return self.find_open_by_symbol(pair).average_price()
        
    def profit(self) -> float:
        '''Returns the total profit for all positions'''
        return sum([position.profit for position in self if position.profit is not None])
    
    def num_open(self) -> int:
        return len([p for p in self if p.is_open()])

    def num_closed(self) -> int:
        return len([p for p in self if not p.is_open()])

    def __str__(self) -> str:
        return '\n'.join([str(p) for p in self])
    
    def position_for_signal(self, signal: Signal) -> Position:        
        ps = [p for p in self if p.fits_signal(signal)]
        open = [p for p in ps if p.is_open()]
        return open[0] if len(open) > 0 else None
    
    # {
#     'uid': '6cdb3700-757b-4a5f-8a87-34db75903caa', 
#     'timestamp': 1685130589916, 
#     'event': {
#         'execution': {
#             'execution': {
#                 'uid': '45c4bb6f-9ce3-4258-82b1-b27b8f9815ae', 
#                 'order': {
#                     'uid': '57b4e666-ddfa-44bb-810b-caabca9f9bb2', 
#                     'accountUid': 'e8d555f5-e7d3-42a5-b9fa-66fcdf856405', 
#                     'tradeable': 'PF_ATOMUSD', 
#                     'direction': 'Buy', 
#                     'quantity': '1', 
#                     'filled': '0', 
#                     'timestamp': 1685130589916, 
#                     'limitPrice': '10.6650000000', 
#                     'orderType': 'IoC', 
#                     'clientId': '', 
#                     'reduceOnly': False, 
#                     'lastUpdateTimestamp': 1685130589916
#                 }, 
#                 'timestamp': 1685130589916, 
#                 'quantity': '1', 
#                 'price': '10.56000000', 
#                 'markPrice': '10.55708715830', 
#                 'limitFilled': False, 
#                 'executionType': 'taker', 
#                 'usdValue': '10.56', 
#                 'orderData': {
#                     'positionSize': '3', 
#                     'fee': '0.00528000000'
#                 }
#             }, 
#             'takerReducedQuantity': ''
#         }
#     }
# }