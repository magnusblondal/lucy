
DOT = 'pf_dotusd'
BTC = 'pf_btcusd'
# BTC = 'fi_xbtusd'
        
ETH = 'pf_ethusd'
ATOM = 'pf_atomusd'

def pair_symbol(symbol: str):
    return f'pf_{symbol.lower()}usd'
