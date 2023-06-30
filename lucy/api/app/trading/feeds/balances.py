from ..flex import FuturesCurrency, Flex

class Balances:
    account: str
    '''The user account name'''
    timestamp: int
    '''The unix timestamp of the balance state in milliseconds'''
    seq: int
    '''The subscription message sequence number'''
    holding: dict[float]
    '''A map from currency names to balance quantity'''
    flex_futures: Flex

    def __init__(self, account: str, timestamp: int, seq: int, holding: dict[float] = None, flex_futures: Flex=None) -> None:
        self.account = account
        self.timestamp = timestamp
        self.seq = seq
        self.holding = holding
        self.flex_futures = flex_futures

    def __str__(self) -> str:
        return f"Balances:: account: {self.account}, timestamp: {self.timestamp}, seq: {self.seq},\n holding: {self.holding},\n flex_futures: \n{self.flex_futures}"
        # return f"Balances:: account: {self.account}, timestamp: {self.timestamp}, seq: {self.seq}, holding: {self.holding}, flex_futures: {self.flex_futures}"

    @staticmethod
    def from_feed(data) -> 'Balances':
        print("Balances:: from_feed")
        if data is None:
            return None
        try:
            return Balances(
                data['account'],
                data['timestamp'],
                data['seq'],
                data['holding'],
                Flex(data['flex_futures']) 
                )
        except Exception as e:
            print(e)
            return None
    
    def update(self, data) -> None:
        print("Balances:: update")
        print(data)
        if data is None:
            print("Balances:: update: data is None")
            return
        self.timestamp = data['timestamp']
        self.seq = data['seq']
        self.holding = data['holding'] if 'holding' in data else self.holding
        self.flex_futures = Flex(data['flex_futures'])

# futures	        map of structures	A map from single collateral wallet names to collateral wallet structure
# flex_futures	structure	        The multi-collateral wallet structure


{
    'feed': 'balances', 
    'account': 'e8d555f5-e7d3-42a5-b9fa-66fcdf856405', 
    'flex_futures': {'currencies': {'USDT': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.05, 'haircut': 0.05}, 'EURT': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.03}, 'FIL': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.1}, 'LTC': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.075}, 'SOL': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.075}, 'DOT': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.075}, 'GBP': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.05, 'haircut': 0.01}, 'USD CREDIT': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.0, 'haircut': 0.0}, 'USD': {'quantity': 71.24751035364, 'value': 71.24751035364, 'collateral_value': 71.24751035364, 'available': 60.1116901861002, 'conversion_spread': 0.0, 'haircut': 0.0}, 'USDC': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.05, 'haircut': 0.05}, 'ATOM': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.075}, 'XRP': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.075}, 'XBT': {'quantity': 0.00075389745, 'value': 22.926104383219503, 'collateral_value': 22.238321251722915, 'available': 0.00075389745, 'conversion_spread': 0.5, 'haircut': 0.03}, 'ETH': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.03}, 'LINK': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.075}, 'ARB': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.25, 'haircut': 0.1}, 'MATIC': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.05}, 'EUR': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.05, 'haircut': 0.01}, 'ADA': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.05}, 'DOGE': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.25, 'haircut': 0.05}}, 'balance_value': 94.17, 'portfolio_value': 70.54385018610019, 'collateral_value': 93.49, 'initial_margin': 9.752160000000002, 'initial_margin_without_orders': 9.752160000000002, 'maintenance_margin': 4.876080000000001, 'pnl': -23.62038684719999, 'unrealized_funding': -0.005762966699830491, 'total_unrealized': -23.62614981389982, 'total_unrealized_as_margin': -23.62614981389982, 'margin_equity': 69.86385018610018, 'available_margin': 60.11169018610018, 'isolated': {}, 'cross': {'balance_value': 94.17, 'portfolio_value': 70.54385018610019, 'collateral_value': 93.49, 'initial_margin': 9.752160000000002, 'initial_margin_without_orders': 9.752160000000002, 'maintenance_margin': 4.876080000000001, 'pnl': -23.62038684719999, 'unrealized_funding': -0.005762966699830491, 'total_unrealized': -23.62614981389982, 'total_unrealized_as_margin': -23.62614981389982, 'margin_equity': 69.86385018610018, 'available_margin': 60.11169018610018, 'effective_leverage': 6.979403492666548}}, 'timestamp': 1687965066608, 'seq': 2}

