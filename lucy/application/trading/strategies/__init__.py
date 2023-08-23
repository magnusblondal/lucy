from .strategy import Strategy
from .bb_breakout import BBbreakout
from .rsi_crossover import RsiCrossover

import sys, inspect

def make(name) -> Strategy:
    if name == "Strategy":
        raise ValueError("Strategy name cannot be 'Strategy'")

    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    strat = [(x[0], x[1]) for x in clsmembers if x[0].lower() == name.lower()]
    if not strat:
        raise ValueError(f"Strategy {name} not found")    
    return strat[0][1].__call__()

def list() -> list[str]:
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    strat = [(x[0], x[1]) for x in clsmembers if x[0] != "Strategy"]
    return [x[0] for x in strat]