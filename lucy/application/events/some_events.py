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
    def __init__(
        self,
        position_id: Id,
        bot_id: Id,
        symbol: Symbol,
        qty: float,
        side: str
    ) -> None:
        super().__init__()
        self.position_id = position_id
        self.bot_id = bot_id
        self.symbol = symbol if isinstance(symbol, Symbol) else Symbol(symbol)
        self.qty = qty
        self.side = side

    def __str__(self) -> str:
        bot = f"Bot: {self.bot_id}"
        symbol = f"Symbol: {self.symbol}"
        qty = "Qty: {self.qty}  Side: {self.side}"
        return super().__str__() + f"PositionEntryEvent:: {bot} {symbol} {qty}"


class AddFundsEvent(DomainEvent):
    def __init__(self, position_id: Id, bot_id: Id, amount: float) -> None:
        super().__init__()
        self.position_id = position_id
        self.bot_id = bot_id
        self.amount = amount

    def __str__(self) -> str:
        bot = "Bot: {self.bot_id}"
        amount = f"Amount: {self.amount}"
        return super().__str__() + f"AddFundsEvent:: {bot}  {amount}"


class PositionExitEvent(DomainEvent):
    def __init__(self, position_id: Id) -> None:
        super().__init__()
        self.position_id = position_id

    def __str__(self) -> str:
        pos = f"Position: {self.position_id}"
        return super().__str__() + f"PositionExitEvent:: {pos}"


class ProfitCalculatedEvent(DomainEvent):
    def __init__(
        self,
        position_id: Id,
        bot_id: Id,
        profit: float,
        profit_pct: float
    ) -> None:
        super().__init__()
        self.position_id = position_id
        self.bot_id = bot_id
        self.profit = float(profit)
        self.profit_percentage = float(profit_pct)

    def __str__(self) -> str:
        pos = f"Position: {self.position_id}"
        bot = f"Bot: {self.bot_id}"
        profit = f"Profit: ${self.profit} - {self.profit_percentage}%"
        mssg = f"ProfitCalculatedEvent:: {pos}  {bot} {profit}"
        return super().__str__() + mssg


class BotActiveStateChangedEvent(DomainEvent):
    bot_id: Id
    is_active: bool

    def __init__(self, bot_id: Id, is_active: bool) -> None:
        super().__init__()
        self.bot_id = bot_id
        self.is_active = is_active

    def __str__(self) -> str:
        bot = f"Bot: {self.bot_id}"
        active = f"Active: {self.is_active}"
        mssg = f"BotActiveStateChangedEvent:: {bot} {active}"
        return super().__str__() + mssg
