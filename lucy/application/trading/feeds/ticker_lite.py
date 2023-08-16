
class TickerLite():
    product_id: str             
    '''The subscribed product (referred also as instrument or symbol; 'PI_XBTUSD')'''
    bid: float                  
    '''The price of the current best bid'''
    ask: float                  
    '''The price of the current best ask'''
    change: float               
    '''The 24h change in price'''
    premium: float              
    '''The premium associated with the product'''
    volume: float               
    '''The sum of the sizes of all fills observed in the last 24 hours'''
    tag: str                    
    '''Currently can be week, month or quarter. Other tags may be added without notice. ('perpetual')'''
    pair: str                   
    '''The currency pair of the instrument ('XBT:USD')'''
    dtm: int                  
    '''The days until maturity'''
    maturityTime: int         
    '''Maturity time in milliseconds'''
    volumeQuote: float          
    '''The same as volume except that, for multi-collateral futures, it is converted to the non-base currency'''

    def __init__(self, product_id: str, bid: float, ask: float, change: float, premium: float, volume: float, 
                 tag: str, pair: str, dtm: int, maturityTime:int, volumeQuote: float) -> None:
        self.product_id = product_id
        self.bid = bid
        self.ask = ask
        self.change = change
        self.premium = premium
        self.volume = volume
        self.tag = tag
        self.pair = pair
        self.dtm = dtm
        self.maturityTime = maturityTime
        self.volumeQuote = volumeQuote

    def __str__(self) -> str:
        return f"TickerLite:: product_id: {self.product_id}, bid: {self.bid}, ask: {self.ask}, change: {self.change}, premium: {self.premium}, volume: {self.volume}, tag: {self.tag}, pair: {self.pair}, dtm: {self.dtm}, maturityTime: {self.maturityTime}, volumeQuote: {self.volumeQuote}"

    @staticmethod
    def from_feed(data) -> 'TickerLite':
        return TickerLite(
            data['product_id'], 
            data['bid'],
            data['ask'],
            data['change'],
            data['premium'],
            data['volume'],
            data['tag'],
            data['pair'],
            data['dtm'],
            data['maturityTime'],
            data['volumeQuote'])
    
# {
#     'feed': 'ticker_lite', 
#     'product_id': 'PI_XBTUSD', 
#     'bid': 30571.5, 
#     'ask': 30574.0, 
#     'change': -0.3243842404681563,
#     'premium': -0.0,
#     'volume': 15466700.0,
#     'tag': 'perpetual',
#     'pair': 'XBT:USD',
#     'dtm': 0,
#     'maturityTime': 0,
#     'volumeQuote': 15466700.0
# }