from datetime import datetime
import itertools

from lucy.application.trading.feeds.fills import Fills
from lucy.model.id import Id

class Order:
    id: Id
    position_id: Id 
    bot_id: Id
    symbol: str
    qty: float
    price: float
    order_type: str
    side: str
    type: str
    filled: float
    limit_price: float
    reduce_only: bool
    order_created_at: datetime 
    last_update_timestamp: datetime
    exchange_id: str
    created_at: datetime

    def __init__(self, id: Id, position_id: Id , bot_id: Id, symbol: str, 
                 qty: float, price: float, order_type: str,
                 side: str, type: str, filled: float, limit_price: float, reduce_only: bool, 
                 order_created_at: datetime , last_update_timestamp: datetime, exchange_id: str,
                 created_at: datetime, fills: Fills = None) -> None:
        self.id                     = Id(id) if isinstance(id, str) else id 
        self.position_id            = position_id
        self.bot_id                 = bot_id
        self.symbol                 = symbol
        self.qty                    = qty
        self.price                  = float(price)
        self.order_type             = order_type
        self.side                   = side
        self.type                   = type
        self.filled                 = filled
        self.limit_price            = limit_price
        self.reduce_only            = reduce_only
        self.order_created_at       = order_created_at
        self.last_update_timestamp  = last_update_timestamp
        self.exchange_id            = exchange_id
        self.created_at             = created_at
        self.fills                  = fills or Fills()

    def is_close_order(self) -> bool:
        return self.order_type == "close"
    
    def is_entry_order(self) -> bool:
        return self.order_type == "entry"
    
    def is_filled(self) -> bool:
        return self.fills.is_filled()
    
    def avg_fill_price(self) -> float:
        ps = [float(f.price) * float(f.qty)  for f in self.fills]
        qs = sum([float(f.qty) for f in self.fills])
        return float(sum(ps) / qs) if qs > 0 else 0
    
    def __str__(self) -> str:
        fills = '\n'.join([f"   {f}" for f in self.fills])
        fills = f"\n{fills}" if len(fills) > 0 else ""
        return f"Order:: id: {self.id}, position_id: {self.position_id}, bot_id: {self.bot_id}, symbol: {self.symbol}, qty: {self.qty}, price: {self.price}, side: {self.side}, order type: '{self.order_type}' type: {self.type}, filled: {self.filled}, limit_price: {self.limit_price}, reduce_only: {self.reduce_only}, order_created_at: {self.order_created_at}, last_update_timestamp: {self.last_update_timestamp}, created_at: {self.created_at}{fills}"
    

class Orders(list[Order]):
    def __init__(self, orders: list[Order] = None) -> None:
        super().__init__(orders or [])
    
    def last(self) -> Order:
        return sorted(self, key = lambda x: x.order_created_at)[-1]
    
    def for_position(self, position_id: Id) -> 'Orders':
        return Orders([o for o in self if o.position_id == position_id])
    
    def is_open(self):
        return not self.is_closed()
    
    def is_closed(self) -> bool:
        return any(o for o in self if o.is_close_order())
    
    def close_order(self) -> Order:
        os = [o for o in self if o.is_close_order()]
        return os[0] if len(os) > 0 else None
    
    def accumulate_orders(self) -> 'Orders':
        return Orders([o for o in self if not o.is_close_order()])
    
    def total_qty(self) -> float:
        return float(sum([o.qty for o in self.accumulate_orders()]))
    
    def is_close_filled(self) -> bool:
        o = self.close_order()
        return o is not None and o.is_filled()
    
    def avg_accumulation_fill_price(self) -> float:
        orders = self.accumulate_orders()        
        ps = [float(f.price) * float(f.qty)  for f in orders.fills()]
        qs = sum([float(f.qty) for f in orders.fills()])
        return sum(ps) / qs if qs > 0 else 0
    
    def avg_close_fill_price(self) -> float:
        o = self.close_order()
        return o.avg_fill_price() if o is not None else 0
    
    def avg_fill_price(self) -> float:
        '''Note: first filter on what fills to apply to'''
        ps = [float(f.price) * float(f.qty)  for f in self.fills()]
        qs = sum([float(f.qty) for f in self.fills()])
        return sum(ps) / qs if qs > 0 else 0
    
    def fills(self) -> Fills:
        fills_list = [o.fills for o in self]
        return Fills(list(itertools.chain(*fills_list)))
    
    def set_fills(self, fills: Fills) -> None:
        self.fills = fills

    def calculate_profit(self) -> tuple[float, float]:
        buy_price = self.avg_accumulation_fill_price()
        sell_price = self.avg_close_fill_price()
        qty = self.total_qty()
        price_diff = sell_price - buy_price
        profit = price_diff * qty
        profit_pct = (price_diff / buy_price) * 100
        return (profit, profit_pct)

    def __str__(self) -> str:
        os = [f"{str(o.id)}: {o.order_type}" for o in self]
        return f"Orders:: {len(self)} {os}"