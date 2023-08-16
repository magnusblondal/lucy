
from lucy.infrastructure.repos.position_repository import PositionRepository
from lucy.model.id import Id
from ..usecase import Usecase
from lucy.infrastructure.repos.bot_repository import BotRepository

import lucy.application.events.bus as bus

class AuditBot(Usecase):
    def handle(self, id: str):
        '''Audit a bot'''
        bot = BotRepository().fetch_bot(id)
        bot.audit()
        bus.publish(bot.events())

class ProfitOrLossCalculationForPosition(Usecase):
    def handle(self, order_id: Id):
        '''Calculate profit or loss for a position'''
        if isinstance(order_id, str):
            order_id = Id(order_id)
        position = PositionRepository().fetch_by_order(order_id)
        position.calculate_profit_loss()
        bus.publish(position.events())