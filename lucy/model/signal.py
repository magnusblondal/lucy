from datetime import datetime
from lucy.model.id import Id
from lucy.model.interval import Interval


class Signal:
    id: Id
    position_id: Id
    bot_id: Id
    strategy: str
    ticker: str
    side: str
    signal_type: str
    interval: Interval
    bar_open_time: datetime
    signal_time: datetime
    close: float
    created_at: datetime

    def __init__(
        self,
        id,
        position_id,
        bot_id,
        strategy,
        ticker,
        side,
        signal_type,
        interval: Interval,
        bar_open_time,
        signal_time,
        close
    ) -> None:
        self.id = id
        self.position_id = position_id
        self.bot_id = bot_id
        self.strategy = strategy
        self.ticker = ticker
        self.side = side
        self.signal_type = signal_type
        self.interval = Interval(interval) if isinstance(
            interval, str) else interval
        self.bar_open_time = bar_open_time
        self.signal_time = signal_time
        self.close = close

    @staticmethod
    def create_new(
        bot_id,
        strategy,
        ticker,
        side,
        signal_type,
        interval,
        bar_open_time,
        signal_time,
        close
    ) -> 'Signal':
        return Signal(
            Id.make(),
            None,
            bot_id,
            strategy,
            ticker,
            side,
            signal_type,
            interval,
            bar_open_time,
            signal_time,
            close
        )

    def is_entry(self):
        return self.signal_type == "entry"

    def is_add_funds(self):
        return self.signal_type == "add_funds"

    def is_close(self):
        return self.signal_type == "close"

    def is_long(self):
        return self.side.lower() == "long"

    def __str__(self) -> str:
        return f"Signal:: '{self.strategy}' {self.ticker} {self.side.upper()} {self.signal_type.upper()} '{self.interval}' close: {self.close} id: {self.id} pos: {self.position_id} bot: {self.bot_id} bar_open_time: {self.bar_open_time} signal_time: {self.signal_time}"

    @staticmethod
    def empty(time: datetime, close: float) -> 'Signal':
        return Signal(
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            time,
            close
        )

    def is_empty(self) -> bool:
        return self.id is None and self.position_id is None and self.bot_id is None and self.strategy is None and self.ticker is None and self.side is None and self.signal_type is None

    def is_valid(self) -> bool:
        return not self.is_empty()


class Signals(list[Signal]):
    def __init__(self, signals: list[Signal] = None) -> None:
        super().__init__(signals or [])

