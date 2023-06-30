#!/usr/bin/env python
import click

from api.app.trading.pairs_usd_pf import *
from api.app.trading.exchange import Exchange
import api.app.trading.futures_socket_connector as web_socket_api

from cli.views.position_view import PositionsView
from cli.views.currency_view import CurrencyView
from cli.controllers.bot_controller import BotController
from cli.controllers.order_controller import OrderController

from rich import inspect

def _positions():
    positions = Exchange().positions()
    PositionsView().listi(positions, 'Positions')


@click.group()
def cli():
    pass

@cli.command()
def info():
    _positions()
    OrderController().open_orders()

@cli.command()
def pos():
    _positions()

@cli.command()
def accounts():
    accounts = Exchange().accounts()
    CurrencyView().listi(accounts, 'Accounts')

# __________ Orders ____________
# ----------
# Open Orders
# ----------
@cli.command()
def orders():
    OrderController().open_orders()

# ----------
# Market orders
# ----------
@cli.command()
@click.argument('symbol')
@click.argument('qty')
@click.option('-s', '--short', is_flag=True, default=False, help='Short order')
def market(symbol, qty, short):
    OrderController().market_order(symbol, qty, short)

# ----------
# Buy
# ----------
@cli.command()
@click.argument('symbol')
@click.argument('qty')
def buy(symbol, qty):
    OrderController().buy(symbol, qty)
    
# ----------
# Sell
# ----------
@cli.command()
@click.argument('symbol')
@click.argument('qty', default=0, type=click.FLOAT) # , help='Quantity to sell. If not given, sell all.'
def sell(symbol, qty):
    OrderController().sell(symbol, qty)

# ----------
# Close position
# ----------
@cli.command()
@click.argument('symbol')
def close(symbol):
    OrderController().close(symbol)

# ----------
# Limit Order
# ----------
@cli.command()
@click.argument('symbol')
@click.argument('qty')
@click.argument('price', type=click.FLOAT)
@click.option('-s', '--short', is_flag=True, default=False, help='Short order')
def limit(symbol, qty, price, short):
    OrderController().limit_order(symbol, qty, price, short)
    
# ----------
# Cancel orders
# ----------
@cli.command(help='Cancel open orders; single symbol or all')
@click.argument('symbol', default="") # , help='Symbol to cancel. If not given, cancel all.'
def cancel(symbol):
    OrderController().cancel(symbol)

# ----------
# Edit order
# ----------
@cli.command()
@click.argument('order_id')
@click.argument('qty', type=click.FLOAT)
@click.argument('price', type=click.FLOAT)
def edit(order_id, qty, price):
    OrderController().edit(order_id, qty, price)

# ----------
# Order Status
# ----------
@cli.command()
@click.argument('order_id')
def status(order_id):
    OrderController().order_status(order_id)

@cli.command()
def executions():
    for x in Exchange().executions():
        print(x)

# __________ Bot ____________
# ----------
# All bots list
# ----------
@cli.command(help="Show bots list")
def bots():
    BotController().list_bots()

# ----------
# Single bot info
# ----------
@cli.command(help="Show Bot details")
@click.option( '-v', '--verbose', is_flag=True, default=False, help='Show further details')
@click.argument('id', type=click.STRING)
def bot(id:str, verbose:bool):
    BotController().bot_info(id, verbose)

# ----------
# Add new bot
# ----------
@cli.command(help="Add new bot")
@click.argument('type', type=click.STRING, default="bot")
def add(type):
    if type == "bot":
        BotController().add()
    else:
        print("Unknown bot type")

# ----------
# Edit bot
# ----------
@cli.command(help="Edit bot")
@click.argument('id', type=click.STRING)
def edit(id):
    BotController().edit(id)

# ----------
# Audit bot
# ----------
@cli.command()
@click.argument('id')
def audit(id):
    BotController().audit(id)

# ----------
# Start bot
# ----------
@cli.command()
@click.argument('id')
def start(id):
    BotController().start_bot(id)
    
# ----------
# Stop bot
# ----------
@cli.command()
@click.argument('id', type=click.STRING, default="")
def stop(id):
    if id == "":
        click.confirm('Stop all bots?', abort=True)
        BotController().stop_all_bots()
    else:
        BotController().stop_bot(id)

@cli.command()
def listen():
    print("Listening...")
    web_socket_api.listen()

if __name__ == '__main__':
    cli()
