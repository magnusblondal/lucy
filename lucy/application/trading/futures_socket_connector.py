from .futures_web_socket import FuturesSocketListener
from .logging_ws_socket import SocketLogger


logger = SocketLogger.get_logger("futures socket connector")
timeout = 10
websocket_trace = False  # set to True for connection verbose logging


def listen(settings, product_ids: list[str] = None):
    product_ids = product_ids or [
        # "PI_XBTUSD",
        "PF_XBTUSD"
    ]

    public_feeds_for_products = [
        # "ticker",
        # "ticker_lite",
        # "trade",
        # "book" # TODO
    ]

    public_feeds = [
        "heartbeat",
    ]

    private_feeds = [
        # "balances",
        # "account_balances_and_margins", # ?
        # "account_log",
        # "deposits_withdrawals",   # ?
        "fills",
        # "open_positions",
        # "open_orders",
        # "notifications_auth"
    ]

    cfWs = FuturesSocketListener(product_ids,
                                 public_feeds_for_products, public_feeds, private_feeds,
                                 base_url=settings.api_path_ws_futures,
                                 api_key=settings.api_key,
                                 api_secret=settings.api_secret,
                                 timeout=10,
                                 trace=websocket_trace)
    # exit()


if __name__ == "__main__":
    listen()
