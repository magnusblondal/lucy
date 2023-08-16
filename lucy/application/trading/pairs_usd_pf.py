
DOT = 'pf_dotusd'
BTC = 'pf_btcusd'
# BTC = 'fi_xbtusd'
        
ETH = 'pf_ethusd'
ATOM = 'pf_atomusd'

def pair_symbol(symbol: str):
    symbol = symbol.lower()
    s = symbol if symbol[:3] == 'pf_' else f'pf_{symbol}'
    if s[-3:] != 'usd':
        s = f"{s}usd"
    return s