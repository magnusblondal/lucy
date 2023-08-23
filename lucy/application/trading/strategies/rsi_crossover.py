from .strategy import Strategy

class RsiCrossover(Strategy):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)