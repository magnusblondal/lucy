from datetime import datetime
from lucy.application.events.event import DomainEvent
from lucy.application.events.order_events import OrderFilledEvent

from lucy.model.domain_model import DomainModel
from lucy.model.id import Id

class Fill(DomainModel):
    id: str
    '''The fill id (fill_id).'''
    fill_type: str
    '''maker | taker'''
    instrument: str                                                             
    '''The fill instrument (referred also as symbol or product_id).'''
    time: int
    '''The server UTC date and time in milliseconds.'''
    price: float
    '''The price at which the order was filled.'''
    seq: int
    '''The subscription message sequence number.'''
    buy: bool
    '''A flag that shows if filled order was a buy.'''
    qty: float
    '''The quantity that was filled.'''
    remaining_order_qty: float
    '''The remaining quantity of the order that has not been filled.'''
    order_id: str
    '''The order id that was filled.'''
    '''The classification of the fill:
        'maker'              if the user has a limit order that gets filled,
        'taker'              if the user makes an execution that crosses the spread,
        'liquidation'        if an execution is the result of a liquidation,
        'assignee'           if an execution is a result of a counterparty receiving an Assignment in PAS,
        'assignor'           if an execution is a result of the user assigning their position due to a failed liquidation,
        'unwindBankrupt'     any portion of a liquidated position cannot be filled or assigned, the remaining contracts are unwound.
        'unwindCounterparty' any portion of your counterparty's position is liquidated and cannot be filled or assigned the remaining contracts are unwound. More information on our Equity Protection Process.
        'takerAfterEdit'     if the user edits the order and it is instantly executed.
    '''
    fee_paid: float
    '''Fee paid on fill'''
    fee_currency: str                                                               # 'USD',
    '''Currency in which the fee was charged. See "Currencies" on Ticker Symbols'''
    taker_order_type: str
    '''The order type of the taker execution side; 'market' or 'limit'.'''
    order_type: str                                  
    '''The order type; 'market' or 'limit'.'''
    cli_ord_id: str
    '''The unique client order identifier. This field is returned only if the order has a client order id.'''
    position_id: Id
    '''The position that the fill relates to. This field is parsed from the cli_ord_id field.'''

    def __init__(self, fill_id: str, instrument: str, time: int, price: float, 
                 buy: bool, qty: float, 
                 remaining_order_qty: float, order_id: str, fill_type: str, fee_paid: float, fee_currency: str, 
                 taker_order_type: str, order_type: str, cli_ord_id: str, position_id: Id, first_entry: bool = False) -> None:
        super().__init__(fill_id)
        # self.id                     = fill_id
        self.instrument             = instrument
        self.time                   = time
        self.price                  = float(price)
        self.seq                    = 0
        self.buy                    = buy
        self.qty                    = float(qty)
        self.remaining_order_qty    = remaining_order_qty
        self.order_id               = order_id
        self.fill_type              = fill_type
        self.fee_paid               = float(fee_paid)
        self.fee_currency           = fee_currency
        self.taker_order_type       = taker_order_type
        self.order_type             = order_type
        self.cli_ord_id             = cli_ord_id
        self.position_id            = position_id
        if first_entry:
            self._this_just_happened(OrderFilledEvent(self.id, self.order_id, self.remaining_order_qty == 0))


    def __str__(self) -> str:
        return f"Fill:: {self.instrument} Price: {self.price}, seq: {self.seq}, buy: {self.buy}, qty: {self.qty}, remaining_order_qty: {self.remaining_order_qty}, fill_type: {self.fill_type}, fee_paid: {self.fee_paid}, fee_currency: {self.fee_currency}, taker_order_type: {self.taker_order_type}, order_type: {self.order_type} cli_ord_id: {self.cli_ord_id} Order id: {self.order_id} Fill id: {self.id} Time: {self.time}"

    def dtm(self) -> datetime:
        return datetime.fromtimestamp(self.time / 1000)
    
    def events(self) -> list[DomainEvent]:
        evs = self._events or []
        self._events = []
        return evs
    
    @staticmethod
    def from_feed(data) -> 'Fill':
        return Fill(
            data['fill_id']                 if 'fill_id' in data else "",
            data['instrument']              if 'instrument' in data else "",
            data['time']                    if 'time' in data else None,
            data['price']                   if 'price' in data else 0,
            data['buy']                     if 'buy' in data else None,
            data['qty']                     if 'qty' in data else None,
            data['remaining_order_qty']     if 'remaining_order_qty' in data else None,
            data['order_id']                if 'order_id' in data else None,
            data['fill_type']               if 'fill_type' in data else None,
            data['fee_paid']                if 'fee_paid' in data else None,
            data['fee_currency']            if 'fee_currency' in data else None,
            data['taker_order_type']        if 'taker_order_type' in data else None,
            data['order_type']              if 'order_type' in data else None,
            data['cli_ord_id']              if 'cli_ord_id' in data else None,
            data['cli_ord_id'].split('_')[0] if 'cli_ord_id' in data else "",
            True
        )

class Fills(list[Fill]):
    account: str
    '''The user account.'''

    def __init__(self, fills: list[Fill] = None, account: str = '') -> None:
        super().__init__(fills or [])
        self.account = account

    @staticmethod
    def from_feed(data) -> 'Fills':
        acc = data['account'] or data['username'] or ""
        return Fills([Fill.from_feed(fill) for fill in data['fills']], acc)
    
    def __str__(self) -> str:
        fills = "\n  ".join([str(fill) for fill in self[-3:]]) if len(self) > 0 else ""
        fills = f"\n  {fills}" if len(fills) > 0 else "No fills"
        return f"Fills:: fills: {len(self)} {fills}"
    
    def update(self, data) -> list[Fill]:
        try:
            if data is None:
                print("Data is None")
                return
            fs = [ Fill.from_feed(fill) for fill in data['fills'] ]
            for fill in fs:
                self.append(fill)
            return fs
        except Exception as e:
            print(f"Error updating fills: {e}")
            return []
    
    def for_position(self, position_id: Id) -> 'Fills':
        return Fills([fill for fill in self if fill.position_id == position_id])
    
    def for_order(self, order_id: Id) -> 'Fills':
        return Fills([fill for fill in self if fill.order_id == order_id])
    
    # def is_filled(self, order_id: Id) -> bool:
    #     o = self.for_order(order_id)
    #     if len(o) == 0:
    #         return False
    #     return any([fill for fill in o if fill.remaining_order_qty == 0])
    
    def is_filled(self) -> bool:
        return any([fill for fill in  self if fill.remaining_order_qty == 0])
    
    def closing_fills(self) -> 'Fills':
        return Fills([fill for fill in self if fill.order_type == 'close'])
    
    def last(self) -> Fill:
        return sorted(self, key=lambda x: x.seq, reverse=False)[-1]
    
    def tail(self, cnt: int = 5) -> list[Fill]:
        return sorted(self, key=lambda x: x.seq, reverse=False)[-cnt:]
    