from datetime import datetime, timedelta
from typing import Tuple

from .order import Order

from .domain_model import DomainModel
from .id import Id, generate_id
from .signal import Signal
from ..events.event import PositionEntryEvent, AddFundsEvent, PositionExitEvent, OrderCreatedEvent, SignalEvent, ProfitCalculatedEvent
from ..trading.open_order import OrderResults
from ..trading.exchange import Exchange
from ..trading.pairs_usd_pf import *
from ..trading.execution import Execution
from ..models.domain_model import DomainModel
from ..events.event import DomainEvent

from rich import inspect

class Position(DomainModel):
    bot_id: Id
    signals: list[Signal] = []
    orders: list[OrderResults] = []
    symbol: str = ""
    profit: float = 0.0
    profit_pct: float = 0.0
    side: str = ""
    created_at: datetime = None

    def __init__(self, id: Id, bot_id: Id, symbol: str, side:str, profit: float = 0.0, profit_pct:float = 0.0) -> None:
        self.bot_id = bot_id
        self.symbol = symbol
        self.side = side
        self.profit = profit
        self.profit_pct = profit_pct
        super().__init__(id)
    
    @staticmethod
    def create_new(signal: Signal) -> 'Position':
        symbol = pair_symbol(signal.ticker)
        return Position(Id(), signal.bot_id, symbol, signal.side)
        
    def events(self) -> list[DomainEvent]:
        return self._events if self._events is not None else []       
    
    def _create_buy_order(self, qty: float, reduce_only: bool = False) -> OrderResults:
        print(f"Long Market {self.symbol} {qty}")
        return Exchange().long_market(self.symbol, qty, self.id.make_combined_id(), reduce_only)

    def _create_sell_order(self, qty: float, reduce_only: bool = False) -> OrderResults:
        print(f"Sell Market {self.symbol} {qty}")
        return Exchange().short_market(self.symbol, qty, self.id.make_combined_id(), reduce_only)

    def fits_signal(self, signal: Signal) -> bool:
        same_symbols = self.symbol == pair_symbol(signal.ticker)
        same_side = self.side == signal.side 
        return same_symbols and same_side and self.is_open()
    
    def is_open(self):
        return len(self._close_orders()) == 0

    def is_long(self):
        return self.side.lower() == "long"
    
    def _close_orders(self) -> list[Order]:
        return [o for o in self.orders if o.is_close_order() ]
    
    def _entry_orders(self) -> list[Order]:
        return [o for o in self.orders if not o.is_close_order() ]

    def open_qty(self):
        qty = [o.qty for o in self._entry_orders()]
        return sum(qty) if len(qty) > 0 else 0
    
    def _handle_order(self, signal: Signal, qty: float):
        self.signals.append(signal)
        if self.is_long():
            order = self._create_buy_order(qty)
        else:
            order = self._create_sell_order(qty)            
        self.orders.append(order)
        return order

    def entry(self, signal: Signal, entry_size: float):
        self._this_just_happened(SignalEvent(signal, self.id))
        qty = entry_size / signal.close
        qty = round(qty, 0)
        order = self._handle_order(signal, qty)
        self._this_just_happened(PositionEntryEvent(position_id=self.id, bot_id=self.bot_id, symbol=self.symbol, qty=qty, side=self.side))
        self._this_just_happened(OrderCreatedEvent(self.id, self.bot_id, 'entry', order))

    def add_funds(self, signal: Signal, so_size: float, max_safety_orders: int):
        print(f"Add funds {signal.id.id}")
        print(f"{signal.id.id} - {len(self.signals)}")
        self._this_just_happened(SignalEvent(signal, self.id))
        if not self.is_open():
            print(f"-> Position {self.id} handle {signal.signal_type} -- position is closed, cannot add funds")
            return
        
        if len(self.orders) < max_safety_orders:
            print(f"-> Position {self.id} Max: {max_safety_orders} Orders: {len(self.orders)} -- Max safety order reached, cannot add funds")
            return
            
        qty = round(so_size / signal.close)
        order = self._handle_order(signal, qty)
        self._this_just_happened(OrderCreatedEvent(self.id, self.bot_id, 'add_funds', order ))      

    def close(self, signal: Signal):
        self._this_just_happened(SignalEvent(signal, self.id))
        if self.is_open():
            self.signals.append(signal)
            if self.is_long():
                order = self._create_sell_order(self.open_qty(), reduce_only=True)
            else:
                order = self._create_buy_order(self.open_qty(), reduce_only=True)
            self._this_just_happened(PositionExitEvent(position_id=self.id))  
            self.orders.append(order)
            self._this_just_happened(OrderCreatedEvent(self.id, self.bot_id, 'close', order ))      
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
        return Exchange().executions_by_exchage_ids(self._exchange_order_ids(), since, before)
    
    def average_price(self, buys: list[Execution]) -> float:
        total_spent = sum([x.usdValue for x in buys])
        total_qty = sum([x.quantity for x in buys])
        return total_spent / total_qty
    
    def is_audited(self) -> bool:
        return self.profit != 0.0
    
    def audit(self):
        if self.is_open():
            print(f"-> Bot {self.id} audit -- position is open")
            return
        executions = self._fetch_executions()

        if len(self.orders) != len(executions):
            print(f"-> Bot {self.id} audit -- order count mismatch -> {len(self.orders)} orders, {len(executions)} executions")
            return

        buys = [x for x in executions if x.direction.lower() == "buy"]
        sells = [x for x in executions if x.direction.lower() == "sell"]
        
        avg_buy_price = self.average_price(buys)
        avg_sell_price = self.average_price(sells)
        self.profit = avg_sell_price - avg_buy_price
        self.profit_pct = (self.profit / avg_buy_price) * 100

        print(f"-> Bot {self.id} audit -- profit {self.profit} {self.profit_pct}")
        self._this_just_happened(ProfitCalculatedEvent(self.id, self.bot_id, self.profit, self.profit_pct))


    def __str__(self) -> str:
        ss = '\n'.join([f"\t\t{signal}" for signal in self.signals])
        os = '\n'.join([f"\t\t{order}" for order in self.orders])
        return f"Position id: {self.id}, bot_id: {self.bot_id}, open: {self.is_open()}, signals: \n {ss}, orders: \n {os}"
    
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