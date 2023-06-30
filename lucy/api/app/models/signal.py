from datetime import datetime
from .id import Id

class Signal:
    id: Id
    position_id: Id
    bot_id: Id
    strategy: str
    ticker: str
    side: str
    signal_type: str
    interval: str
    bar_open_time: datetime
    signal_time: datetime
    close: float
    created_at: datetime = None

    def __init__(self, id, position_id, bot_id, strategy, ticker, side, signal_type, interval, bar_open_time, signal_time, close) -> None:
        self.id = id
        self.position_id = position_id
        self.bot_id = bot_id
        self.strategy = strategy
        self.ticker = ticker
        self.side = side
        self.signal_type = signal_type
        self.interval = interval
        self.bar_open_time = bar_open_time
        self.signal_time = signal_time
        self.close = close

    @staticmethod
    def create_new(bot_id, strategy, ticker, side, signal_type, interval, bar_open_time, signal_time, close) -> 'Signal':
        return Signal(Id.make(), None, bot_id, strategy, ticker, side, signal_type, interval, bar_open_time, signal_time, close)
    
    def is_entry(self):
        return self.signal_type == "entry"

    def is_add_funds(self):
        return self.signal_type == "add_funds"
    
    def is_close(self):
        return self.signal_type == "close"
    
    def is_long(self):
        return self.side.lower() == "long"
    
    def __str__(self) -> str:
        return f"Signal:: strategy: {self.strategy}, ticker: {self.ticker}, side: {self.side}, signal_type: {self.signal_type}, interval: {self.interval}, bar_open_time: {self.bar_open_time}, signal_time: {self.signal_time}, close: {self.close}"
