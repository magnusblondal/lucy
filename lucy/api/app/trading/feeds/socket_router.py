import json

from .ticker_lite import TickerLite
from .open_positions import OpenPositions
from .heartbeat import Heartbeat
from .ticker import Ticker
from .trade import Trade, Trades
from .open_orders import OpenOrders, OpenOrder
from .fills import Fills, Fill
from .balances import Balances
from .notifications_auth import NotificationsAuth
from .account_log import AccountLog, AccountLogs

from api.app.infrastructure.repos.fills_repository import FillsRepository

class SocketRouter:
    openOrders: OpenOrders
    fills: Fills
    balance: Balances
    trades: Trades
    notificationsAuth: NotificationsAuth
    accountLogs: AccountLogs

    def __init__(self):
        self.feeds = {
                'ticker_lite': self.ticker_lite, 
                'ticker': self.ticker,
                'open_positions': self.open_positions,
                'heartbeat': self.heartbeat,
                'open_orders_snapshot': self.open_orders_snapshot, 'open_orders': self.open_orders,
                'fills_snapshot': self.fills_snapshot, 'fills': self.fills_update,
                'balances': self.balances, 
                'balances_snapshot': self.balances_snapshot,
                'trade_snapshot': self.trade_snapshot, 'trade': self.trade,
                'notifications_auth': self.notifications_auth,
                'account_log_snapshot': self.account_log_snapshot, 'account_log': self.account_log
                }
        self.notificationsAuth = NotificationsAuth([])
        
    # ------------------------------
    # Open Orders
    # ------------------------------
    def open_orders_snapshot(self, message_json, event=""):
        print('>>>>>>> Open Orders Snapshot------------------------------')
        self.openOrders = OpenOrders.from_feed(message_json)
        print(self.openOrders)

    def open_orders(self, message_json, event=""):        
        print('>>>>>>> Open Orders ------------------------------')
        if event == 'subscribed':
            print('Open Orders Subscribed Successfully')
        else:
            self.openOrders.update(OpenOrder.from_feed(message_json))
            print(self.openOrders)

    # ------------------------------
    # Fills
    # ------------------------------
    def fills_snapshot(self, message_json, event=""):
        print('>>>>>>> Fills Snapshot------------------------------')
        self.fills = Fills.from_feed(message_json)
        [print(f) for f in self.fills.tail(5)]

    def fills_update(self, message_json, event=""):
        print('>>>>>>> Fills ------------------------------')
        if event == 'subscribed':
            print('Fills Subscribed Successfully')
        else:
            print('Fills Update ------------------------------')
            fills = self.fills.update(message_json)
            if fills is not None and len(fills) > 0:
                for f in fills:
                    FillsRepository().add(f)
                [print(f) for f in fills]
            else:
                print('No Fills !!!')

    # ------------------------------
    # Balances
    # ------------------------------
    def balances_snapshot(self, message_json, event=""):
        print('>>>>>>> Balances Snapshot------------------------------')
        self.balance = Balances.from_feed(message_json)
        print(self.balance)

    def balances(self, message_json, event=""):
        print('>>>>>>> Balances ------------------------------')
        if event == 'subscribed':
            print('Balances Subscribed Successfully')
        else:
            print('Balances Update')
            self.balance.update(message_json)
            print(self.balance)

    # ------------------------------
    # Ticker Lite
    # ------------------------------
    def ticker_lite(self, message_json, event=""):
        if event == 'subscribed':
            print('Ticker Lite Subscribed Successfully')
        else:
            print('>>>>>>> Ticker Lite ------------------------------')
            print(TickerLite.from_feed(message_json))
        
    # ------------------------------
    # Open Positions
    # ------------------------------
    def open_positions(self, message_json, event=""):
        if event == 'subscribed':
            print('Open Positions Subscribed Successfully')
        else:
            print('>>>>>>> Open Positions ------------------------------')
            x = OpenPositions.from_feed(message_json)
            print(x)

    # ------------------------------
    # Heartbeat
    # ------------------------------
    def heartbeat(self, message_json, event=""):
        if event == 'subscribed':
            print('Heartbeat Subscribed Successfully')
        else:
            print('>>>>>>> Heartbeat ------------------------------')
            x = Heartbeat.from_feed(message_json)
            print(x)

    # ------------------------------
    # NotificationsAuth
    # ------------------------------
    def notifications_auth(self, message_json, event=""):
        if event == 'subscribed':
            print('NotificationsAuth Subscribed Successfully')
        else:
            print('>>>>>>> NotificationsAuth ------------------------------')
            self.notificationsAuth.add(message_json['notifications'])
            print(self.notificationsAuth)

    # ------------------------------
    # Account Logs
    # ------------------------------    
    def account_log_snapshot(self, message_json, event=""):
        print('>>>>>>> Account Logs Snapshot------------------------------')
        self.accountLogs = AccountLogs.from_feed(message_json)
        print(self.accountLogs)

    def account_log(self, message_json, event=""):
        if event == 'subscribed':
            print('Account Logs Subscribed Successfully')
        else:
            print('>>>>>>> Account Logs ------------------------------')
            self.accountLogs.add(AccountLog.from_feed(message_json['new_entry']))
            last = self.accountLogs.last()
            print(f"{self.accountLogs} last: {last.id} '{last.info}'")

    # ------------------------------
    # Ticker
    # ------------------------------    
    def ticker(self, message_json, event=""):
        if event == 'subscribed':
            print('Ticker Subscribed Successfully')
        else:
            print('>>>>>>> Ticker ------------------------------')
            x = Ticker.from_feed(message_json)
            print(x)
    
    # ------------------------------
    # Trade
    # ------------------------------
    def trade_snapshot(self, message_json, event=""):
        print('>>>>>>> Trade Snapshot------------------------------')
        self.trades = Trades.from_feed(message_json)
        print(self.trades)

    def trade(self, message_json, event=""):
        if event == 'subscribed':
            print('Trade Subscribed Successfully')
        else:
            print('>>>>>>> Trade ------------------------------')
            x = Trade.from_feed(message_json)
            self.trades.add(x)
            print(self.trades)
            print(x)

    # ------------------------------
    # Route
    # ------------------------------
    def route(self, message_json):
        try:
            feed = message_json.get("feed", "")
            event = message_json.get("event", "")
            if feed in self.feeds:
                self.feeds[feed](message_json, event)
            elif event != 'challenge' and event != 'info':
                print('>>>>>>> Unknown Feed ------------------------------')
                print(message_json)
                print('-------------------------------------')
        except Exception as e:
            print('>>>>>>> Error ------------------------------')
            print(e)
            print(e.with_traceback())
            print('-------------------------------------')
