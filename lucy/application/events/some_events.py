from aiosignal import Signal

from lucy.model.id import Id
from lucy.model.symbol import Symbol
from .event import DomainEvent

class SignalEvent(DomainEvent):
    signal: Signal
    position_id: Id

    def __init__(self, signal: Signal, position_id: Id) -> None:
        super().__init__()
        self.signal = signal
        self.position_id = position_id
        self.bot_id = signal.bot_id

    def __str__(self) -> str: 
        return f"SignalEvent:: Bot: {self.bot_id}  Signal: {self.signal}"
    
class PositionEntryEvent(DomainEvent):
    def __init__(self, position_id: Id, bot_id: Id, symbol: Symbol, qty: float, side: str) -> None:
        super().__init__()
        self.position_id = position_id
        self.bot_id = bot_id
        self.symbol = symbol if isinstance(symbol, Symbol) else Symbol(symbol)
        self.qty = qty
        self.side = side
    
    def __str__(self) -> str:
        return super().__str__() + f"PositionEntryEvent:: Bot: {self.bot_id}  Symbol: {self.symbol}  Qty: {self.qty}  Side: {self.side}"


class AddFundsEvent(DomainEvent):
    def __init__(self, position_id: Id, bot_id: Id, amount: float) -> None:
        super().__init__()
        self.position_id = position_id
        self.bot_id = bot_id
        self.amount = amount

    def __str__(self) -> str:
        return super().__str__() + f"AddFundsEvent:: Bot: {self.bot_id}  Amount: {self.amount}"

class PositionExitEvent(DomainEvent):   
    def __init__(self, position_id: Id) -> None:
        super().__init__()
        self.position_id = position_id

    def __str__(self) -> str:
        return super().__str__() + f"PositionExitEvent:: Position: {self.position_id}"

class ProfitCalculatedEvent(DomainEvent):
    def __init__(self, position_id: Id, bot_id: Id, profit: float, profit_pct: float) -> None:
        super().__init__()
        self.position_id = position_id
        self.bot_id = bot_id
        self.profit = float(profit)
        self.profit_percentage = float(profit_pct)
    
    def __str__(self) -> str:
        return super().__str__() + f"ProfitCalculatedEvent:: Position: {self.position_id}  Bot: {self.bot_id}  Profit: ${self.profit} - {self.profit_percentage}%"

class BotActiveStateChangedEvent(DomainEvent):
    bot_id: Id
    is_active: bool

    def __init__(self, bot_id: Id, is_active: bool) -> None:
        super().__init__()
        self.bot_id = bot_id
        self.is_active = is_active

    def __str__(self) -> str:
        return super().__str__() + f"BotActiveStateChangedEvent:: Bot: {self.bot_id}  Active: {self.is_active}"
