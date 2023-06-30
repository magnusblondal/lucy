
from ...models.id import Id

from ...models.trade import Trade
from ...models.bot import DcaBot, Bot
from ...models.position import Position
from .repository import Repository
from .position_repository import PositionRepository
from .signal_repository import SignalRepository
from .order_repository import OrderRepository

from rich import inspect

class BotRepository(Repository):
    def _build(self, row: tuple) -> DcaBot:
        return DcaBot(
            Id(row[0]),
            row[1],
            description = row[2],
            active = row[3],            
            num_positions_allowed = int(row[4]),
            capital = float(row[5]),
            entry_size = float(row[6]),
            so_size = float(row[7]),
            max_safety_orders = int(row[8]),
            allow_shorts = row[9]
            )

    def fetch_bot(self, id: str) -> Bot:
        sql = '''
            SELECT * FROM bots WHERE id LIKE %s
            '''
        values = (id + '%',)
        result = self._fetch_one(sql, values)
        if result is None or len(result) == 0:
            return None
        
        bot = self._build(result)
        bot.positions = PositionRepository().fetch_for_bot(bot.id)
        signals = SignalRepository().fetch_for_bot(bot.id)
        orders = OrderRepository().fetch_for_bot(bot.id)
        for position in bot.positions:
            position.signals = [signal for signal in signals if signal.position_id == position.id]
            position.orders = [order for order in orders if order.position_id == position.id]
        return bot	
        
    def fetch_bots(self) -> list[Bot]:
        sql = '''
            SELECT * FROM bots
            '''
        result = self._fetch_all(sql)
        bots = []   
        for row in result: 
            bot = self._build(row) 
            signals = SignalRepository().fetch_for_bot(bot.id)
            orders = OrderRepository().fetch_for_bot(bot.id)
            bot.positions = PositionRepository().fetch_for_bot(bot.id)
            for position in bot.positions:
                position.signals = [signal for signal in signals if signal.position_id == position.id]
                position.orders = [order for order in orders if order.position_id == position.id]
            bots.append(bot)
        return bots

    def _save_dca_bot(self, bot: DcaBot) -> None:
        sql = '''
            INSERT INTO bots
            (id, name, description, active, max_positions, capital, entry_size, so_size, max_safety_orders, allow_shorts)
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            '''
        values = (bot.id.id, bot.name, bot.description, bot.active, bot.num_positions_allowed, bot.capital, bot.entry_size, bot.so_size, bot.max_safety_orders, bot.allow_shorts)
        self._execute(sql, values)

    def save(self, bot: Bot) -> None:
        if isinstance(bot, DcaBot):
            self._save_dca_bot(bot)
        else:
            raise Exception('Bot type not supported')

    def _update_dca_bot(self, bot: Bot) -> None:
        sql = '''
            UPDATE bots
            SET 
                name = %s, description = %s, active = %s, max_positions = %s,
                capital = %s, entry_size = %s, 
                so_size = %s, max_safety_orders = %s, allow_shorts = %s
            WHERE id = %s
            '''
        values = (bot.name, bot.description, bot.active, bot.num_positions_allowed, bot.capital, bot.entry_size, bot.so_size, bot.max_safety_orders, bot.allow_shorts, bot.id.id)
        self._execute(sql, values)

    def update(self, bot: Bot) -> None:
        if isinstance(bot, DcaBot):
            self._update_dca_bot(bot)
        else:
            raise Exception('Bot type not supported')
    
    def update_active(self, bot_id: Id, active: bool) -> None:
        sql = '''
            UPDATE bots
            SET active = %s
            WHERE id = %s
            '''
        values = (active, bot_id.id)
        self._execute(sql, values)
