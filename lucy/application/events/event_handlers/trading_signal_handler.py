from datetime import datetime

from ..some_events import SignalEvent, PositionEntryEvent, PositionExitEvent, AddFundsEvent, ProfitCalculatedEvent, BotActiveStateChangedEvent
from ..order_events import OrderFilledEvent, OrderCreatedEvent
from lucy.application.usecases.bots.audit import ProfitOrLossCalculationForPosition
from lucy.infrastructure.repos.signal_repository import SignalRepository
from lucy.infrastructure.repos.position_repository import PositionRepository
from lucy.infrastructure.repos.order_repository import OrderRepository
from lucy.infrastructure.repos.bot_repository import BotRepository 
from lucy.main_logger import MainLogger

logger = MainLogger.get_logger(__name__)

def trading_signal_handler(event: SignalEvent):
    logger.info(f"Trading Signal Handler: {event.signal.id.id}")
    SignalRepository().add(event.bot_id, event.position_id, event.signal)

def position_entry_handler(event: PositionEntryEvent):
    logger.info(f"Position Entry Handler: {event}")
    PositionRepository().add(event.position_id, event.bot_id, event.symbol, event.side)

def add_funds_handler(event: AddFundsEvent):
    logger.info(f"Add Funds Handler: {event}")
    # OrderRepository().add(event.order)
    #TODO: Impl

def position_exit_handler(event: PositionExitEvent):
    logger.info(f"Position Exit Handler: {event}")
    # OrderRepository().add(event.order)
    #TODO: Impl

def order_created_handler(event: OrderCreatedEvent):
    logger.info(f"Order Created Handler: {event}")
    OrderRepository().add(event.order)

def profit_calculated_handler(event: ProfitCalculatedEvent):
    logger.info(f"Profit Calculated Handler: {event}")
    PositionRepository().update_profit(event.position_id, event.profit, event.profit_percentage)

def bot_active_state_changed_handler(event: BotActiveStateChangedEvent):
    logger.info(f"Bot Active State Changed Handler: {event}")
    BotRepository().update_active(event.bot_id, event.is_active)

def order_filled_handler(event: OrderFilledEvent):
    logger.info(f"Order Filled Handler: {event} Order filled: {event.is_order_filled}")
    if event.is_order_filled:
        ProfitOrLossCalculationForPosition().handle(event.order_id)