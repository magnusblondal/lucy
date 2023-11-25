# from rich import inspect
from .event_handlers.trading_signal_handler import (
    trading_signal_handler,
    order_created_handler,
    profit_calculated_handler,
    order_filled_handler,
)
from .event_handlers.trading_signal_handler import (
    position_entry_handler,
    position_exit_handler,
    add_funds_handler,
    bot_active_state_changed_handler,
)
from .event import Event
from .some_events import (
    SignalEvent,
    PositionEntryEvent,
    AddFundsEvent,
    PositionExitEvent,
    ProfitCalculatedEvent,
    BotActiveStateChangedEvent,
)
from .order_events import OrderFilledEvent, OrderCreatedEvent
from lucy.main_logger import MainLogger

logger = MainLogger.get_logger(__name__)


def publish(events: list[Event]) -> None:
    if not events:
        # logger.info("BUS publish: No events to publish")
        return
    es = [type(e).__name__ for e in events]
    logger.info(f"BUS publish: {len(events)} events: {' '.join(es)}")
    for ev in events:
        _publish(ev)


def _publish(event: Event) -> None:
    logger.info(f"Event published: {type(event).__name__}")

    if isinstance(event, SignalEvent):
        """
        Trading Signal
        """
        logger.info(
            f"SignalEvent published: {event} {event.signal.id.id} <---")
        trading_signal_handler(event)

    elif isinstance(event, PositionEntryEvent):
        """
        Position Entry Signal
        """
        logger.info(f"PositionEntryEvent published: {event}")
        position_entry_handler(event)

    elif isinstance(event, AddFundsEvent):
        """
        Add Funds Signal
        """
        logger.info(f"PositionEntryEvent published: {event}")
        add_funds_handler(event)
        """
        Position Exit Signal
        """
        logger.info(f"PositionEntryEvent published: {event}")
        position_exit_handler(event)

    elif isinstance(event, OrderCreatedEvent):
        """
        Order Created
        """
        logger.info(f"OrderCreatedEvent published: {event}")
        order_created_handler(event)

    elif isinstance(event, ProfitCalculatedEvent):
        """
        Profit Calculated
        """
        logger.info(f"ProfitCalculatedEvent published: {event}")
        profit_calculated_handler(event)

    elif isinstance(event, BotActiveStateChangedEvent):
        logger.info(f"BotActiveStateChangedEvent published: {event}")
        bot_active_state_changed_handler(event)

    elif isinstance(event, OrderFilledEvent):
        """
        Order Filled
        """
        logger.info(f"OrderFilledEvent published: {event}")
        order_filled_handler(event)

    else:
        logger.warning(f"Event not handled: {type(event).__name__}")
