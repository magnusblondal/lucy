
from lucy.model.id import Id
from lucy.model.bot import Bots, DcaBot, Bot
from lucy.model.interval import Interval
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
            allow_shorts = row[9],
            interval = Interval(int(row[10])),
            symbol = row[11]
            )


    def fetch(self, id: str) -> Bot:
        sql = '''
            SELECT * FROM bots WHERE id LIKE %s
            '''
        values = (str(id) + '%',)
        result = self._fetch_one(sql, values)
        if result is None or len(result) == 0:
            return None        

        bot             = self._build(tuple(result))
        bot.positions   = PositionRepository().fetch_for_bot(bot.id)
        signals         = SignalRepository().fetch_for_bot(bot.id)
        for position in bot.positions:
            position.signals        = [signal for signal in signals if signal.position_id == position.id]
            position.orders         = OrderRepository().fetch_for_position(position.id)
        return bot	
    
    def fetch_bots(self) -> Bots:
        '''Fetch all bots'''
        sql = '''
            SELECT * FROM bots'''
        return self._fetch_em(sql)
    
    def fetch_active_bots(self) -> Bots:
        '''Fetch all active bots'''
        sql = '''
            SELECT * FROM bots WHERE active = True
            '''
        return self._fetch_em(sql)

    def add(self, bot: Bot) -> None:
        if isinstance(bot, DcaBot):
            self._save_dca_bot(bot)
        else:
            raise Exception('Bot type not supported')

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
        values = (active, str(bot_id))
        self._execute(sql, values)
    

    # region Private

    def _fetch_em(self, sql: str) -> Bots:
        bots = []   
        result = self._fetch_all(sql)

        for row in result: 
            bot = self._build(tuple(row)) 
            signals = SignalRepository().fetch_for_bot(bot.id)
            orders = OrderRepository().fetch_for_bot(bot.id)
            bot.positions = PositionRepository().fetch_for_bot(bot.id)
            for position in bot.positions:
                position.signals = [signal for signal in signals if signal.position_id == position.id]
                position.orders = orders.for_position(position.id)
            bots.append(bot)
        return Bots(bots)

    def _save_dca_bot(self, bot: DcaBot) -> None:
        sql = '''
            INSERT INTO bots
            (id, name, description, active, max_positions, capital, entry_size, so_size, max_safety_orders, allow_shorts, interval, symbol, strategy)
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            '''
        values = (str(bot.id), bot.name, bot.description, bot.active, bot.num_positions_allowed, 
                  bot.capital, bot.entry_size, bot.so_size, bot.max_safety_orders, 
                  bot.allow_shorts, bot.interval.interval, bot.symbol, bot.strategy.name)
        self._execute(sql, values)

    def _update_dca_bot(self, bot: DcaBot) -> None:
        sql = '''
            UPDATE bots
            SET 
                name = %s, description = %s, active = %s, max_positions = %s,
                capital = %s, entry_size = %s, 
                so_size = %s, max_safety_orders = %s, allow_shorts = %s,
                interval = %s, symbol = %s, strategy = %s
            WHERE id = %s
            '''
        values = (bot.name, bot.description, bot.active, bot.num_positions_allowed, 
                  bot.capital, bot.entry_size, bot.so_size, bot.max_safety_orders, 
                  bot.allow_shorts, bot.interval.interval, bot.symbol, str(bot.id), bot.strategy.name)
        self._execute(sql, values)

    #endregion