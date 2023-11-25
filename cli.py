#!/usr/bin/env python
import click

from config import settings
from lucy.application.trading.exchange import Exchange
import lucy.application.trading.futures_socket_connector as web_socket_api
from lucy.cli.views.position_view import PositionsView
from lucy.cli.views.currency_view import CurrencyView
from lucy.cli.controllers.bot_controller import BotController
from lucy.cli.controllers.order_controller import OrderController
from lucy.cli.controllers.runner import Runner
from lucy.model.symbol import Symbol


def _positions():
    positions = Exchange().positions()
    PositionsView().listi(positions, 'Positions')


@click.group()
def cli():
    pass


@cli.command(help='Show Positions and Open Orders')
def info():
    _positions()
    OrderController().open_orders()


@cli.command(help='Show open Positions')
def pos():
    """
    Open Positions
    """
    _positions()


@cli.command()
def accounts():
    """
    Accounts list
    """
    accounts = Exchange().accounts()
    CurrencyView().listi(accounts, 'Accounts')

# __________ Orders ____________


@cli.command(help='Open orders')
def orders():
    """
    Open orders
    """
    OrderController().open_orders()


@cli.command(help='Create market order')
@click.argument('symbol')
@click.argument('qty')
@click.option('-s', '--short', is_flag=True, default=False, help='Short order')
def market(symbol, qty, short):
    """
    Market orders
    """
    OrderController().market_order(symbol, qty, short)


@cli.command(help='Buy by symbol')
@click.argument('symbol')
@click.argument('qty')
def buy(symbol, qty):
    """
    Buy by symbol
    """
    OrderController().buy(symbol, qty)


@cli.command(help='Sell by symbol')
@click.argument('symbol')
# , help='Quantity to sell. If not given, sell all.'
@click.argument('qty', default=0, type=click.FLOAT)
def sell(symbol, qty):
    """
    Sell by symbol
    """
    OrderController().sell(symbol, qty)


@cli.command(help='Close position by symbol')
@click.argument('symbol')
def close(symbol):
    """
    Close position by symbol
    """
    OrderController().close(Symbol(symbol))


@cli.command(help='Create limit order')
@click.argument('symbol')
@click.argument('qty')
@click.argument('price', type=click.FLOAT)
@click.option('-s', '--short', is_flag=True, default=False, help='Short order')
def limit(symbol, qty, price, short):
    """
    Create limit order
    """
    OrderController().limit_order(symbol, qty, price, short)


@cli.command(help='Cancel open orders; single symbol or all')
# , help='Symbol to cancel. If not given, cancel all.'
@click.argument('symbol', default="")
def cancel(symbol):
    """
    Cancel open orders; single symbol or all
    """
    OrderController().cancel(symbol)


@cli.command(help='Edit order')
@click.argument('order_id')
@click.argument('qty', type=click.FLOAT)
@click.argument('price', type=click.FLOAT)
def edit(order_id, qty, price):
    """
    Edit order by order id
    """
    OrderController().edit(order_id, qty, price)


@cli.command(help='Order status')
@click.argument('order_id')
def status(order_id):
    """
    Order status by order id
    """
    OrderController().order_status(order_id)


@cli.command()
def executions():
    for x in Exchange().executions():
        print(x)


# __________ Bot ____________


@cli.command(help="Show bots list")
def bots():
    """
    All bots list
    """
    BotController().list_bots()


@cli.command(help="Show Bot details")
@click.option('-v', '--verbose',
              is_flag=True, default=False, help='Show further details')
@click.option('-s', '--signals',
              is_flag=True, default=False, help='Show signals')
@click.argument('id', type=click.STRING)
def bot(id: str, verbose: bool, signals: bool):
    """
    Single bot info
    """
    BotController().bot_info(id, verbose, signals)


@cli.command(help="Add new bot")
@click.argument('type', type=click.STRING, default="bot")
def add(type):
    """
    Add new bot
    """
    if type == "bot":
        BotController().add()
    else:
        print("Unknown bot type")


@cli.command(help="Edit bot")
@click.argument('id', type=click.STRING)
# TODO: fall med sama heiti er til
def edit(id):
    """
    Edit bot
    """
    BotController().edit(id)


@cli.command(help="Calculate PnL for bot")
@click.argument('id')
def audit(id):
    """
    Calculate PnL for bot
    """
    BotController().audit(id)


@cli.command(help="Start bot")
@click.argument('id')
def start(id):
    """
    Start bot
    """
    BotController().start_bot(id)


@cli.command(help="Stop bot")
@click.argument('id', type=click.STRING, default="")
def stop(id):
    """
    Stop bot
    """
    if id == "":
        click.confirm('Stop all bots?', abort=True)
        BotController().stop_all_bots()
    else:
        BotController().stop_bot(id)


@cli.command(help='Listen to websocket')
def listen():
    """
    Listen to websocket
    """
    print("Listening...")
    web_socket_api.listen(settings)


@cli.command(help='Run Forrest, run!')
def run():
    """
    Run bots
    """
    Runner().start()


if __name__ == '__main__':
    cli()
