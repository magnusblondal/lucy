from rich import print
from rich.table import Table

from lucy.model.bot import Bots, DcaBot
from .view import View
from .position_view import PositionsView


class BotView(View):
    def __init__(self):
        self.position_view = PositionsView()

    def listi(self, bots: Bots, header: str = "") -> None:
        table = Table()
        if header:
            table.title = header

        for c in ['Id', 'Name', 'Active', 'Strategy', 'Symbol', 'Interval',
                  'Max pos.', 'Capital', 'Entry size', 'SO Size', 'Max SO\'s',
                  'Shorts', 'Tot. pos\'s', 'Open pos\'s', 'Profit']:
            table.add_column(f"{self.COLUMN_HEADER_COL}{c}")

        for b in bots:
            capital = "{:>10}".format(b.capital)
            interval = "{:>5}".format(str(b.interval))
            strategy = "{:>9}".format(b.strategy.name)
            max_positions = "{:>5}".format(b.num_positions_allowed)
            entry_size = "{:>8}".format(f"{b.entry_size:.1f}")
            so_size = "{:>7}".format(f"{b.so_size:.1f}")
            max_safety_orders = "{:>4}".format(b.max_safety_orders)
            openPos = "{:>6}".format(b.num_open_positions())
            posCnt = "{:>6}".format(len(b.positions))
            profit = "{:>6}".format(f"${b.profit():.2f}")
            is_active = "{:>3}".format(self.open_or_closed(b.active))
            allow_shorts = "{:>3}".format(self.open_or_closed(b.allow_shorts))

            # symbols             = "{:>9}".format(b.symbols.token_list())
            s = b.symbols.token_list()
            symbols = "{:>9}".format(b.symbols.token_list())
            c = str.count(s, ',')
            if c > 2:
                snd_comma = str.index(s, ',', str.index(s, ',') + 1)
                more = len(b.symbols) - 2
                symbols = f"{b.symbols.token_list()[:snd_comma]} + {more} more"

            table.add_row(b.id.id, self.emp(b.name), is_active, strategy,
                          symbols, interval, max_positions, capital,
                          entry_size, so_size, max_safety_orders, allow_shorts,
                          posCnt, openPos, profit)
        print(table)

    def show(
        self,
        bot: DcaBot,
        show_signals: bool,
        verbose: bool = False
    ) -> None:
        if not bot:
            self.warning("No bot found")
            return

        is_active = self.open(
            "ACTIVE") if bot.active else self.closed("INACTIVE")
        symbols = self.emp(str(bot.symbols)) if len(
            bot.symbols) > 0 else self.dim("No symbols")
        strategy = self.emp(bot.strategy.name)
        shorts = "Shorts allowed" if bot.allow_shorts else "No shorts"
        pos = f"{bot.num_positions_allowed} {self.dim('concurrent positions.')}"
        cap = f"{self.dim('Capital:')} {bot.capital:.0f}"
        entry_size = f"{self.dim('Entry size:')} {bot.entry_size:.0f}"
        so_size = f"{self.dim('SO Size:')} {bot.so_size:.0f}"
        max_safety_orders = f"{self.dim('Max SOs:')} {bot.max_safety_orders}"
        id = self.dim(str(bot.id))
        print(f"{self.emp(bot.name)}  {is_active} {strategy} {bot.interval} {pos}  {cap}  {entry_size}  {so_size}  {max_safety_orders}  {shorts}  {id}")
        print(f" {symbols}")
        if bot.has_description() and verbose:
            self.desc(bot.description)

        # --- Positions ---
        self.position_view.lines(bot.positions, 1, show_signals, verbose)
