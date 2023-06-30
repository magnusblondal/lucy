from datetime import datetime
from typing import List

from ...models.id import Id
from ...models.order import Order
from .repository import Repository

class OrderRepository(Repository):
    def _build(self, row) -> Order:
        return Order(
            id = row[0],
            position_id = Id(id = row[1]),
            bot_id = Id(id = row[2]),
            symbol = row[3],
            qty = row[4],
            price = row[5],
            order_type = row[6],
            side = row[7],
            type = row[8],
            filled = row[9],
            limit_price = row[10],
            reduce_only = row[11],
            order_created_at = row[12],
            last_update_timestamp = row[13],
            exchange_id = row[14],
            created_at = row[15]
        )
    
    def fetch(self, id: Id) -> Order:
        sql = '''
            SELECT * FROM orders WHERE id = %s
            '''
        values = (id.id,)
        result = self._fetch_one(sql, values)
        return self._build(result)

    def fetch_for_position(self, position_id: Id) -> List[Order]:
        sql = '''
            SELECT * FROM orders WHERE position_id = %s '''
        values = (position_id.id,)
        res = self._fetch_all(sql, values)
        return [self._build(row) for row in res]
    
    def fetch_for_bot(self, bot_id: Id) -> List[Order]:
        sql = '''
            SELECT * FROM orders WHERE bot_id = %s
            '''
        values = (bot_id.id,)
        res = self._fetch_all(sql, values)
        return [self._build(row) for row in res]

    def add(self, 
            position_id: Id, bot_id: Id, exchange_id: str, symbol: str, qty: float, 
            price: float, order_type: str, side: str, type: str, filled: int, limit_price: float, 
            reduce_only: bool, created: datetime, last_update: datetime,
            client_id: str) -> None:
        sql = '''
            INSERT INTO orders (
                id,
                position_id, 
                bot_id,
                symbol, 
                qty, 
                price, 
                order_type,
                side, 
                type, filled, limit_price, 
                reduce_only, order_created_at, 
                last_update_timestamp, exchange_id
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            '''
        values = (client_id, 
                  position_id.id, 
                  bot_id.id,
                  symbol, 
                  qty, 
                  price,
                  order_type,
                  side,
                  type,
                  filled,
                  limit_price,
                  reduce_only,
                  created,
                  last_update,
                  exchange_id)
        self._execute(sql, values)