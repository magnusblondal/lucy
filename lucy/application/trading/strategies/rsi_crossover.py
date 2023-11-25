from datetime import datetime
import pandas as pd
import pandas_ta as ta

from lucy.model.interval import Interval
import lucy.application.trading.chart as chart
from lucy.model.signal import Signal
from .strategy import Strategy
# from lucy.main_logger import MainLogger


class RsiCrossover(Strategy):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)
        # logger = MainLogger.get_logger(__name__)

    def validate_entry(
        self,
        df: pd.DataFrame,
        pair: str,
        interval: Interval
    ) -> Signal:
        fast_rsi_length = 14
        slow_rsi_length = 28

        strategy = ta.Strategy(
            name="strategy_BBbreakout",
            ta=[{
                "close":    'close',
                "kind":     'rsi',
                "length":   fast_rsi_length
            }, {
                "close":    'close',
                "kind":     'rsi',
                "length":   slow_rsi_length
            },]
        )
        df.ta.strategy(strategy)

    def validate_add_funds(
        self,
        df: pd.DataFrame,
        last_order_price: float,
        pair: str,
        interval: Interval
    ) -> Signal:
        pass

    def validate_exit(
        self,
        df: pd.DataFrame,
        avg_price: float,
        pair: str,
        interval: Interval
    ) -> Signal:
        pass

    # region Charting

    def _chart_title(self, pair: str, interval: Interval, action: str):
        now = datetime.now().strftime("%y.%m.%d_%H:%M:%S")
        return f"{self.name}_{pair}_{interval}_{action.upper()}_{now}"

    def _chart_entry(self, df: pd.DataFrame, pair: str, interval: Interval):
        chart_data = df[['close']]
        signals = []
        name = self._chart_title(pair, interval, 'entry')
        chart.chart(name, chart_data, signals)

    def _chart_add_funds(
        self,
        df: pd.DataFrame,
        pair: str,
        interval: Interval
    ):
        chart_data = df[['close']]
        s = []
        name = self._chart_title(pair, interval, 'add_funds')
        chart.chart(name, chart_data, s)

    def _chart_tp(
        self,
        df: pd.DataFrame,
        avg_price: float,
        pair: str,
        interval: Interval
    ):
        chart_data = df[['close']]
        s = []
        name = self._chart_title(pair, interval, 'tp')
        chart.chart(name, chart_data, s)

    # endregion

