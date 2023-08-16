
class Trade:
    product_id: str
    '''The subscribed product (referred also as instrument or symbol)'''
    uid: str
    '''Unique identifier for the matched trade'''
    side: str
    '''The classification of the taker side in the matched trade: 'buy' if the taker is a buyer, 'sell' if the taker is a seller.'''
    type: str                 # 'fill',
    '''The classification of the matched trade in an orderbook: 
      'fill' if it is a normal buyer and seller, 
      'liquidation' if it is a result of a user being liquidated from their position, 
      'termination' if it is a result of a user being terminated, 
      or 'block' if it is a component of a block trade.'''
    seq: int
    '''The subscription message sequence number'''
    time: int
    '''The UTC or GMT time of the trade in milliseconds'''
    qty: float              # 0.0001,
    '''The quantity of the traded product'''
    price: float                # 30035.0
    '''The price that the product got traded'''

    def __init__(self, product_id: str, uid: str, side: str, type: str, seq: int, time: int, qty: float, price: float) -> None:
        self.product_id = product_id
        self.uid = uid
        self.side = side
        self.type = type
        self.seq = seq
        self.time = time
        self.qty = qty
        self.price = price
    
    def __str__(self) -> str:
        return f"Trade:: product_id: {self.product_id}, uid: {self.uid}, side: {self.side}, type: {self.type}, seq: {self.seq}, time: {self.time}, qty: {self.qty}, price: {self.price}"
    
    @staticmethod
    def from_feed(data) -> 'Trade':
        return Trade(
            data['product_id'], 
            data['uid'],
            data['side'],
            data['type'],
            data['seq'],
            data['time'],
            data['qty'],
            data['price'])


class Trades:
    trades: dict[Trade]

    def __init__(self, trades: list[Trade]) -> None:
        self.trades = {}
        for trade in trades:
            if trade.product_id in self.trades.keys():
                self.trades[trade.product_id].append(trade)
            else:
                self.trades[trade.product_id] = [trade]
    
    def __str__(self) -> str:
        ts = [(key, len(val)) for key, val in self.trades.items()]
        s = "".join([f"{key}: {value}\n" for key, value in ts])
        s = "\n" + s if s != "" else s
        return f"Trades:: trades: {s}"
    
    def add(self, trade: Trade) -> None:
        if trade.product_id in self.trades.keys():
            self.trades[trade.product_id].append(trade)
        else:
            self.trades[trade.product_id] = [trade]

    @staticmethod
    def from_feed(data) -> 'Trades':
        trades = [Trade.from_feed(trade) for trade in data['trades']]
        return Trades(trades)
