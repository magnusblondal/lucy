from lucy.model.id import Id
from .repository import Repository
from lucy.application.trading.feeds.fills import Fill, Fills

class FillsRepository(Repository):
    def _build(self, row: tuple) -> Fill:
        return Fill(
            Id(row[0]),
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            row[6],
            row[7],
            row[8],
            row[9],
            row[10],
            row[11],
            row[12],
            row[13],
            row[14]
        )
    
    def add(self, fill: Fill) -> None:
        sql = '''
            INSERT INTO fills (
                id, instrument, time, price, buy, qty, remaining_order_qty, order_id, fill_type, fee_paid, fee_currency,
                taker_order_type, order_type, cli_ord_id, position_id
                )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
        values = (
            fill.id,
            fill.instrument,
            fill.dtm(),
            fill.price,
            fill.buy,
            fill.qty,
            fill.remaining_order_qty,
            fill.order_id,
            fill.fill_type,
            fill.fee_paid,
            fill.fee_currency,
            fill.taker_order_type,
            fill.order_type,
            fill.cli_ord_id or "",
            fill.position_id
        )
        self._execute(sql, values)

    def single(self, id: Id) -> Fill:
        sql = '''
            SELECT id, instrument, time, price, buy, qty, remaining_order_qty, order_id, fill_type, fee_paid, fee_currency, 
            taker_order_type, order_type, cli_ord_id, position_id
            FROM fills
            WHERE id = %s
            '''
        values = (id,)
        res = self._fetch_one(sql, values)
        fill = self._build(res)
        return fill
    
    def fetch_for_order(self, order_id: Id) -> Fills:
        sql = '''
            SELECT id, instrument, time, price, buy, qty, remaining_order_qty, order_id, fill_type, fee_paid, fee_currency, 
            taker_order_type, order_type, cli_ord_id, position_id
            FROM fills
            WHERE order_id = %s
            '''
        values = (str(order_id),)
        res = self._fetch_all(sql, values)
        fills = Fills([self._build(row) for row in res])
        return fills
    
    def fetch_for_orders(self, order_ids: list[Id]) -> Fills:
        if len(order_ids) == 0:
            return Fills([])
        
        ss = '%s, ' * len(order_ids) 
        ss = ss[:-2]
        sql = '''
            SELECT id, instrument, time, price, buy, qty, remaining_order_qty, order_id, fill_type, fee_paid, fee_currency, 
            taker_order_type, order_type, cli_ord_id, position_id
            FROM fills
            WHERE order_id IN 
            '''
        sql += '(' + ss + ')'
        order_ids = [str(o) for o in order_ids]
        values = tuple(order_ids)
        res = self._fetch_all(sql, values)
        fills = Fills([self._build(tuple(row)) for row in res])
        return fills
    
    def fetch_for_position(self, position_id: Id) -> Fills:
        sql = '''
            SELECT id, instrument, time, price, buy, qty, remaining_order_qty, order_id, fill_type, fee_paid, fee_currency, 
            taker_order_type, order_type, cli_ord_id, position_id
            FROM fills
            WHERE position_id = %s
            '''
        values = (str(position_id),)
        res = self._fetch_all(sql, values)
        fills = Fills([self._build(row) for row in res])
        return fills

# id, instrument, time, price, buy, qty, remaining_order_qty, order_id, fill_type, fee_paid, fee_currency, taker_order_type, order_type, cli_ord_id

# id
# instrument
# time
# price
# buy
# qty
# remaining_order_qty
# order_id
# fill_type
# fee_paid
# fee_currency
# taker_order_type
# order_type
# cli_ord_id