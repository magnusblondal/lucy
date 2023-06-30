from typing import List

from rich import inspect, print
from rich.table import Table

from api.app.trading.open_order import OpenOrder
from api.app.models.bot import DcaBot, Bot

from .view import View

class BotView(View):
    def listi(self, bots: list[Bot], header: str=None) -> None:
        table = Table()
        if header:
            table.title = header
        for c in ['Id', 'Name', 'Active', 'Max pos.', 'Capital', 'Entry size', 'SO Size', 'Max SO\'s', 'Shorts', 'Tot. pos\'s', 'Open pos\'s', 'Profit']:
            table.add_column(f"{self.COLUMN_HEADER_COL}{c}")
            
        for b in bots:
            capital             = "{:>10}".format(b.capital)
            max_positions       = "{:>6}".format(b.num_positions_allowed)
            entry_size          = "{:>6}".format(f"{b.entry_size:.1f}")
            so_size             = "{:>6}".format(f"{b.so_size:.1f}")
            max_safety_orders   = "{:>4}".format(b.max_safety_orders)
            openPos             = "{:>6}".format(b.num_open_positions())
            posCnt              = "{:>6}".format(len(b.positions))
            profit              = "{:>6}".format(f"${b.profit():.2f}") 
            is_active           = self.open("ACTIVE") if b.active else self.closed("INACTIVE")
            shorts = "✅" if b.allow_shorts else "❌"
            allow_shorts        = "{:>3}".format(shorts)
            table.add_row(b.id.id, self.emp(b.name), is_active, max_positions, capital, entry_size, so_size, max_safety_orders, allow_shorts, posCnt, openPos, profit)
        print(table)

    def show(self, bot: DcaBot, verbose: bool=False) -> None:
        is_active           = self.open("ACTIVE") if bot.active else self.closed("INACTIVE")
        shorts = "Shorts allowed" if bot.allow_shorts else "No shorts"
        pos = f"{bot.num_positions_allowed} {self.dim('concurrent positions.')}"

        print(f"{self.emp(bot.name)}  {is_active} {pos}  {self.dim('Capital:')} {bot.capital:.0f}  {self.dim('Entry size:')} {bot.entry_size:.0f}  {self.dim('SO Size:')} {bot.so_size:.0f}  {self.dim('Max SOs:')} {bot.max_safety_orders}  {shorts}  {self.dim('Id:', bot.id)}")
        if bot.has_description() and verbose:
            self.desc(bot.description)
        
        # --- Positions ---
        print(f"{self.dim('Positions:')} {len(bot.positions)} {self.dim('Profit:')} ${bot.profit():.6f}")
        for d in bot.positions:
            open_closed = self.open_or_closed(d.is_open()) 
            posStr = f"{self.emp('Position:')} {open_closed} {d.symbol} {self.dim('Side:')} {d.side} {self.dim('Qty:', d.open_qty())} {self.dim('Profit:')} ${d.profit:.2f} {d.profit_pct:.2f}%   {self.dim('Id:', d.id)}"
            print(self.indent(posStr))
            
            # --- Signals ---
            print(self.indent(self.dim(f'Signals: ', len(d.signals)), 2))
            for s in d.signals:
                sig = self.right_pad(s.signal_type, 9) 
                # sig = "{:<9}".format(f"{s.signal_type}") 
                p = f"{self.dim('strategy:', s.strategy)}, {s.ticker}, {s.side}, {sig} {s.interval} {self.dim('close:', s.close)} {self.dim('bar open time:', s.bar_open_time)} {self.dim('signal time:', s.signal_time)} {self.dim('id:', s.id)}"
                print(self.indent(p, 3))
            
            # --- Orders ---
            print(self.indent(self.dim(f'Orders: ', len(d.orders)), 2))
            for o in d.orders:
                # client_id = self.dim('cli_ord_id:', o.cli_ord_id) if o.cli_ord_id else ''
                pric = self.dim('price:', self.left_pad(f"{o.price:.3f}", 9))
                qty = self.dim('qty:', "{:<6}".format(o.qty))
                sid = self.dim('side:', "{:<5}".format(o.side))
                reduce = 'Reduce only' if o.reduce_only else ''
                verb = f"{self.dim('id:', o.id)} {self.dim('position id:', o.position_id)} {self.dim('bot id:', o.bot_id)} {self.dim('exch id:', o.exchange_id)}" if verbose else ''
                p = f"{o.symbol} {qty} {pric} {sid} {self.dim('type:', o.type)}  {self.dim('filled:', o.filled)}  {self.dim('limit price:', o.limit_price)}  {reduce}  {verb}"
                print(self.indent(p, 3))
            