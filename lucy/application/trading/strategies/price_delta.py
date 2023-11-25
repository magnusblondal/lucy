import pandas as pd
import pandas_ta as ta

from lucy.model.interval import Interval
from lucy.main_logger import MainLogger
import lucy.application.trading.chart as chart
from lucy.model.signal import Signal
from .strategy import Strategy


class EntrySignal(object):
    pass


class PriceDelta(Strategy):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.logger = MainLogger.get_logger(__name__)
        self.target = 1.0
        self.add_funds_threshold = 1.0
        self.window = 500
        self.std_dev_level = 2.0

    def validate_entry(
        self,
        df: pd.DataFrame,
        pair: str,
        interval: Interval
    ) -> Signal:
        df['delta'] = df['close'] - df['close'].shift(1)
        w = df['delta'].rolling(window=self.window)
        df['std'] = w.std()
        df['std_dev_level'] = w.std() * self.std_dev_level
        df['std_dev_level_below'] = -df['std_dev_level']

        df['entry_long'] = df.close < df['close'].shift(
            1) - df['std_dev_level']
        df['entry_short'] = df.close > df['close'].shift(
            1) + df['std_dev_level']

        entry_signal = df["entry_long"].iloc[-1]
        time = df.index[-1].to_pydatetime()  # type: ignore
        close = df["close"].iloc[-1]

        if entry_signal:
            self._chart_entry(df, pair, interval)

        self.logger.info(
            f"{pair} Entry: Close: {close:.3f} | Entry: {entry_signal}")
        return self._make_signal(
            entry_signal,
            "entry",
            time,
            close,
            pair,
            interval
        )

    def validate_add_funds(
        self,
        df: pd.DataFrame,
        last_order_price: float,
        pair: str,
        interval: Interval
    ) -> Signal:
        rsi_length = 14
        cross_up_trigger = 50
        rsi_col_name = f"RSI_{rsi_length}"
        strategy = ta.Strategy(
            name="strategy_PriceDelta_SO",
            ta=[{
                "close":    'close',
                "kind":     'rsi',
                "length":   rsi_length
            }]
        )
        df.ta.strategy(strategy)
        soThreshold = last_order_price * (1 - (self.add_funds_threshold / 100))

        df['last_order_price'] = last_order_price
        df["rsi_cross_up"] = (df[rsi_col_name] > cross_up_trigger) & (
            df[rsi_col_name].shift() < cross_up_trigger)
        df['so_threshold'] = soThreshold
        df['RSI_50'] = 50.
        df['cross_up_trigger'] = cross_up_trigger
        df['so_price_below_threshold'] = df['close'] < df['so_threshold']
        df['so_signal'] = (
            df['so_price_below_threshold'] is True
        ) & (df['rsi_cross_up'] is True)

        close = df["close"].iloc[-1]
        time = df.index[-1].to_pydatetime()  # type: ignore
        so_signal = df['so_signal'].iloc[-1]

        # so_signal = True

        if so_signal:
            self._chart_add_funds(df, pair, interval, rsi_col_name)

        s = "{} Add Funds: {} {} | {} | {} | {}".format(
            pair,
            f"Signal: {so_signal}",
            f"Threshold: {soThreshold}",
            f"Close: {close:.3f}",
            f"Below level: {df['so_price_below_threshold'].iloc[-1]}",
            f"Below RSI threshold: {df['so_price_below_threshold'].iloc[-1]}"
        )
        self.logger.info(s)
        return self._make_signal(
            so_signal,
            "add_funds",
            time,
            close,
            pair,
            interval
        )

    def validate_exit(
        self,
        df: pd.DataFrame,
        avg_price: float,
        pair: str,
        interval: Interval
    ) -> Signal:
        tp_rsi_cross_down_trigger = 55.
        rsi_length = 14

        rsi_col_name = f"RSI_{rsi_length}"

        strategy = ta.Strategy(
            name="strategy_PriceDelta_TP",
            ta=[{
                "close":    'close',
                "kind":     'rsi',
                "length":   rsi_length
            }]
        )
        df.ta.strategy(strategy)
        take_profit_level = avg_price + (avg_price * (self.target / 100))

        df['tp_rsi_cross_down_trigger'] = tp_rsi_cross_down_trigger
        df['take_profit_price'] = take_profit_level
        df["rsi_tp_cross_down"] = (
            df[rsi_col_name] < tp_rsi_cross_down_trigger
        ) & (
            df[rsi_col_name].shift() > tp_rsi_cross_down_trigger)
        df['above_tp_price'] = df['close'] > df['take_profit_price'].shift()
        df['tp_trigger'] = df['rsi_tp_cross_down'] & df['above_tp_price']
        close = df["close"].iloc[-1]
        time = df.index[-1].to_pydatetime()  # type: ignore
        tp_signal = df['tp_trigger'].iloc[-1]

        # tp_signal = True

        if tp_signal:
            self._chart_tp(df, avg_price, pair, interval, rsi_col_name)
        # s = f"{pair} TP: Level: {take_profit_level:.3f} | Close: {close:.3f} | Above level: {df['above_tp_price'].iloc[-1]} | TP Signal: {tp_signal}"
        s = "{} TP: {} | {} | {} | {}".format(
            pair,
            f"Level: {take_profit_level:.3f}",
            f"Close: {close:.3f}",
            f"Above level: {df['above_tp_price'].iloc[-1]}",
            f"TP Signal: {tp_signal}"
        )
        self.logger.info(s)
        return self._make_signal(
            tp_signal,
            "close",
            time,
            close,
            pair,
            interval
        )

    # region Charting

    def _chart_add_funds(
        self,
        df: pd.DataFrame,
        pair: str,
        interval: Interval,
        rsi_col_name: str
    ):
        chart_data = df[['close', 'so_threshold', 'last_order_price']]
        rsi_data = ('cross_up_trigger',
                    df[['RSI_50', 'cross_up_trigger', rsi_col_name]])
        so_signal = ('so_signal', df[['so_signal']])
        so_price_below_threshold = (
            'so_price_below_threshold', df[['so_price_below_threshold']])
        rsi_cross_up_d = ('rsi_cross_up', df[['rsi_cross_up']])

        s = [rsi_data, rsi_cross_up_d, so_price_below_threshold, so_signal]
        name = self._chart_title(pair, interval, 'add_funds')
        chart.chart(name, chart_data, s)

    # TODO: 2x
    # def _chart_add_funds(
    #     self,
    #     df: pd.DataFrame,
    #     pair: str,
    #     interval: Interval
    # ):
    #     chart_data = df[['close']]
    #     s = []
    #     name = self._chart_title(pair, interval, 'add_funds')
    #     chart.chart(name, chart_data, s)

    def _chart_tp(
        self,
        df: pd.DataFrame,
        avg_price: float,
        pair: str,
        interval: Interval,
        rsi_col_name: str
    ):
        df['RSI_50'] = 50.
        df['position_avg_price'] = avg_price
        chart_data = df[['close', 'position_avg_price', 'take_profit_price']]
        tp_rsi_cross_down_trigger = ('tp_rsi_cross_down_trigger', df[[
            'RSI_50',
            'tp_rsi_cross_down_trigger',
            rsi_col_name,
        ]])
        tp_trigger = ('tp_trigger', df[['tp_trigger']])
        rsi_tp_cross_down = ('rsi_tp_cross_down', df[['rsi_tp_cross_down']])
        above_tp_price = ('above_tp_price', df[['above_tp_price']])
        s = [tp_rsi_cross_down_trigger,
             rsi_tp_cross_down, above_tp_price, tp_trigger]
        name = self._chart_title(pair, interval, 'tp')
        chart.chart(name, chart_data, s)

    # endregion

