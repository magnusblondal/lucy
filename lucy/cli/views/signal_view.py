from rich import inspect, print
from rich.table import Table

from lucy.model.signal import Signal
from .view import View

class SignalView(View):
            
    def lines(self, signals: list[Signal], indents:int = 0, verbose:bool = False) -> None:
    # --- Signals ---
        print(self.indent(self.dim(f'Signals: ', str(len(signals))), 2))
        for s in signals:
            strat = self.dim('strategy:', s.strategy)
            sig = self.right_pad(s.signal_type, 9) 
            interv = self.dim('interval', str(s.interval))
            close = self.dim('close:', s.close)
            signal_time = self.dim('signal time:', s.signal_time)
            id = self.dim('id:', str(s.id))
            # sig = "{:<9}".format(f"{s.signal_type}") 
            
            open_time =self.dim('bar open time:', s.bar_open_time)
            verb = f"{open_time}"
            p = f"{strat}, {s.side}, {sig} {interv} {close} {signal_time} {id} {verb}"
            print(self.indent(p, indents + 1))