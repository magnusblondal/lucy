from pydantic import BaseModel
from datetime import datetime

from lucy.model.id import Id
from lucy.model.signal import Signal


class SignalIncoming(BaseModel):
    bot_id: str
    strategy: str
    ticker: str
    side: str
    signal_type: str
    interval: str
    bar_open_time: datetime
    signal_time: datetime
    close: float

    def to_model(self) -> Signal:
        return Signal.create_new(
            Id(self.bot_id),
            self.strategy,
            self.ticker,
            self.side,
            self.signal_type,
            self.interval,
            self.bar_open_time,
            self.signal_time,
            self.close
        )
