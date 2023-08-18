class Symbol(object):
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol.lower()

    def pf(self) -> str:
        s = self.symbol if self.symbol[:3] == 'pf_' else f'pf_{self.symbol}'
        if s[-3:] != 'usd':
            s = f"{s}usd"
        return s
    
    def __str__(self) -> str:
        return self.pf()
    
    def token(self) -> str:
        '''Token part of the trading pair'''
        s = self.symbol[3:] if self.symbol[:3] == 'pf_' else self.symbol
        s = s[:-3] if s[-3:] == 'usd' else s
        return s
    
    @staticmethod
    def DOT():
        return Symbol('dot')
    
    @staticmethod
    def ATOM():
        return Symbol('atom')

class Symbols(list[Symbol]):
    def __init__(self, symbols: list[Symbol] = None):
        super().__init__(symbols or [])

    def __str__(self) -> str:
        return ", ".join([str(s) for s in self])
    
    def tokens(self) -> list[str]:
        '''Returns  a list of the token names'''
        return [s.token() for s in self]

    def token_list(self) -> str:
        '''Returns the token names contained separated by space'''
        return " ".join(self.tokens())
    
    @staticmethod
    def from_str(symbols: str) -> 'Symbols':
        '''Returns a Symbols object from a string of symbols separated by space or comma'''
        if ',' in symbols:
            return Symbols([Symbol(s.replace(' ', '')) for s in symbols.split(",")])
        return Symbols([Symbol(s) for s in symbols.split(" ")])