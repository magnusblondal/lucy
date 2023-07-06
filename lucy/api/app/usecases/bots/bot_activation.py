
from ..usecase import Usecase
from ...infrastructure.repos.bot_repository import BotRepository
from ...models.bot import DcaBot
import lucy.api.app.events.bus as bus

class BotActivationResult:
    success: bool
    current_state: bool
    bot: DcaBot

    def __init__(self, success: bool, current_state: bool, bot: DcaBot):
        self.success = success
        self.current_state = current_state
        self.bot = bot

class BotActivation(Usecase):
    def handle(self, symbol: str, turn_on: bool) -> BotActivationResult:
        '''Turn Bot on or off'''
        if symbol is None:
            return self._all_off()
        
        bot = BotRepository().fetch_bot(symbol)
        if bot is None:
            return BotActivationResult(False, current_state=False, bot=None)
        
        if turn_on:
            bot.turn_on()
        else:
            bot.turn_off()
        bus.publish(bot.events())
        return BotActivationResult(success=True, current_state=bot.active, bot=bot)
    
    def _all_off(self):
        bots = BotRepository().fetch_bots()
        events = []
        for bot in bots:
            bot.turn_off()
            events.extend(bot.events())
        bus.publish(events)
        return BotActivationResult(success=True, current_state=False, bot=None)