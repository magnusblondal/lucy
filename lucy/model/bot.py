import pandas as pd

from lucy.cli.views.position_view import PositionsView
from .create_bot import CreateDcaBot, EditDcaBot
from lucy.model.domain_model import DomainModel
from lucy.model.position import Position, Positions
from lucy.model.signal import Signal
from lucy.model.interval import Interval, Intervals
from lucy.model.id import Id
from lucy.model.symbol import Symbol, Symbols
from lucy.application.events.event import DomainEvent
from lucy.application.events.some_events import BotActiveStateChangedEvent
from lucy.application.trading.exchange import Exchange
import lucy.application.trading.strategies as strategies
from lucy.main_logger import MainLogger


class Bot(DomainModel):
    def __init__(
        self,
        id: Id,
        name: str,
        description: str,
        active: bool,
        num_positions_allowed: int
    ) -> None:
        super().__init__(id)
        self.name = name
        self.description = description
        self.active = active
        self.num_positions_allowed = num_positions_allowed


class DcaBot(Bot):

    def __init__(
        self,
        id: Id,
        name: str,
        description: str,
        active: bool,
        capital: float,
        entry_size: float,
        so_size: float,
        max_safety_orders: int,
        allow_shorts: bool,
        num_positions_allowed: int,
        interval: Interval,
        strategy: str,
        symbols: Symbols = None
    ) -> None:
        super().__init__(id, name, description, active, num_positions_allowed)
        self.capital = capital
        self.entry_size = entry_size
        self.so_size = so_size
        self.max_safety_orders = max_safety_orders
        self.allow_shorts = allow_shorts
        self.positions = Positions()
        self.interval = interval
        self.symbols = symbols or Symbols()
        self.logger = MainLogger.get_logger(__name__)
        self.strategy = strategies.make(strategy)

    # TODO: cyclomatic complexity
    def tick(self, intervals: Intervals, exchange: Exchange):
        if not intervals.has(self.interval):
            return

        for s in self.symbols:
            try:
                symbol = s.pf()
                df = exchange.ohlc(symbol, self.interval, 'trade')
                if df.empty:
                    self.logger.warning(
                        "Bot {} {} {} {} df is empty, no ohlc data".format(
                            self.name,
                            symbol,
                            self.interval,
                            symbol
                        )
                    )
                    return

                # Ath hvort erum með position
                #   ef ekki, þá athuga hvort er entry event
                has_open, pos = self.positions.has_open(symbol)
                if has_open:
                    PositionsView().debug(
                        self.name,
                        symbol,
                        self.positions,
                        'check for exit'
                    )
                    if not self._check_for_close(symbol, df, pos):
                        self._check_for_add_funds(symbol, df, pos)
                    else:
                        so_signal = self.strategy.validate_add_funds(
                            df, pos.last_order_price(), symbol, self.interval)
                        if so_signal.is_valid():
                            print(
                                f"Bot ADD FUNDS {self.name} {symbol} {self.interval} _ADD FUNDS_ {symbol} {so_signal.signal_time} {so_signal.close}")
                            so_signal.bot_id = self.id
                            so_signal.position_id = pos.id
                            if pos.can_add_safety_order(self.max_safety_orders):
                                self._add_funds2(pos, so_signal)
                            else:
                                self.logger.info(
                                    f"Bot {self.name} {symbol} {self.interval} {so_signal.signal_time} {so_signal.close} can't add funds, max safety orders reached")
                                print(
                                    f"Bot {self.name} {symbol} {self.interval} can't add funds, max safety orders reached")
                else:
                    self._check_for_entry(symbol, df)

            except Exception as e:
                m = "Error in DcaBot.tick {} {} {}".format(
                    self.name,
                    symbol,
                    self.interval
                )
                self.logger.error(m, exc_info=True)
                self.logger.error(f"DF: cols: {df.columns} \n {df.head(5)}")

    def _check_for_entry(self, symbol: Symbol, df: pd.DataFrame) -> bool:
        PositionsView().debug(
            self.name,
            symbol,
            self.positions,
            'check for entry'
        )
        entry_signal = self.strategy.validate_entry(df, symbol, self.interval)
        if entry_signal.is_valid():
            entry_signal.bot_id = self.id
            self._new_position(entry_signal)
            self.logger.info(
                f"Bot entered Position: {self.name} {symbol} {self.interval} {entry_signal.signal_time} {entry_signal.close} entry_signal: {entry_signal}")
            print(
                f"Bot entered Position: {self.name} {symbol} {self.interval}")
            return True
        return False

    def _check_for_close(
        self,
        symbol: Symbol,
        df: pd.DataFrame,
        pos: Position
    ) -> bool:
        avg_entry_price = pos.average_price()
        close_signal = self.strategy.validate_exit(
            df, avg_entry_price, symbol, self.interval)
        if close_signal.is_valid():
            close_signal.bot_id = self.id
            close_signal.position_id = pos.id
            mssg = f"Bot EXIT {self.name} {self.interval} _SELL_ {symbol}"
            print(mssg)
            self._close(close_signal)
            return True
        return False

    def _check_for_add_funds(
        self,
        symbol: Symbol,
        df: pd.DataFrame,
        pos: Position
    ) -> bool:
        so_signal = self.strategy.validate_add_funds(
            df, pos.last_order_price(), symbol, self.interval)
        if so_signal.is_valid():
            print(
                f"Bot ADD FUNDS {self.name} {symbol} {self.interval} _ADD FUNDS_ {symbol} {so_signal.signal_time} {so_signal.close}")
            so_signal.bot_id = self.id
            so_signal.position_id = pos.id
            if pos.can_add_safety_order(self.max_safety_orders):
                self._add_funds2(pos, so_signal)
            else:
                self.logger.info(
                    f"Bot {self.name} {symbol} {self.interval} {so_signal.signal_time} {so_signal.close} can't add funds, max safety orders reached")
                print(
                    f"Bot {self.name} {symbol} {self.interval} can't add funds, max safety orders reached")
            return True
        return False

    # ef ekki position opin:
    #   spurja Strategy hvort er entry event:
    #       ef svo er, þá búa til nýtt position
    # ef position opin:
    #   spurja Strategy hvort er exit event:
    #       ef svo er, þá loka position

    # exit getur orðið:
    #   tak profit
    #   - stop loss
    #   - take profit
    #   - trailing stop loss
    #   - trailing take profit

    @staticmethod
    def create_new(bot: CreateDcaBot):
        return DcaBot(Id(),
                      bot.name,
                      bot.description or "",
                      bot.active,
                      bot.capital,
                      bot.entry_size,
                      bot.so_size,
                      bot.max_safety_orders,
                      bot.allow_shorts,
                      bot.max_positions_allowed,
                      Interval(bot.interval),
                      bot.strategy,
                      Symbols.from_str(bot.symbols),
                      )

    def update(self, edit: EditDcaBot):
        self.name = edit.name
        self.description = edit.description or ""
        self.capital = edit.capital
        self.entry_size = edit.entry_size
        self.so_size = edit.so_size
        self.max_safety_orders = edit.max_safety_orders
        self.allow_shorts = edit.allow_shorts
        self.num_positions_allowed = edit.max_positions_allowed
        self.interval = Interval(edit.interval)
        self.symbols = Symbols.from_str(edit.symbols)
        self.strategy = strategies.make(edit.strategy)
        print(f"Bot {self.name} updated Strategy: {self.strategy.name}")

    def events(self) -> list[DomainEvent]:
        evs = self._events or []
        for p in self.positions:
            evs.extend(p.events())
        self._events = []
        return evs

    def _within_max_limit(self):
        num_open_pos = self.num_open_positions()
        return num_open_pos < self.num_positions_allowed

    def _position(self, id: Id) -> Position:
        ps = [position for position in self.positions if position.id == id]
        return ps[0] if len(ps) > 0 else None

    def _new_position(self, signal: Signal):
        print(
            f"-> Bot '{self.id}' handle '{signal.signal_type}' -- opna position")
        if self.positions is None:
            self.positions = Positions()

        has_open, pos = self.positions.has_open(signal.ticker)
        if has_open:
            print(
                f"-> Bot {self.id} handle {signal.signal_type} -- position already open for symbol {signal.ticker}")
            return

        if not self._within_max_limit():
            print(
                f"-> Bot {self.id} handle {signal.signal_type} -- max limit reached, cannot open position")
            return

        position = self.positions.create_new(signal)
        position.entry(signal, self.entry_size)

    def _add_funds2(self, position: Position, signal: Signal):
        print(f"-> Bot {self.id} handle {signal.signal_type} -- add funds")
        if position is not None:
            position.add_funds(signal, self.so_size, self.max_safety_orders)
        else:
            print(
                f"-> Bot {self.id} handle {signal.signal_type} -- No open position found, cannot add funds")

    # def _add_funds(self, signal: Signal):
    #     print(f"-> Bot {self.id} handle {signal.signal_type} -- add funds")
    #     if self.positions.is_empty():
    #         print(f"-> Bot {self.id} handle {signal.signal_type} -- No position available, cannot add funds")
    #         return
    #     position = self.positions.position_for_signal(signal)

    #     if position is not None:
    #         signal.position_id = position.id
    #         position.add_funds(signal, self.so_size, self.max_safety_orders)
    #     else:
    #         print(f"-> Bot {self.id} handle {signal.signal_type} -- No open position found, cannot add funds")

    def _close(self, signal: Signal):
        print(f"-> Bot {self.id} handle {signal.signal_type} -- loka position")
        if self.positions.is_empty():
            print(
                f"-> Bot {self.id} handle {signal.signal_type} -- No position available, cannot close")
            return
        position = self.positions.position_for_signal(signal)
        if position is not None:
            position.close(signal)
        else:
            print(
                f"-> Bot {self.id} handle {signal.signal_type} -- position not found, cannot close")

    def has_description(self) -> bool:
        return self.description is not None and len(self.description) > 0

    def audit(self):
        print(f"-> Bot {self.id} audit")
        if self.positions.is_empty():
            print(
                f"-> Bot {self.id} audit -- No position available, cannot audit")
            return

        unaudited = [
            position
            for position in self.positions
            if not position.is_audited()
        ]
        for position in unaudited:
            position.calculate_profit_loss()
        if len(unaudited) == 0:
            print(f"-> Bot {self.id} audit -- No positions to audit")

    def profit(self) -> float:
        '''Returns the total profit for all positions'''
        return self.positions.profit()

    def num_open_positions(self) -> int:
        '''Returns the number of currently open positions'''
        return len([
            position
            for position in self.positions
            if position.is_open()
        ])

    def handle(self, signal: Signal) -> tuple[bool, str]:
        '''Handle a signal'''
        if not self.active:
            print(
                "-> Bot {} handle {} -- bot is not active".format(
                    self.id,
                    signal.signal_type
                )
            )
            return (False, "Bot is not active")
        if signal.is_entry():
            self._new_position(signal)
        elif signal.is_add_funds():
            self._add_funds(signal)
        elif signal.is_close():
            self._close(signal)
        else:
            msg = "Bot {} handle {} -- unknown signal type".format(
                self.id,
                signal.signal_type
            )
            print(msg)
            return (False, msg)
        return (True, "OK")

    def has_positions(self) -> bool:
        return self.positions is not None and not self.positions.is_empty()

    def turn_off(self, liquidate: bool = False):
        ''''''
        self.active = False
        self._this_just_happened(
            BotActiveStateChangedEvent(self.id, self.active))

    def turn_on(self):
        self.active = True
        self._this_just_happened(
            BotActiveStateChangedEvent(self.id, self.active))

    def __str__(self) -> str:
        ds = '\n' + '\n'.join([f" {p}" for p in self.positions]
                              ) if self.has_positions() > 0 else "No Positions"
        shorts = "Allows shorts" if self.allow_shorts else "No shorts"
        return f"Bot {self.name} capital: {self.capital} entry size: {self.entry_size} so size: {self.so_size} max so's: {self.max_safety_orders} {shorts} {self.id}{ds}"


class Bots(list[DcaBot]):
    def __init__(self, bots: list[DcaBot] = None) -> None:
        super().__init__(bots or [])

