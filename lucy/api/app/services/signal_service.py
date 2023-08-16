from rich import inspect

from lucy.infrastructure.repos.bot_repository import BotRepository
from lucy.model.signal_incoming import SignalIncoming
from lucy.application.events import bus

class SignalService:
    def handle(self, signal: SignalIncoming) -> tuple[bool, str]:
        bot = BotRepository().fetch_bot(signal.bot_id)
        result = bot.handle(signal.to_model())
        bus.publish(bot.events())
        return result
