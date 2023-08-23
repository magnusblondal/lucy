from rich import inspect
from lucy.infrastructure.repos.signal_repository import SignalRepository
from lucy.model.id import Id
from lucy.model.order import Order, Orders
from lucy.model.symbol import Symbol
from .repository import Repository
from .fills_repository import FillsRepository

class OrderRepository(Repository):
    def _build(self, row) -> Order:
        return Order(
            id = row[0],
            position_id             = Id(row[1]),
            bot_id                  = Id(row[2]),
            symbol                  = Symbol(row[4]),
            qty                     = row[5],
            price                   = row[6],
            order_type              = row[7],
            side                    = row[8],
            type                    = row[9],
            filled                  = row[10],
            limit_price             = row[11],
            reduce_only             = row[12],
            order_created_at        = row[13],
            last_update_timestamp   = row[14],
            exchange_id             = row[15],
            created_at              = row[16],

            signal = SignalRepository().fetch(Id(row[3]))
        )
    
    def fetch(self, id: Id) -> Order:
        sql = '''
            SELECT * FROM orders WHERE id = %s
            '''
        values = (str(id),)
        result = self._fetch_one(sql, values)
        return self._build(result)
    
    def fetch_with_data(self, id: Id) -> Order:
        order = self.fetch(id)
        if order is None:
            return None
        return self._fetch_data(order)

    def fetch_for_position(self, position_id: Id) -> Orders:
        sql = '''
            SELECT * FROM orders WHERE position_id = %s '''
        values = (str(position_id),)
        res = self._fetch_all(sql, values)
        os = Orders([self._build(row) for row in res])
        for o in os:
            o.fills = FillsRepository().fetch_for_order(o.id)
        return os
    
    def fetch_for_bot(self, bot_id: Id) -> Orders:
        sql = '''
            SELECT * FROM orders WHERE bot_id = %s
            '''
        values = (str(bot_id),)
        res = self._fetch_all(sql, values)
        return Orders([self._build(row) for row in res])

    def add(self, order: Order) -> None:
        sql = '''
            INSERT INTO orders (
                id,
                position_id, 
                bot_id,
                signal_id,
                symbol, 
                qty, 
                price, 
                order_type,
                side, 
                type, 
                filled, 
                limit_price, 
                reduce_only, 
                order_created_at, 
                last_update_timestamp, 
                exchange_id
            )
            VALUES (
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s
            )
            '''
        values = (str(order.id),
                  str(order.position_id),
                  str(order.bot_id), 
                  str(order.signal.id),
                  str(order.symbol), 
                  order.qty, 
                  order.price,
                  order.order_type,
                  order.side,
                  order.type,
                  order.filled,
                  order.limit_price,
                  order.reduce_only,
                  order.order_created_at,
                  order.last_update_timestamp,
                  order.exchange_id)
        self._execute(sql, values)

    def _fetch_data(self, order: Order) -> Order:
        order.fills = FillsRepository().fetch_for_order(order.id)
        # order.signal = SignalRepository().fetch_for_order(order.id)
        return order
