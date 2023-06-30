from ...models.id import Id
from ...models.position import Position
from .repository import Repository

class PositionRepository(Repository):
    def _build(self, row) -> Position:
        return Position(
            id = Id(row[0]),
            bot_id = Id(row[1]),
            symbol = row[2],
            side = row[3],
            profit = row[4],
            profit_pct = row[5]
            )
    
    def fetch(self, id: Id) -> Position:
        sql = '''
            SELECT * FROM positions WHERE id = %s
            '''
        values = (id.id,)
        result = self._fetch_one(sql, values)
        return self._build(result)

    def fetch_for_bot(self, bot_id: Id) -> list[Position]:
        sql = '''
            SELECT * FROM positions WHERE bot_id = %s
            '''
        values = (bot_id.id,)
        rows = self._fetch_all(sql, values)
        return [self._build(row) for row in rows]

    def add(self, position_id: Id, bot_id: Id, symbol: str, side: str) -> None:
        sql = '''
            INSERT INTO positions (
            id, bot_id, symbol, profit, profit_pct, side
            )
            VALUES (
                %s, %s, %s, %s, %s, %s
            )
            '''
        values = (position_id.id, 
                  bot_id.id, 
                  symbol, 
                  0, 
                  0, 
                  side)
        self._execute(sql, values)

    def update_profit(self, position_id: Id, profit: float, profit_pct: float) -> None:
        sql = '''
            UPDATE positions SET profit = %s, profit_pct = %s WHERE id = %s
            '''
        values = (profit, profit_pct, position_id.id)
        self._execute(sql, values)