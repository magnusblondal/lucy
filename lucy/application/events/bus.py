from rich import inspect
from .event_handlers.trading_signal_handler import trading_signal_handler, order_created_handler, profit_calculated_handler, order_filled_handler
from .event_handlers.trading_signal_handler import position_entry_handler, position_exit_handler, add_funds_handler, bot_active_state_changed_handler
from .event import Event
from .some_events import SignalEvent, PositionEntryEvent, AddFundsEvent, PositionExitEvent, ProfitCalculatedEvent, BotActiveStateChangedEvent
from .order_events import OrderFilledEvent, OrderCreatedEvent
from lucy.main_logger import MainLogger

logger = MainLogger.get_logger(__name__)

def publish(events: list[Event]) -> None:
    # print(f"BUS publish: {len(events)} events")
    for ev in events:
        _publish(ev)

def _publish(event: Event) -> None:
    logger.info(f"Event published: {type(event).__name__}")

    # ---------
    # Trading Signal
    # ---------
    if isinstance(event, SignalEvent):
        # print(f"SignalEvent published: {event} {event.signal.id.id} <---")
        trading_signal_handler(event)

    # ---------
    # Position Entry Signal
    # ---------
    if isinstance(event, PositionEntryEvent):
        # print(f"PositionEntryEvent published: {event}")
        position_entry_handler(event)

    # ---------
    # Add Funds Signal
    # ---------
    if isinstance(event, AddFundsEvent):
        # print(f"PositionEntryEvent published: {event}")
        add_funds_handler(event)
    
    # ---------
    # Position Exit Signal
    # ---------
    if isinstance(event, PositionExitEvent):
        # print(f"PositionEntryEvent published: {event}")
        position_exit_handler(event)
    
    # ---------
    # Order Created 
    # ---------
    if isinstance(event, OrderCreatedEvent):
        # print(f"OrderCreatedEvent published: {event}")
        order_created_handler(event)
    
    # ---------
    # Profit Calculated
    # ---------
    if isinstance(event, ProfitCalculatedEvent):
        # print(f"ProfitCalculatedEvent published: {event}")
        profit_calculated_handler(event)

    # ---------
    # 
    # ---------
    if isinstance(event, BotActiveStateChangedEvent):
        bot_active_state_changed_handler(event)

    # ---------
    # 
    # ---------
    if isinstance(event, OrderFilledEvent):
        order_filled_handler(event)