from  .futures_web_socket import FuturesSocketListener
from  .logging_ws_socket import SocketLogger
logger = SocketLogger.get_logger("futures socket connector")

api_path = "wss://www.cryptofacilities.com/ws/v1"
api_key = "3EWPFVk88Cmol8hw8falnfA67Q5RAhnT8jysgfif9gnKmhf0KacIddHA"
api_secret = "D06lgIZD5y/9z6bZL17S7SioS0zwEEQGQH0T7+kVfto1CePZbvzR7UQUoKZzBT/uWEyVy/vmwislBLfCc9/a7Ip2"
timeout = 10

websocket_trace = False  # set to True for connection verbose logging

def listen(product_ids: list[str] = None):

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

    cfWs = FuturesSocketListener(product_ids, public_feeds_for_products, public_feeds, private_feeds, base_url=api_path, 
                                 api_key=api_key, api_secret=api_secret, timeout=10, trace=websocket_trace)
    # exit()

if __name__ == "__main__":
    listen()