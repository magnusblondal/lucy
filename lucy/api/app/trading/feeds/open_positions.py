
class OpenPosition:
    instrument: str
    '''The instrument (referred also as symbol or product_id) of the position ('PF_ATOMUSD').'''
    balance: float
    '''The size of the position. Negative numer is a short position, positive is a long position.'''
    pnl: float
    '''The profit and loss of the position.'''
    entry_price: float
    '''The average entry price of the instrument.'''
    mark_price: float 
    '''The market price of the position instrument.'''
    index_price: float
    '''The index price of the position instrument.'''
    liquidation_threshold: float
    '''The mark price of the contract at which the position will be liquidated.'''
    effective_leverage: float
    '''How leveraged the net position is in a given margin account. Formula: Position Value at Market / Portfolio Value.'''
    return_on_equity: float
    '''The percentage gain or loss relative to the initial margin used in the position. Formula: PnL/IM'''
    unrealized_funding: float
    initial_margin: float
    initial_margin_with_orders: float
    maintenance_margin: float
    pnl_currency: str

    def __init__(self, instrument: str, balance: float, pnl: float, entry_price: float, mark_price: float, 
                 index_price: float, liquidation_threshold: float, effective_leverage: float, return_on_equity: float, 
                 unrealized_funding: float, initial_margin: float, initial_margin_with_orders: float, 
                 maintenance_margin: float, pnl_currency: str) -> None:
        self.instrument = instrument
        self.balance = balance
        self.pnl = pnl
        self.entry_price = entry_price
        self.mark_price = mark_price
        self.index_price = index_price
        self.liquidation_threshold = liquidation_threshold
        self.effective_leverage = effective_leverage
        self.return_on_equity = return_on_equity
        self.unrealized_funding = unrealized_funding
        self.initial_margin = initial_margin
        self.initial_margin_with_orders = initial_margin_with_orders
        self.maintenance_margin = maintenance_margin
        self.pnl_currency = pnl_currency
    
    def __str__(self) -> str:
        return f"OpenPosition:: instrument: {self.instrument}, balance: {self.balance}, pnl: {self.pnl}, entry_price: {self.entry_price}, mark_price: {self.mark_price}, index_price: {self.index_price}, liquidation_threshold: {self.liquidation_threshold}, effective_leverage: {self.effective_leverage}, return_on_equity: {self.return_on_equity}, unrealized_funding: {self.unrealized_funding}, initial_margin: {self.initial_margin}, initial_margin_with_orders: {self.initial_margin_with_orders}, maintenance_margin: {self.maintenance_margin}, pnl_currency: {self.pnl_currency}"
        
    def from_feed(data) -> 'OpenPosition':
        return OpenPosition(
            data['instrument'], 
            data['balance'],
            data['pnl'],
            data['entry_price'],
            data['mark_price'],
            data['index_price'],
            data['liquidation_threshold'],
            data['effective_leverage'],
            data['return_on_equity'],
            data['unrealized_funding'],
            data['initial_margin'],
            data['initial_margin_with_orders'],
            data['maintenance_margin'],
            data['pnl_currency'])

class OpenPositions:
    account: str
    '''The user account.'''
    positions: list[OpenPosition]
    '''A list containing the user open positions.'''
    seq: int
    timestamp: int

    def __init__(self, account: str, positions: list[OpenPosition], seq: int, timestamp: int) -> None:
        self.account = account
        self.positions = positions
        self.seq = seq
        self.timestamp = timestamp

    def __str__(self) -> str:
        ps = '\n'.join([f"  {str(p)}" for p in self.positions])
        return f'OpenPositions(account={self.account}, seq={self.seq}, timestamp={self.timestamp}, positions=\n{ps})'

    def from_feed(data) -> 'OpenPositions':        
        positions = [OpenPosition.from_feed(p) for p in data['positions']]
        return OpenPositions(
            data['account'],
            positions,
            data['seq'],
            data['timestamp'])
