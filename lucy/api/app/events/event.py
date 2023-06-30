from ..models.id import Id
from ..models.signal import Signal
from ..trading.open_order import OrderResults

class Event:
    pass

class DomainEvent(Event):
    pass

class SignalEvent(DomainEvent):
    signal: Signal
    position_id: Id

    def __init__(self, signal: Signal, position_id: Id) -> None:
        super().__init__()
        self.signal = signal
        self.position_id = position_id
        self.bot_id = signal.bot_id

    def __str__(self) -> str: 
        return f"SignalEvent:: bot_id: {self.bot_id}, signal: {self.signal}"
    
class PositionEntryEvent(DomainEvent):
    position_id: Id
    bot_id: Id
    symbol: str
    qty: float
    side: str

    def __init__(self, position_id: Id, bot_id: Id, symbol: str, qty: float, side: str) -> None:
        super().__init__()
        self.position_id = position_id
        self.bot_id = bot_id
        self.symbol = symbol
        self.qty = qty
        self.side = side


class AddFundsEvent(DomainEvent):
    position_id: Id
    bot_id: Id
    amount: float    
    
    def __init__(self, position_id: Id, bot_id: Id, amount: float) -> None:
        super().__init__()
        self.position_id = position_id
        self.bot_id = bot_id
        self.amount = amount

class PositionExitEvent(DomainEvent):
    position_id: Id
    
    def __init__(self, position_id: Id) -> None:
        super().__init__()
        self.position_id = position_id

class OrderCreatedEvent(DomainEvent):
    position_id: Id
    bot_id: Id
    order_type: str
    order: OrderResults

    def __init__(self, position_id: Id, bot_id: Id, order_type: str,  order: OrderResults) -> None:
        super().__init__()
        self.position_id = position_id
        self.bot_id = bot_id
        self.order_type = order_type
        self.order = order

class ProfitCalculatedEvent(DomainEvent):
    position_id: Id
    bot_id: Id
    profit: float
    profit_percentage: float

    def __init__(self, position_id: Id, bot_id: Id, profit: float, profit_pct: float) -> None:
        super().__init__()
        self.position_id = position_id
        self.bot_id = bot_id
        self.profit = profit
        self.profit_percentage = profit_pct

class BotActiveStateChangedEvent(DomainEvent):
    bot_id: Id
    is_active: bool

    def __init__(self, bot_id: Id, is_active: bool) -> None:
        super().__init__()
        self.bot_id = bot_id
        self.is_active = is_active
