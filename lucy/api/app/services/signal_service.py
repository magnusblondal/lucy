from rich import inspect

from ..infrastructure.repos.bot_repository import BotRepository
from ..models.signal_incoming import SignalIncoming
from ..events import bus

class SignalService:
    def handle(self, signal: SignalIncoming) -> tuple[bool, str]:
        bot = BotRepository().fetch_bot(signal.bot_id)
        result = bot.handle(signal.to_model())
        bus.publish(bot.events())
        return result
