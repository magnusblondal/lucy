from datetime import datetime
from lucy.model.interval import Interval

from lucy.model.signal import Signal


class Strategy(object):
    def __init__(self, name) -> None:
        self.name = name

    def _make_signal(self, valid: bool, type:str, time: datetime, close: float, pair: str, interval: Interval, side: str = 'long') -> Signal:
        return Signal.create_new(
            None, # self.id,
            self.name,
            pair, 
            side,
            type,
            interval,
            time,
            time,
            close) if valid else Signal.empty(time, close)