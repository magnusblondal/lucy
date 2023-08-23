from rich import inspect, print
from rich.table import Table

from lucy.model.signal import Signal
from .view import View

class SignalView(View):
            
    def lines(self, signals: list[Signal], indents:int = 0, verbose:bool = False) -> None:
    # --- Signals ---
        print(self.indent(self.dim(f'Signals: ', str(len(signals))), 2))
        for s in signals:
            self.line(s, indents + 1, verbose)
           
    def line(self, signal: Signal, indents:int = 0, verbose:bool = False) -> None:
        strat       = self.dim('Signal:', signal.strategy)
        sig         = self.right_pad(signal.signal_type, 9) 
        interv      = self.dim('interval', str(signal.interval))
        close       = self.dim('close:', signal.close)
        signal_time = self.dim('signal time:', signal.signal_time)
        id          = self.dim(str(signal.id))
        open_time   = self.dim('bar open time:', signal.bar_open_time)
        verb        = f"{signal_time} {open_time}" if verbose else ''
        p = f"{strat}, {signal.side}, {sig} {interv} {close} {id} {verb}"
        print(self.indent(p, indents + 1))