
from rich import inspect
from lucy.infrastructure.repos.position_repository import PositionRepository
from lucy.model.id import Id
from ..usecase import Usecase
from lucy.infrastructure.repos.bot_repository import BotRepository
from lucy.main_logger import MainLogger
import lucy.application.events.bus as bus

class AuditBot(Usecase):
    def handle(self, id: str):
        '''Audit a bot'''
        bot = BotRepository().fetch(id)
        bot.audit()
        bus.publish(bot.events())

class ProfitOrLossCalculationForPosition(Usecase):
    def __init__(self):
        self.logger = MainLogger.get_logger(__name__)

    def handle(self, order_id: Id):
        '''Calculate profit or loss for a position'''
        inspect(order_id)
        if isinstance(order_id, str):
            order_id = Id(order_id)
        print(f"ProfitOrLossCalculationForPosition:: order id: {order_id}")
        position = PositionRepository().fetch_by_order(order_id)
        if position is None or position.is_empty():
            if position is None:
                mssg = "is None"
            elif position.is_empty():
                mssg = "is empty"
            else:
                mssg = "is unknown"
            self.logger.info(f"ProfitOrLossCalculationForPosition: No position found for order id: {order_id} {mssg}")
            return
        position.calculate_profit_loss()
        bus.publish(position.events())