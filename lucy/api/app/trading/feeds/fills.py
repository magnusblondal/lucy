
class Fill:
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
    fill_id: str
    '''The fill id.'''
    fill_type: str
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

    def __init__(self, instrument: str, time: int, price: float, seq: int, buy: bool, qty: float, remaining_order_qty: float, order_id: str, fill_id: str, fill_type: str, fee_paid: float, fee_currency: str, taker_order_type: str, order_type: str, cli_ord_id: str) -> None:
        self.instrument = instrument
        self.time = time
        self.price = price
        self.seq = seq
        self.buy = buy
        self.qty = qty
        self.remaining_order_qty = remaining_order_qty
        self.order_id = order_id
        self.fill_id = fill_id
        self.fill_type = fill_type
        self.fee_paid = fee_paid
        self.fee_currency = fee_currency
        self.taker_order_type = taker_order_type
        self.order_type = order_type
        self.cli_ord_id = cli_ord_id

    def __str__(self) -> str:
        return f"Fill:: instrument: {self.instrument}, time: {self.time}, price: {self.price}, seq: {self.seq}, buy: {self.buy}, qty: {self.qty}, remaining_order_qty: {self.remaining_order_qty}, order_id: {self.order_id}, fill_id: {self.fill_id}, fill_type: {self.fill_type}, fee_paid: {self.fee_paid}, fee_currency: {self.fee_currency}, taker_order_type: {self.taker_order_type}, order_type: {self.order_type}, cli_ord_id: {self.cli_ord_id}"

    @staticmethod
    def from_feed(data) -> 'Fill':
        return Fill(
            data['instrument']              if 'instrument' in data else "",
            data['time']                    if 'time' in data else None,
            data['price']                   if 'price' in data else None,
            data['seq']                     if 'seq' in data else None,
            data['buy']                     if 'buy' in data else None,
            data['qty']                     if 'qty' in data else None,
            data['remaining_order_qty']     if 'remaining_order_qty' in data else None,
            data['order_id']                if 'order_id' in data else None,
            data['fill_id']                 if 'fill_id' in data else None,
            data['fill_type']               if 'fill_type' in data else None,
            data['fee_paid']                if 'fee_paid' in data else None,
            data['fee_currency']            if 'fee_currency' in data else None,
            data['taker_order_type']        if 'taker_order_type' in data else None,
            data['order_type']              if 'order_type' in data else None,
            data['cli_ord_id']              if 'cli_ord_id' in data else None,
        )


class Fills:
    fills: list[Fill]
    account: str
    '''The user account.'''

    def __init__(self, account: str, fills) -> None:
        self.account = account
        self.fills = fills

    @staticmethod
    def from_feed(data) -> 'Fills':
        acc = data['account'] or data['username'] or ""
        return Fills(acc, [Fill.from_feed(fill) for fill in data['fills']])
    
    def __str__(self) -> str:
        fills = "\n  ".join([str(fill) for fill in self.fills[-3:]]) if len(self.fills) > 0 else ""
        fills = f"\n  {fills}" if len(fills) > 0 else "No fills"
        return f"Fills:: fills: {len(self.fills)} {fills}"
    
    def update(self, data) -> None:
        try:
            if data is None:
                print("Data is None")
                return
            fs = [ Fill.from_feed(fill) for fill in data['fills'] ]
            for fill in fs:
                self.fills.append(fill)
        except Exception as e:
            print(f"Error updating fills: {e}")