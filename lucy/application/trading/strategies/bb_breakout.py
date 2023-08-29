from datetime import datetime
import pandas as pd
import numpy as np
import pandas_ta as ta

from lucy.model.interval import Interval
from lucy.main_logger import MainLogger
import lucy.application.trading.chart as chart
from lucy.model.signal import Signal
from .strategy import Strategy

class EntrySignal(object):
    pass

class BBbreakout(Strategy):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.target = 1.0
        self.add_funds_threshold = 1.0
        self.logger = MainLogger.get_logger(__name__)

    def validate_entry(self, df: pd.DataFrame, pair: str, interval: Interval) -> Signal:
        # BBands
        std_fast        = 1.0
        std_slow        = 2.0
        length          = 55 # 15
        mamode          ="sma" #"ema"
        offset          = 0

        # Moving Averages
        fast_ma_length  = 100
        slow_ma_length  = 200
        ma_type         = "sma"

        # Column names
        # - Moving Averages
        fastMa = f"{ma_type.upper()}_{fast_ma_length}"
        slowMa = f"{ma_type.upper()}_{slow_ma_length}"
        # - Fast BBands
        bbu = f"BBU_{length}_{std_fast}" # Upper
        bbm = f"BBM_{length}_{std_fast}" # Middle
        bbl = f"BBL_{length}_{std_fast}" # Lower
        bbb = f"BBB_{length}_{std_fast}" # Bandwidth
        bbp = f"BBP_{length}_{std_fast}" # Percent
        # - Slow BBands
        bbu_slow = f"BBU_{length}_{std_slow}" # Upper

        strategy = ta.Strategy(
            name="strategy_BBbreakout",
            ta=[{
                "close":    'close', 
                "kind":     "bbands", 
                "length":   length,
                "std":      std_fast,
                "mamode":   mamode,
                "ddof":     offset,
            }, {
                "close":    'close', 
                "kind":     "bbands", 
                "length":   length,
                "std":      std_slow,
                "mamode":   mamode,
                "ddof":     offset,
            }, {
                "close":    'close',
                "kind":     ma_type, 
                "length":   fast_ma_length
            }, {
                "close":    'close',
                "kind":     ma_type, 
                "length":   slow_ma_length
            },]
        )
        df.ta.strategy(strategy)
        # fast ma is above slow ma
        df["up_trend"]          = df[fastMa] > df[slowMa]
        # fast ma is crossing up over slow ma
        df["ema_cross_up"]      = (df[fastMa] > df[slowMa]) & (df[fastMa].shift() < df[slowMa].shift())
        # fast ma is crossing down under slow ma
        # closing above fast upper band
        df["bb_breakout"]       = np.where(df['close'] > df[bbu].shift(), True, False)
        # closing below slow upper band
        df["bb_within_slow"]    = np.where(df['close'] < df[bbu_slow].shift(), True, False)
        # this is the first close above the fast upper band
        df["bb_signal"]         = (df['bb_breakout'] == True) & (df['bb_breakout'].shift() == False)
        
        # are going up from basis, rather than down from beyond the upper band
        # coming down from above fast upper band
        df["bbu_slow_cross_down"]    = (df['close'] < df[bbu_slow]) & (df['close'].shift() > df[bbu_slow].shift())
        
        # close crossing up over middle band
        df["bbm_cross_up"]    = (df['close'] > df[bbm]) & (df['close'].shift() < df[bbm].shift())

        # setur indexinn (tímann) þegar förum upp yfir middle band
        df['counter_bbm_cross_up'] = df.index.where(df["bbm_cross_up"])
        # fyllum inn með síðasta gildi
        df['counter_bbm_cross_up'].fillna(method="ffill", inplace=True)

        # setur indexinn (tímann) þegar förum niður fyrir slow upper band
        df['counter_bbu_slow_cross_down'] = df.index.where(df.bbu_slow_cross_down)
        df['counter_bbu_slow_cross_down'].fillna(method="ffill", inplace=True)
        # fá tímafildið til að geta gert timedelta reikninga
        df['date'] = pd.to_datetime(df.index)
        # reikna hvað er langt frá því að fórum upp yfir middle band
        df['delta_bbm_cross_up']            = ( df['date'].sub(df['counter_bbm_cross_up']).astype('timedelta64[s]').dt.total_seconds() ) +1
        # reikna hvað er langt frá því að fórum niður fyrir slow upper band
        df['delta_bbu_slow_cross_down']     = ( df['date'].sub(df['counter_bbu_slow_cross_down']).astype('timedelta64[s]').dt.total_seconds() ) +1
        # fórum við síðast upp yfir middle band
        df['bbm_cross_up_last']             = df['delta_bbm_cross_up'] < df['delta_bbu_slow_cross_down'].fillna(float('inf'))
        # drop columns
        df.drop(['counter_bbm_cross_up', 'counter_bbu_slow_cross_down', 'date'], axis=1,inplace=True)
        
        # Uptrend and BB breakout and BB within slow and coming up from fast basis
        df["entry_signal"]      = (df["up_trend"] == True) & (df["bb_signal"] == True) & (df["bb_within_slow"] == True) & (df["bbm_cross_up_last"] == True)

        entry_signal = df["entry_signal"].iloc[-1]
        time = df.index[-1].to_pydatetime() # type: ignore 
        close = df["close"].iloc[-1]
        
        entry_signal = True
        
        if entry_signal:
            self._chart_entry(df, pair, interval, bbm, bbu, bbu_slow, slowMa, fastMa)
        
        s = f"{pair} Entry: Close: {close:.3f} | BBM: {df[bbm].iloc[-1]:.3f} | BBU_fast: {df[bbu].iloc[-1]:.3f} | BBU_slow: {df[bbu_slow].iloc[-1]:.3f} | Uptrend: {df['up_trend'].iloc[-1]} | BBbreakout: {df['bb_breakout'].iloc[-1]} | Within slow: {df['bb_within_slow'].iloc[-1]} | Entry: {entry_signal}"
        self.logger.info(s)
        return self._make_signal(entry_signal, "entry", time, close, pair, interval) 

    def validate_exit(self, df: pd.DataFrame, avg_price: float, pair: str, interval: Interval) -> Signal:
        tp_rsi_cross_down_trigger   = 55.
        rsi_length                  = 14

        rsi_col_name = f"RSI_{rsi_length}"

        strategy = ta.Strategy(
            name="strategy_BBbreakout_TP",
            ta=[ {
                "close":    'close',
                "kind":     'rsi', 
                "length":   rsi_length
            }]
        )
        df.ta.strategy(strategy)        
        take_profit_level = avg_price + (avg_price * (self.target / 100))

        df['tp_rsi_cross_down_trigger'] = tp_rsi_cross_down_trigger
        df['take_profit_price']         = take_profit_level
        df["rsi_tp_cross_down"]         = (df[rsi_col_name] < tp_rsi_cross_down_trigger) & (df[rsi_col_name].shift() > tp_rsi_cross_down_trigger)
        df['above_tp_price']            = df['close'] > df['take_profit_price'].shift()
        df['tp_trigger']                = df['rsi_tp_cross_down'] & df['above_tp_price']        
        close           = df["close"].iloc[-1]
        time            = df.index[-1].to_pydatetime() # type: ignore
        tp_signal       = df['tp_trigger'].iloc[-1]
        
        tp_signal = True

        if tp_signal:
            self._chart_tp(df, avg_price, pair, interval, rsi_col_name)
        s = f"{pair} TP: Level: {take_profit_level:.3f} | Close: {close:.3f} | Above level: {df['above_tp_price'].iloc[-1]} | TP Signal: {tp_signal}"
        self.logger.info(s)
        return self._make_signal(tp_signal, "close", time, close, pair, interval)
    
    
    def validate_add_funds(self, df: pd.DataFrame, last_order_price: float, pair: str, interval: Interval) -> Signal:
        rsi_length = 14
        cross_up_trigger = 50
        rsi_col_name = f"RSI_{rsi_length}"
        strategy = ta.Strategy(
            name="strategy_BBbreakout_SO",
            ta=[ {
                "close":    'close',
                "kind":     'rsi', 
                "length":   rsi_length
            }]
        )
        df.ta.strategy(strategy)
        soThreshold = last_order_price * (1 - (self.add_funds_threshold / 100) )

        df['last_order_price']          = last_order_price
        df["rsi_cross_up"]              = (df[rsi_col_name] > cross_up_trigger) & (df[rsi_col_name].shift() < cross_up_trigger)
        df['so_threshold']              = soThreshold
        df['RSI_50']                    = 50.
        df['cross_up_trigger']          = cross_up_trigger
        df['so_price_below_threshold']  = df['close'] < df['so_threshold']
        df['so_signal']                 = (df['so_price_below_threshold'] == True) & (df['rsi_cross_up'] == True)

        close = df["close"].iloc[-1]
        time = df.index[-1].to_pydatetime() # type: ignore
        so_signal = df['so_signal'].iloc[-1]

        # so_signal = True

        if so_signal:
            self._chart_add_funds(df, pair, interval, rsi_col_name)

        s = f"{pair} Add Funds: Signal: {so_signal} Threshold: {soThreshold} | Close: {close:.3f} | Below level: {df['so_price_below_threshold'].iloc[-1]} | Below RSI threshold: {df['so_price_below_threshold'].iloc[-1]}"
        self.logger.info(s)
        return self._make_signal(so_signal, "add_funds", time, close, pair, interval)


    #region Charting

    def _chart_title(self, pair: str, interval: Interval, action: str):
        now = datetime.now().strftime("%y.%m.%d_%H:%M:%S")
        return f"{pair}_{interval}_{action.upper()}_{now}"
        
        
    def _chart_entry(self, df: pd.DataFrame, pair: str, interval: Interval, bbm: str, bbu: str, bbu_slow: str, slowMa: str, fastMa: str):
        chart_data          = df[['close', bbm, bbu, bbu_slow]]
        trend               = ('trend', df[['close', slowMa, fastMa]])
        entry_signal        = ('entry_signal', df[['entry_signal']] )
        bb_signal           = ('bb_signal', df[['bb_signal']] )
        bb_breakout         = ('bb_breakout', df[['bb_breakout']] )
        bb_within_slow      = ('bb_within_slow', df[['bb_within_slow']] )
        up_trend            = ('up_trend', df[['up_trend']] )
        bbm_cross_up_last   = ('bbm_cross_up_last', df[['bbm_cross_up_last']] )

        signals         = [trend, entry_signal, bb_breakout, bb_signal, bb_within_slow, up_trend, bbm_cross_up_last]
        name            = self._chart_title(pair, interval, 'entry')
        chart.chart(name, chart_data, signals)

    def _chart_add_funds(self, df: pd.DataFrame, pair: str, interval: Interval, rsi_col_name: str):
        chart_data                  = df[['close', 'so_threshold', 'last_order_price']]
        rsi_data                    = ('cross_up_trigger', df[['RSI_50', 'cross_up_trigger', rsi_col_name]])
        so_signal                   = ('so_signal', df[['so_signal']])
        so_price_below_threshold    = ('so_price_below_threshold', df[['so_price_below_threshold']])
        rsi_cross_up_d              = ('rsi_cross_up', df[['rsi_cross_up']])
        s = [rsi_data, rsi_cross_up_d, so_price_below_threshold, so_signal]
        name = self._chart_title(pair, interval, 'add_funds')
        chart.chart(name, chart_data, s)

    def _chart_tp(self, df: pd.DataFrame, avg_price: float, pair: str, interval: Interval, rsi_col_name: str):
        df['RSI_50']                = 50.
        df['position_avg_price']    = avg_price
        chart_data                  = df[['close', 'position_avg_price', 'take_profit_price']]
        tp_rsi_cross_down_trigger   = ('tp_rsi_cross_down_trigger', df[['RSI_50', 'tp_rsi_cross_down_trigger', rsi_col_name]])
        tp_trigger                  = ('tp_trigger', df[['tp_trigger']])
        rsi_tp_cross_down           = ('rsi_tp_cross_down', df[['rsi_tp_cross_down']])
        above_tp_price              = ('above_tp_price', df[['above_tp_price']])
        s = [tp_rsi_cross_down_trigger, rsi_tp_cross_down, above_tp_price, tp_trigger]
        name = self._chart_title(pair, interval, 'tp')
        chart.chart(name, chart_data, s)
    
    #endregion