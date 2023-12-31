from lucy.model.id import Id
from lucy.model.position import Position, Positions
from lucy.model.symbol import Symbol
from .repository import Repository
from .order_repository import OrderRepository
from .signal_repository import SignalRepository
from lucy.main_logger import MainLogger


class PositionRepository(Repository):
    def __init__(self):
        super().__init__()
        self.logger = MainLogger.get_logger(__name__)

    def _build(self, row) -> Position:
        return Position(
            id=Id(row[0]),
            bot_id=Id(row[1]),
            symbol=Symbol(row[2]),
            side=row[3],
            profit=row[4],
            profit_pct=row[5],
            created_at=row[6]
        ) if row is not None else Position.empty()

    def fetch(self, id: Id) -> Position:
        sql = '''
            SELECT * FROM positions WHERE id = %s
            '''
        values = (str(id),)
        result = self._fetch_one(sql, values)
        return self._build(result)

    def fetch_for_bot(self, bot_id: Id) -> Positions:
        sql = '''
            SELECT * FROM positions WHERE bot_id = %s
            '''
        values = (bot_id.id,)
        rows = self._fetch_all(sql, values)
        return Positions([self._build(row) for row in rows])

    def fetch_by_order(self, order_id: Id) -> Position:
        sql = '''
        select * from positions p
        where p.id in (
            select o.position_id from orders o where o.id = %s)
            '''
        values = (str(order_id),)
        row = self._fetch_one(sql, values)
        pos = self._build(row)
        return self._fetch_data(pos)

    def fetch_with_data(self, id: Id) -> Positions:
        pos = self.fetch(id)
        if pos is None:
            return None
        return self._fetch_data(pos)

    def add(
        self,
        position_id: Id,
        bot_id: Id,
        symbol: Symbol,
        side: str
    ) -> None:
        sql = '''
            INSERT INTO positions (
            id, bot_id, symbol, profit, profit_pct, side
            )
            VALUES (
                %s, %s, %s, %s, %s, %s
            )
            '''
        values = (str(position_id),
                  str(bot_id),
                  str(symbol),
                  0,
                  0,
                  side)
        self._execute(sql, values)

    def update_profit(
        self,
        position_id: Id,
        profit: float,
        profit_pct: float
    ) -> None:
        self.logger.info(
            f"PositionRepository.update_profit: {position_id} {profit} {profit_pct}")
        sql = '''
            UPDATE positions SET profit = %s, profit_pct = %s WHERE id = %s
            '''
        values = (profit, profit_pct, str(position_id))
        self._execute(sql, values)

    def _fetch_data(self, pos: Position) -> Position:
        pos.orders = OrderRepository().fetch_for_position(pos.id)
        pos.signals = SignalRepository().fetch_for_position(pos.id)
        return pos