{
    'feed': 'balances_snapshot', 
    'account': 'e8d555f5-e7d3-42a5-b9fa-66fcdf856405', 
    'holding': {
        'ADA': 0.0, 'USDT': 0.0, 'EUR': 0.0, 'FEE': 0.0, 'FIL': 0.0, 'LTC': 0.0, 'SOL': 0.0, 'DOT': 0.0, 'GBP': 0.0, 'USDC': 0.0, 'USD': 0.0, 
        'USD CREDIT': 0.0, 'ATOM': 0.0, 'XRP': 0.0, 'XBT': 8.36e-09, 'ETH': 0.0, 'LINK': 0.0, 'ARB': 0.0, 'MATIC': 0.0, 'BCH': 0.0, 'DOGE': 0.0, 'EURT': 0.0
    }, 
    'futures': 
    {
        'F-XBT:USD': {'name': 'F-XBT:USD', 'pair': 'XBT/USD', 'unit': 'XBT', 'portfolio_value': 5.7968e-07, 'balance': 5.7968e-07, 'maintenance_margin': 0.0, 'initial_margin': 0.0, 'available': 5.7968e-07, 'unrealized_funding': 0.0, 'pnl': 0.0}, 
        'F-BCH:USD': {'name': 'F-BCH:USD', 'pair': 'BCH/USD', 'unit': 'BCH', 'portfolio_value': 0.0, 'balance': 0.0, 'maintenance_margin': 0.0, 'initial_margin': 0.0, 'available': 0.0, 'unrealized_funding': 0.0, 'pnl': 0.0}, 
        'F-ETH:USD': {'name': 'F-ETH:USD', 'pair': 'ETH/USD', 'unit': 'ETH', 'portfolio_value': 0.0, 'balance': 0.0, 'maintenance_margin': 0.0, 'initial_margin': 0.0, 'available': 0.0, 'unrealized_funding': 0.0, 'pnl': 0.0}, 
        'F-XRP:XBT': {'name': 'F-XRP:XBT', 'pair': 'XRP/XBT', 'unit': 'XBT', 'portfolio_value': 0.0, 'balance': 0.0, 'maintenance_margin': 0.0, 'initial_margin': 0.0, 'available': 0.0, 'unrealized_funding': 0.0, 'pnl': 0.0}, 
        'F-LTC:USD': {'name': 'F-LTC:USD', 'pair': 'LTC/USD', 'unit': 'LTC', 'portfolio_value': 0.0, 'balance': 0.0, 'maintenance_margin': 0.0, 'initial_margin': 0.0, 'available': 0.0, 'unrealized_funding': 0.0, 'pnl': 0.0}, 
        'F-XRP:USD': {'name': 'F-XRP:USD', 'pair': 'XRP/USD', 'unit': 'XRP', 'portfolio_value': 0.0, 'balance': 0.0, 'maintenance_margin': 0.0, 'initial_margin': 0.0, 'available': 0.0, 'unrealized_funding': 0.0, 'pnl': 0.0}}, 
    'flex_futures': 
    {
        'currencies': 
        {
            'USDT': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.05, 'haircut': 0.05}, 
            'EURT': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.03}, 
            'FIL': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.1}, 
            'LTC': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.075}, 
            'SOL': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.075}, 
            'DOT': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.075}, 
            'GBP': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.05, 'haircut': 0.01}, 
            'USD CREDIT': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.0, 'haircut': 0.0}, 
            'USD': {'quantity': 71.69940162885, 'value': 71.69940162885, 'collateral_value': 71.69940162885, 'available': 61.8590209541119, 'conversion_spread': 0.0, 'haircut': 0.0}, 
            'USDC': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.05, 'haircut': 0.05}, 
            'ATOM': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.075}, 
            'XRP': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.075}, 
            'XBT': {'quantity': 0.00075389745, 'value': 23.132928609652502, 'collateral_value': 22.438940751362924, 'available': 0.00075389745, 'conversion_spread': 0.5, 'haircut': 0.03}, 
            'ETH': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.03}, 
            'LINK': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.075}, 
            'ARB': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.25, 'haircut': 0.1}, 
            'MATIC': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.05}, 
            'EUR': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.05, 'haircut': 0.01}, 
            'ADA': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.5, 'haircut': 0.05}, 
            'DOGE': {'quantity': 0.0, 'value': 0.0, 'collateral_value': 0.0, 'available': 0.0, 'conversion_spread': 0.25, 'haircut': 0.05}
        }, 
        'balance_value': 94.83, 
        'portfolio_value': 72.68390095411185, 
        'collateral_value': 94.14, 
        'initial_margin': 10.134880000000003, 
        'initial_margin_without_orders': 9.789802000000002, 
        'maintenance_margin': 4.894901000000001, 
        'pnl': -22.143036646600045,
        'unrealized_funding': -0.003062399288107072,
        'total_unrealized': -22.146099045888153,
        'total_unrealized_as_margin': -22.146099045888153,
        'margin_equity': 71.99390095411185,
        'available_margin': 61.85902095411185,
        'isolated': {},
        'cross': 
        {
            'balance_value': 94.83,
            'portfolio_value': 72.68390095411185,
            'collateral_value': 94.14,
            'initial_margin': 10.134880000000003,
            'initial_margin_without_orders': 9.789802000000002,
            'maintenance_margin': 4.894901000000001,
            'pnl': -22.143036646600045,
            'unrealized_funding': -0.003062399288107072,
            'total_unrealized': -22.146099045888153,
            'total_unrealized_as_margin': -22.146099045888153,
            'margin_equity': 71.99390095411185,
            'available_margin': 61.85902095411185,
            'effective_leverage': 6.799049551600153
        }
    },
    'timestamp': 1687878634953, 
    'seq': 0
}