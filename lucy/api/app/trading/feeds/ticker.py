


class Ticker:
    time: int
    '''The UTC time of the server in milliseconds'''
    product_id: str                                   
    '''The subscribed product (referred also as instrument or symbol)'''
    funding_rate: float
    '''(Perpetuals only) The current funding rate. If zero, field is not populated.'''
    funding_rate_prediction: float
    '''(Perpetuals only) The estimated next funding rate. If zero, field is not populated.'''
    relative_funding_rate: float
    '''(Perpetuals only) The absolute funding rate relative to the spot price at the time of funding rate calculation. If zero, field is not populated.'''
    relative_funding_rate_prediction: float
    '''(Perpetuals only) The estimated next absolute funding rate relative to the current spot price. If zero, field is not populated.'''
    next_funding_rate_time: int                                   
    '''(Perpetuals only) The time until next funding rate in milliseconds.'''

    bid: float
    '''The price of the current best bid'''
    ask: float
    '''The price of the current best ask'''
    bid_size: float
    '''The size of the current best bid'''
    ask_size: float
    '''The size of the current best ask'''
    volume: float
    '''The sum of the sizes of all fills observed in the last 24 hours'''
    dtm: int
    '''The days until maturity'''
    leverage: float
    '''The leverage of the product'''
    index: float
    '''The real time index of the product'''
    premium: float
    '''The premium associated with the product'''
    last: float
    '''The price of the last trade of the product'''
    change: float
    '''The 24h change in price'''
    suspended: bool
    '''True if the market is suspended, false otherwise'''
    tag: str
    '''Currently can be perpetual, month or quarter. Other tags may be added without notice. ('perpetual')'''
    pair: str                                 # 'XBT:USD',
    '''The currency pair of the instrument'''
    openInterest: float
    '''The current open interest of the instrument'''
    markPrice: float 
    '''The market price of the instrument'''
    maturityTime: int
    '''The UTC time, in milliseconds, at which the contract will stop trading'''
    post_only: bool
    '''True if the market is in post-only, false otherwise'''
    volumeQuote: float
    '''The same as volume except that, for multi-collateral futures, it is converted to the non-base currency'''



    def __init__(self, time: int, product_id: str, funding_rate: float, funding_rate_prediction: float, relative_funding_rate: float, relative_funding_rate_prediction: float, next_funding_rate_time: int, bid: float, ask: float, bid_size: float, ask_size: float, volume: float, dtm: int, leverage: float, index: float, premium: float, last: float, change: float, suspended: bool, tag: str, pair: str, openInterest: float, markPrice: float, maturityTime: int, post_only: bool, volumeQuote: float) -> None:
        self.time = time
        self.product_id = product_id
        self.funding_rate = funding_rate
        self.funding_rate_prediction = funding_rate_prediction
        self.relative_funding_rate = relative_funding_rate
        self.relative_funding_rate_prediction = relative_funding_rate_prediction
        self.next_funding_rate_time = next_funding_rate_time
        self.bid = bid
        self.ask = ask
        self.bid_size = bid_size
        self.ask_size = ask_size
        self.volume = volume
        self.dtm = dtm
        self.leverage = leverage
        self.index = index
        self.premium = premium
        self.last = last
        self.change = change
        self.suspended = suspended
        self.tag = tag
        self.pair = pair
        self.openInterest = openInterest
        self.markPrice = markPrice
        self.maturityTime = maturityTime
        self.post_only = post_only
        self.volumeQuote = volumeQuote

    def __str__(self) -> str:
        return f'{self.time}, {self.product_id}, {self.funding_rate}, {self.funding_rate_prediction}, {self.relative_funding_rate}, {self.relative_funding_rate_prediction}, {self.next_funding_rate_time}, {self.bid}, {self.ask}, {self.bid_size}, {self.ask_size}, {self.volume}, {self.dtm}, {self.leverage}, {self.index}, {self.premium}, {self.last}, {self.change}, {self.suspended}, {self.tag}, {self.pair}, {self.openInterest}, {self.markPrice}, {self.maturityTime}, {self.post_only}, {self.volumeQuote}'

    @staticmethod
    def from_feed(data) -> 'Ticker':
        return Ticker(
            data['time'], 
            data['product_id'], 
            data['funding_rate'] if 'funding_rate' in data else 0,
            data['funding_rate_prediction'] if 'funding_rate_prediction' in data else 0,
            data['relative_funding_rate'] if 'relative_funding_rate' in data else 0,
            data['relative_funding_rate_prediction'] if 'relative_funding_rate_prediction' in data else 0,
            data['next_funding_rate_time'] if 'next_funding_rate_time' in data else 0,
            data['bid'],
            data['ask'],
            data['bid_size'],
            data['ask_size'],
            data['volume'],
            data['dtm'],
            data['leverage'],
            data['index'],
            data['premium'],
            data['last'],
            data['change'],
            data['suspended'],
            data['tag'],
            data['pair'],
            data['openInterest'],
            data['markPrice'],
            data['maturityTime'],
            data['post_only'],
            data['volumeQuote'])

# {
#     'time': 1687797353208,
#     'product_id': 'PI_XBTUSD',
#     'funding_rate': 1.96583215e-10,
#     'funding_rate_prediction': 1.01989374e-10,
#     'relative_funding_rate': 5.979856944444e-06,
#     'relative_funding_rate_prediction': 3.091184722222e-06,
#     'next_funding_rate_time': 1687798800000,
#     'feed': 'ticker',
#     'bid': 30293.0,
#     'ask': 30296.0,
#     'bid_size': 6000.0,
#     'ask_size': 7595.0,
#     'volume': 15302295.0,
#     'dtm': 0,
#     'leverage': '50x',
#     'index': 30296.46,
#     'premium': -0.0,
#     'last': 30296.5,
#     'change': -0.7908179972493268,
#     'suspended': False,
#     'tag': 'perpetual',
#     'pair': 'XBT:USD',
#     'openInterest': 33568965.0,
#     'markPrice': 30297.40063963151,
#     'maturityTime': 0,
#     'post_only': False,
#     'volumeQuote': 15302295.0
# }