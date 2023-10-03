from lucy.model.signal import Signal, Signals
from lucy.model.id import Id
from .repository import Repository

class SignalRepository(Repository):
    def __init__(self):
        super().__init__()
        
    def _build(self, row) -> Signal:
        return Signal(
            id = Id(row[0]),
            position_id = Id(row[1]),
            bot_id = Id(row[2]),
            strategy = row[3],
            ticker = row[4],
            side = row[5],
            signal_type = row[6],
            interval = row[7],
            bar_open_time = row[8],
            signal_time = row[9],
            close = row[10]
        )
        
    def add(self, bot_id: Id, position_id: Id, signal: Signal) -> None:
        sql = '''
            INSERT INTO signals (
                id, position_id, bot_id, strategy, ticker, side, signal_type, interval, bar_open_time, signal_time, close
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            '''
        values = (signal.id.id, position_id.id, bot_id.id, signal.strategy, signal.ticker, signal.side, 
                  signal.signal_type, signal.interval.interval, signal.bar_open_time, signal.signal_time, 
                  signal.close)
        self._execute(sql, values)
    
    def fetch(self, id: Id) -> Signal:
        sql = '''
            SELECT * FROM signals WHERE id = %s
            '''
        values = (str(id),)
        result = self._fetch_one(sql, values)
        return self._build(result)

    def fetch_for_position(self, position_id: Id) -> Signals:
        sql = '''
            SELECT * FROM signals WHERE position_id = %s '''
        values = (position_id.id,)
        res = self._fetch_all(sql, values)
        return Signals([self._build(row) for row in res])
    
    def fetch_for_bot(self, bot_id: Id) -> Signals:
        sql = '''
            SELECT * FROM signals WHERE bot_id = %s
            '''
        values = (str(bot_id),)
        res = self._fetch_all(sql, values)
        return Signals([self._build(row) for row in res])
