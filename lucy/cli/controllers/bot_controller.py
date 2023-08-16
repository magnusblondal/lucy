import click
from rich import inspect

import lucy.application.events.bus as bus

from lucy.cli.views.bot_view import BotView
from lucy.model.bot import DcaBot
from lucy.model.create_bot import CreateDcaBot, EditDcaBot
from lucy.infrastructure.repos.bot_repository import BotRepository

from lucy.application.usecases.bots.bot_activation import BotActivation
from lucy.application.usecases.bots.audit import AuditBot

class BotController:
    view: BotView = BotView()
    repo:BotRepository = BotRepository()

    def add(self):
        '''Add new Bot'''
        self.view.process_title("Add new bot")
        name                = click.prompt('Name',                      type=str)
        type                = click.prompt('Type',                      type=str, default='DCA')
        active              = click.prompt('Active',                    type=bool, default=True)
        symbol              = click.prompt('Symbol',                    type=str, default='BTCUSD')
        interval            = click.prompt('Interval (1 5 15 60  240 (4h)  1440 (24h))',                  type=int,  default=60)
        max_positions       = click.prompt('Max Concurrent Positions',  type=int,  default=1)
        capital             = click.prompt('Capital',                   type=float)
        entry_size          = click.prompt('Entry Size',                type=float)
        so_size             = click.prompt('SO Size',                   type=float)
        max_safety_orders   = click.prompt('Max Safety Orders',         type=int)
        allow_shorts        = click.prompt('Allow Shorts',              type=bool, default=False)
        desc                = click.prompt('Description',               type=str, default='')

        gen = CreateDcaBot(
            name = name,
            description = desc,
            capital = capital,
            entry_size = entry_size,
            so_size = so_size,
            max_safety_orders = max_safety_orders,
            allow_shorts = allow_shorts,
            max_positions_allowed = max_positions,
            interval = interval,
            symbol = symbol)

        bot = DcaBot.create_new(gen)
        repo = BotRepository()
        repo.save(bot)

        self.view.confirmation(f"Bot '{bot.name}' created. Id: '{bot.id}'")

    def edit(self, id: str):
        '''Edit Bot'''
        bot = self.repo.fetch_bot(id)
        if bot is None:
            self.view.warning(f"Bot with id '{id}' not found")
            return

        self.view.process_title(f"Edit bot '{bot.name}' (id: {bot.id})")
        name                = click.prompt('Name', type=str, default=bot.name)
        active              = click.prompt('Active', type=bool, default=bot.active)
        symbol              = click.prompt('Symbol',                    type=str, default=bot.symbol)
        interval            = click.prompt('Interval (1 5 15 60  240 (4h)  1440 (24h))', type=int,  default=bot.interval.interval)
        max_positions       = click.prompt('Max Concurrent Positions',  type=int,  default=bot.num_positions_allowed)
        capital             = click.prompt('Capital', type=float, default=bot.capital)
        entry_size          = click.prompt('Entry Size', type=float, default=bot.entry_size)
        so_size             = click.prompt('SO Size', type=float, default=bot.so_size)
        max_safety_orders   = click.prompt('Max Safety Orders', type=int, default=bot.max_safety_orders)
        allow_shorts        = click.prompt('Allow Shorts', type=bool, default=bot.allow_shorts)
        desc                = click.prompt('Description', type=str, default=bot.description)

        edit = EditDcaBot(
            name = name,
            description = desc,
            capital = capital,
            entry_size = entry_size,
            so_size = so_size,
            max_safety_orders = max_safety_orders,
            allow_shorts = allow_shorts,
            max_positions_allowed = max_positions,
            interval = interval,
            symbol = symbol)
        bot.update(edit)

        if click.confirm('Do you want to continue?', default=True, abort=True):
            self.repo.update(bot)
            self.view.confirmation(f"Bot updated. Id: '{bot.id}'")

    def audit(self, id: str):
        '''Audit bot; calculate profit/loss'''
        AuditBot().handle(id)

    def list_bots(self):
        '''List all bots'''
        bots = self.repo.fetch_bots()
        self.view.listi(bots, 'Bots')

    def bot_info(self, id: str, verbose: bool, signals: bool):
        '''Show bot details'''
        bot = self.repo.fetch_bot(id)
        self.view.show(bot, signals, verbose)

    def _activation_callback(self, result, id: str, starting: bool):
        if result is None:
            self.view.warning(f"No results received.")
        elif result.success and id == "all" and not starting:
            self.view.confirmation(f"All bots turned off.")
        elif result.success:
            msg = "started" if starting else "stopped"
            self.view.confirmation(f"'{result.bot.name}' {msg}.")
        elif result.bot is None:
            self.view.warning(f"Bot with id '{id}' not found")

    def start_bot(self, id: str):
        '''Start bot'''
        result = BotActivation().handle(id, True)
        self._activation_callback(result, id, True)
        
    def stop_bot(self, id: str):
        '''Stop bot'''
        result = BotActivation().handle(id, False)
        self._activation_callback(result, id, False)
    
    def stop_all_bots(self):
        '''Stop all bots'''
        result = BotActivation().handle(None, False)
        self._activation_callback(result, "all", False)