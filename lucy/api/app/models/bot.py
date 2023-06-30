from rich import inspect

from .create_bot import CreateDcaBot, EditDcaBot
from .domain_model import DomainModel
from .position import Position
from .signal import Signal
from .id import *
from ..events.event import DomainEvent, BotActiveStateChangedEvent


class Bot(DomainModel):
    name: str
    description: str
    active: bool
    num_positions_allowed: int

    def __init__(self, id: Id, name: str, description: str, active: bool, num_positions_allowed: int) -> None:
        super().__init__(id)
        self.name = name
        self.description = description
        self.active = active
        self.num_positions_allowed = num_positions_allowed

class DcaBot(Bot):
    capital: float
    entry_size: float
    so_size: float
    max_safety_orders: int
    allow_shorts: bool
    positions: list[Position]
    
    def __init__(self, id: Id, name: str, description: str, active: bool, capital: float, entry_size: float, so_size: float, 
                 max_safety_orders: int, allow_shorts: bool, num_positions_allowed: int ) -> None:
        super().__init__(id, name, description, active, num_positions_allowed)
        self.capital = capital
        self.entry_size = entry_size
        self.so_size = so_size
        self.max_safety_orders = max_safety_orders
        self.allow_shorts = allow_shorts
        self.positions = []
    
    @staticmethod
    def create_new(bot: CreateDcaBot):
        return DcaBot(Id(), 
                      bot.name,
                      bot.description,
                      True,
                      bot.capital, 
                      bot.entry_size, 
                      bot.so_size, 
                      bot.max_safety_orders, 
                      bot.allow_shorts,
                      bot.max_positions_allowed)
    
    def update(self, edit: EditDcaBot):
        self.name = edit.name
        self.description = edit.description
        self.capital = edit.capital
        self.entry_size = edit.entry_size
        self.so_size = edit.so_size
        self.max_safety_orders = edit.max_safety_orders
        self.allow_shorts = edit.allow_shorts
        self.num_positions_allowed = edit.max_positions_allowed

    def events(self) -> list[DomainEvent]:
        evs = self._events if self._events is not None else []
        for p in self.positions:
            evs.extend(p.events())
        return evs

    def _within_max_limit(self):
        num_open_pos = self.num_open_positions()
        return num_open_pos < self.num_positions_allowed
    
    def _is_posistion_open_for_symbol(self, symbol: str):
        ps = [p for p in self.positions if p.fits_signal(symbol)]
        return len(ps) > 0
    
    def _position(self, id: Id) -> Position:
        ps = [position for position in self.positions if position.id == id]
        return ps[0] if len(ps) > 0 else None
    
    
    def _position_for_signal(self, signal: Signal) -> Position:
        if len(self.positions) == 0:
            return None
        ps = [p for p in self.positions if p.fits_signal(signal)]
        return ps[0] if len(ps) > 0 else None

    
    def _new_position(self, signal: Signal):
        print(f"-> Bot '{self.id}' handle '{signal.signal_type}' -- opna position")
        if self.positions is None:
            self.positions = []
        if self._is_posistion_open_for_symbol(signal):
            print(f"-> Bot {self.id} handle {signal.signal_type} -- position already open for symbol {signal.ticker}")
            return
        
        if not self._within_max_limit():
            print(f"-> Bot {self.id} handle {signal.signal_type} -- max limit reached, cannot open position")
            return
            
        position = Position.create_new(signal)
        self.positions.append(position)
        position.entry(signal, self.entry_size)
    
    def _add_funds(self, signal: Signal):
        print(f"-> Bot {self.id} handle {signal.signal_type} -- add funds")
        if len(self.positions) == 0:
            print(f"-> Bot {self.id} handle {signal.signal_type} -- No position available, cannot add funds")
            return
        position = self._position_for_signal(signal)
        
        if position is not None:
            signal.position_id = position.id
            position.add_funds(signal, self.so_size, self.max_safety_orders)
        else:
            print(f"-> Bot {self.id} handle {signal.signal_type} -- No open position found, cannot add funds")

    def _close(self, signal: Signal):
        print(f"-> Bot {self.id} handle {signal.signal_type} -- loka position")
        if len(self.positions) == 0:
            print(f"-> Bot {self.id} handle {signal.signal_type} -- No position available, cannot close")
            return
        position = self._position_for_signal(signal)
        if position is not None:
            position.close(signal)
        else:
            print(f"-> Bot {self.id} handle {signal.signal_type} -- position not found, cannot close")

    def has_description(self) -> bool:
        return self.description is not None and len(self.description) > 0
    
    def audit(self):
        print(f"-> Bot {self.id} audit")
        if len(self.positions) == 0:
            print(f"-> Bot {self.id} audit -- No position available, cannot audit")
            return
        
        unaudited = [position for position in self.positions if not position.is_audited()]
        for position in unaudited:
            position.audit()
        if len(unaudited) == 0:
            print(f"-> Bot {self.id} audit -- No positions to audit")
    
    def profit(self) -> float:
        '''Returns the total profit for all positions'''
        return sum([position.profit for position in self.positions if position.profit is not None])
    
    def num_open_positions(self) -> int:
        '''Returns the number of currently open positions'''
        return len([position for position in self.positions if position.is_open()])

    def handle(self, signal: Signal) -> tuple[bool, str]:
        '''Handle a signal'''
        if not self.active:
            print(f"-> Bot {self.id} handle {signal.signal_type} -- bot is not active")
            return (False, "Bot is not active")
        if signal.is_entry():
            self._new_position(signal)
        elif signal.is_add_funds():
            self._add_funds(signal)
        elif signal.is_close():
            self._close(signal)        
        else:
            msg = f"Bot {self.id} handle {signal.signal_type} -- unknown signal type"
            print(msg)
            return (False, msg)
        return (True, "OK")
    
    def has_positions(self) -> bool:
        return self.positions is not None and len(self.positions) > 0
    
    def turn_off(self, liquidate: bool = False):
        ''''''
        self.active = False
        self._this_just_happened(BotActiveStateChangedEvent(self.id, self.active))

    def turn_on(self):
        self.active = True
        self._this_just_happened(BotActiveStateChangedEvent(self.id, self.active))
    
    def __str__(self) -> str:
        ds = '\n'.join([f"\t{p}" for p in self.positions])  if self.has_positions() > 0 else "No Positions"
        return f"Bot id: {self.id}, {self.name}, {self.capital}, {self.entry_size}, {self.so_size}, {self.max_safety_orders}, {self.allow_shorts}, positions: \n{ds}"
