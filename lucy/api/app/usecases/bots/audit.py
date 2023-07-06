
from ..usecase import Usecase
from lucy.api.app.infrastructure.repos.bot_repository import BotRepository

import lucy.api.app.events.bus as bus

class AuditBot(Usecase):
    def handle(self, id: str):
        '''Audit a bot'''
        bot = BotRepository().fetch_bot(id)
        bot.audit()
        bus.publish(bot.events())