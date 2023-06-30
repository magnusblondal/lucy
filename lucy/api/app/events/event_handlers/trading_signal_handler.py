from datetime import datetime

from ..event import SignalEvent, PositionEntryEvent, PositionExitEvent, AddFundsEvent, OrderCreatedEvent, ProfitCalculatedEvent, BotActiveStateChangedEvent
from ...models.signal import Signal
from ...infrastructure.repos.signal_repository import SignalRepository
from ...infrastructure.repos.position_repository import PositionRepository
from ...infrastructure.repos.order_repository import OrderRepository
from ...infrastructure.repos.bot_repository import BotRepository 

def _dtm(t: str) -> datetime:
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    return datetime.strptime(t, date_format)

def trading_signal_handler(event: SignalEvent):
    print(f"Trading Signal Handler: {event.signal.id.id}")
    SignalRepository().add(event.bot_id, event.position_id, event.signal)

def position_entry_handler(event: PositionEntryEvent):
    print(f"Position Entry Handler: {event}")
    PositionRepository().add(event.position_id, event.bot_id, event.symbol, event.side)

def add_funds_handler(event: AddFundsEvent):
    print(f"Add Funds Handler: {event}")
    #TODO: Impl

def position_exit_handler(event: PositionExitEvent):
    print(f"Position Exit Handler: {event}")
    #TODO: Impl

def order_created_handler(event: OrderCreatedEvent):
    print(f"Order Created Handler: {event}")
    ev = event.order.order_event
    OrderRepository().add(
        event.position_id, 
        event.bot_id, 
        ev.orderId, 
        ev.symbol, 
        ev.quantity, 
        ev.limitPrice, 
        event.order_type,
        ev.side, ev.type, ev.filled, 
        ev.limitPrice,
        ev.reduceOnly, _dtm(ev.timestamp), _dtm(ev.lastUpdateTimestamp), 
        ev.cliOrdId )

def profit_calculated_handler(event: ProfitCalculatedEvent):
    PositionRepository().update_profit(event.position_id, event.profit, event.profit_percentage)

def bot_active_state_changed_handler(event: BotActiveStateChangedEvent):
    print(f"Bot Active State Changed Handler: {event}")
    BotRepository().update_active(event.bot_id, event.is_active)
