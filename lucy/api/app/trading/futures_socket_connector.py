from  .futures_web_socket import FuturesSocketListener
from  .cfLogging import CfLogger
logger = CfLogger.get_logger(" Example ")


api_path = "wss://www.cryptofacilities.com/ws/v1"

api_key = "3EWPFVk88Cmol8hw8falnfA67Q5RAhnT8jysgfif9gnKmhf0KacIddHA"
api_secret = "D06lgIZD5y/9z6bZL17S7SioS0zwEEQGQH0T7+kVfto1CePZbvzR7UQUoKZzBT/uWEyVy/vmwislBLfCc9/a7Ip2"
timeout = 10
trace = False  # set to True for connection verbose logging

def subscribe(cfWs, product_ids: list[str], public_feeds_for_products: list[str], public_feeds: list[str], private_feeds: list[str]):
    ##### public feeds #####    
    for feed in public_feeds_for_products:
        cfWs.subscribe_public(feed, product_ids)
    for feed in public_feeds:
        cfWs.subscribe_public(feed)

    ##### private feeds #####
    for feed in private_feeds:
        cfWs.subscribe_private(feed)

def unsubscribe(cfWs, product_ids: list[str], public_feeds_for_products: list[str], public_feeds: list[str], private_feeds: list[str]):

    for feed in public_feeds_for_products:
        cfWs.unsubscribe_public(feed, product_ids)

    for feed in public_feeds:
        cfWs.unsubscribe_public(feed)

    for feed in private_feeds:
        cfWs.unsubscribe_private(feed)

def listen(product_ids: list[str] = None):

    product_ids = product_ids or [
        "PI_XBTUSD", 
        "PF_XBTUSD"
        ]
    
    public_feeds_for_products = [
        # "ticker", 
        # "ticker_lite", 
        # "trade", 
        # "book" # TODO
        ]
    
    public_feeds = [
        # "heartbeat",
        ]
    
    private_feeds = [
        # "balances", 
        # "account_balances_and_margins", # ?
        "account_log",
        # "deposits_withdrawals",   # ?
        # "fills",
        # "open_positions",
        # "open_orders",
        # "notifications_auth"
        ]

    cfWs = FuturesSocketListener(base_url=api_path, api_key=api_key, api_secret=api_secret, timeout=10, trace=trace)
    # Subscribe
    subscribe(cfWs, product_ids, public_feeds_for_products, public_feeds, private_feeds)
    
    logger.info("-----------------------------------------------------------")
    logger.info("****PRESS ANY KEY TO UNSUBSCRIBE AND EXIT APPLICATION****")
    logger.info("-----------------------------------------------------------")
    input()

    # Unsubscribe
    unsubscribe(cfWs, product_ids, public_feeds_for_products, public_feeds, private_feeds)

    # Exit
    exit()

if __name__ == "__main__":
    listen()