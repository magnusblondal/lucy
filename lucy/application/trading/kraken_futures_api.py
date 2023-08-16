
import time
import base64
import hashlib
import hmac
import json
from typing import List
import urllib.request as urllib2
import urllib.parse as urllib
import ssl

from .flex import Account, Flex

class FuturesApi(object):
    def __init__(self, apiPath, apiPublicKey="", apiPrivateKey="", timeout=10, checkCertificate=True, useNonce=False):
        self.apiPath = apiPath
        self.apiPublicKey = apiPublicKey
        self.apiPrivateKey = apiPrivateKey
        self.timeout = timeout
        self.nonce = 0
        self.checkCertificate = checkCertificate
        self.useNonce = useNonce

    ##### public endpoints #####

    # returns all instruments with specifications
    def get_instruments(self):
        endpoint = "/derivatives/api/v3/instruments"
        return self.make_request("GET", endpoint)

    # returns market data for all instruments
    def get_tickers(self):
        endpoint = "/derivatives/api/v3/tickers"
        return self.make_request("GET", endpoint)

    # returns the entire order book of a futures
    def get_orderbook(self, symbol):
        endpoint = "/derivatives/api/v3/orderbook"
        postUrl = "symbol=%s" % symbol
        return self.make_request("GET", endpoint, postUrl=postUrl)

    # returns historical data for futures and indices
    def get_history(self, symbol, lastTime=""):
        endpoint = "/derivatives/api/v3/history"
        if lastTime != "":
            postUrl = "symbol=%s&lastTime=%s" % (symbol, lastTime)
        else:
            postUrl = "symbol=%s" % symbol
        return self.make_request("GET", endpoint, postUrl=postUrl)

    ##### private endpoints #####

    # returns key account information
    # Deprecated because it returns info about the Futures margin account
    # Use get_accounts instead
    # def get_account(self):
    #     endpoint = "/derivatives/api/v3/account"
    #     return self.make_request("GET", endpoint)

    def get_accounts(self) -> List[Account]:
        """
        Key account information
        """
        endpoint = "/derivatives/api/v3/accounts"
        accounts = self.make_request("GET", endpoint)
        res = json.loads(accounts)
        accs = res['accounts']
        flex = accs['flex']
        return [Flex(flex)]

    # places an order
    def send_order(self, orderType, symbol, side, size, limitPrice, stopPrice=None, clientOrderId=None, reduce_only: bool=False):
        endpoint = "/derivatives/api/v3/sendorder"
        postBody = "orderType=%s&symbol=%s&side=%s&size=%s&limitPrice=%s" % (
            orderType, symbol, side, size, limitPrice)

        if orderType == "stp" and stopPrice is not None:
            postBody += "&stopPrice=%s" % stopPrice

        if clientOrderId is not None:
            postBody += "&cliOrdId=%s" % clientOrderId
        
        if reduce_only:
            postBody += "&reduceOnly=%s" % reduce_only

        return self.make_request("POST", endpoint, postBody=postBody)
        

    # places an order
    def send_order_1(self, order):
        endpoint = "/derivatives/api/v3/sendorder"
        postBody = urllib.urlencode(order)
        return self.make_request("POST", endpoint, postBody=postBody)

    def edit_order(self, edit):
        """
        Edit an order
        """
        endpoint = "/derivatives/api/v3/editorder"
        return self.make_request("POST", endpoint, postBody=edit)

    def cancel_order(self, order_id=None):
        """
        Cancels order, based on order id (from Kraken)
        """
        endpoint = "/derivatives/api/v3/cancelorder"
        postBody = "order_id=%s" % order_id
        return self.make_request("POST", endpoint, postBody=postBody)

    
    def cancel_order_by_client_id(self, cli_ord_id=None):
        """
        Cancels order, based on provided (client) order id
        """
        endpoint = "/derivatives/api/v3/cancelorder"
        postBody = "cliOrdId=%s" % cli_ord_id
        return self.make_request("POST", endpoint, postBody=postBody)

    def cancel_all_orders(self):
        """
        Cancel all orders
        """
        endpoint = "/derivatives/api/v3/cancelallorders"
        postbody = ""

        return self.make_request("POST", endpoint, postBody=postbody)

    def cancel_all_orders_for_symbol(self, symbol=None):
        """
        Cancel all orders for a given symbol
        """
        endpoint = "/derivatives/api/v3/cancelallorders"
        postbody = "symbol=%s" % symbol
        return self.make_request("POST", endpoint, postBody=postbody)

    # cancel all orders after
    def cancel_all_orders_after(self, timeoutInSeconds=60):
        endpoint = "/derivatives/api/v3/cancelallordersafter"
        postbody = "timeout=%s" % timeoutInSeconds

        return self.make_request("POST", endpoint, postBody=postbody)

    # places or cancels orders in batch
    def send_batchorder(self, jsonElement):
        endpoint = "/derivatives/api/v3/batchorder"
        postBody = "json=%s" % jsonElement
        return self.make_request("POST", endpoint, postBody=postBody)

    def get_openorders(self):
        """
        All open orders
        """
        endpoint = "/derivatives/api/v3/openorders"
        return self.make_request("GET", endpoint)
    
    def get_order_status(self, order_ids):
        endpoint = "/derivatives/api/v3/orders/status"
        postBody = f"orderIds=%s" % order_ids
        # print(postBody)
        return self.make_request("POST", endpoint,  postBody=postBody)

    def get_fills(self, lastFillTime=""):
        """
        Filled orders
        """
        endpoint = "/derivatives/api/v3/fills"
        if lastFillTime != "":
            postUrl = "lastFillTime=%s" % lastFillTime
        else:
            postUrl = ""
        return self.make_request("GET", endpoint, postUrl=postUrl)

    def get_openpositions(self):
        """
        All open positions
        """
        endpoint = "/derivatives/api/v3/openpositions"
        return self.make_request("GET", endpoint)

    # sends an xbt withdrawal request
    def send_withdrawal(self, targetAddress, currency, amount):
        endpoint = "/derivatives/api/v3/withdrawal"
        postBody = "targetAddress=%s&currency=%s&amount=%s" % (
            targetAddress, currency, amount)
        return self.make_request("POST", endpoint, postBody=postBody)

    # returns xbt transfers
    def get_transfers(self, lastTransferTime=""):
        endpoint = "/derivatives/api/v3/transfers"
        if lastTransferTime != "":
            postUrl = "lastTransferTime=%s" % lastTransferTime
        else:
            postUrl = ""
        return self.make_request("GET", endpoint, postUrl=postUrl)

    # returns all notifications
    def get_notifications(self):
        endpoint = "/derivatives/api/v3/notifications"
        return self.make_request("GET", endpoint)

    # makes an internal transfer
    def transfer(self, fromAccount, toAccount, unit, amount):
        endpoint = "/derivatives/api/v3/transfer"
        postBody = "fromAccount=%s&toAccount=%s&unit=%s&amount=%s" % (
            fromAccount, toAccount, unit, amount)
        return self.make_request("POST", endpoint, postBody=postBody)

    # accountlog csv
    def get_accountlog(self):
        endpoint = "/api/history/v2/accountlogcsv"
        return self.make_request("GET", endpoint)

    def _get_partial_historical_elements(self, elementType, **params):
        endpoint = "/api/history/v2/%s" % elementType

        params = {k: v for k, v in params.items() if v is not None}
        postUrl = urllib.urlencode(params)

        return self.make_request_raw("GET", endpoint, postUrl)

    def _get_historical_elements(self, elementType, since=None, before=None, sort=None, limit=1000):
        elements = []

        continuationToken = None

        while True:
            res = self._get_partial_historical_elements(elementType, since = since, before = before, sort = sort, continuationToken = continuationToken)
            body = json.loads(res.read().decode('utf-8'))
            elements = elements + body['elements']

            if res.headers['is-truncated'] is None or res.headers['is-truncated'] == "false":
                continuationToken = None
                break
            else:
                continuationToken = res.headers['next-continuation-token']

            if len(elements) >= limit:
                elements = elements[:limit]
                break
        return elements

    def get_orders(self, since=None, before=None, sort=None, limit=1000):
        """
        Retrieves orders of your account. With default parameters it gets the 1000 newest orders.
        :param since: Timestamp in milliseconds. Retrieves orders starting at this time rather than the newest/latest.
        :param before: Timestamp in milliseconds. Retrieves orders before this time.
        :param sort: String "asc" or "desc". The sorting of orders.
        :param limit: Amount of orders to be retrieved.
        :return: List of orders
        """
        return self._get_historical_elements('orders', since, before, sort, limit)

    def get_executions(self, since=None, before=None, sort=None, limit=1000):
        """
        Retrieves executions of your account. With default parameters it gets the 1000 newest executions.
        :param since: Timestamp in milliseconds. Retrieves executions starting at this time rather than the newest/latest.
        :param before: Timestamp in milliseconds. Retrieves executions before this time.
        :param sort: String "asc" or "desc". The sorting of executions.
        :param limit: Amount of executions to be retrieved.
        :return: List of executions
        """
        return self._get_historical_elements('executions', since, before, sort, limit)

    def get_market_price(self, symbol, since=None, before=None, sort=None, limit=1000):
        """
        Retrieves prices of given symbol. With default parameters it gets the 1000 newest prices.
        :param symbol: Name of a symbol. For example "PI_XBTUSD".
        :param since: Timestamp in milliseconds. Retrieves prices starting at this time rather than the newest/latest.
        :param before: Timestamp in milliseconds. Retrieves prices before this time.
        :param sort: String "asc" or "desc". The sorting of prices.
        :param limit: Amount of prices to be retrieved.
        :return: List of prices
        """
        return self._get_historical_elements('market/' + symbol + '/price', since, before, sort, limit)

    def get_market_orders(self, symbol, since=None, before=None, sort=None, limit=1000):
        """
        Retrieves orders of given symbol. With default parameters it gets the 1000 newest orders.
        :param symbol: Name of a symbol. For example "PI_XBTUSD".
        :param since: Timestamp in milliseconds. Retrieves orders starting at this time rather than the newest/latest.
        :param before: Timestamp in milliseconds. Retrieves orders before this time.
        :param sort: String "asc" or "desc". The sorting of orders.
        :param limit: Amount of orders to be retrieved.
        :return: List of orders
        """
        return self._get_historical_elements('market/' + symbol + '/orders', since, before, sort, limit)

    def get_market_executions(self, symbol, since=None, before=None, sort=None, limit=1000):
        """
        Retrieves executions of given symbol. With default parameters it gets the 1000 newest executions.
        :param symbol: Name of a symbol. For example "PI_XBTUSD".
        :param since: Timestamp in milliseconds. Retrieves executions starting at this time rather than the newest/latest.
        :param before: Timestamp in milliseconds. Retrieves executions before this time.
        :param sort: String "asc" or "desc". The sorting of executions.
        :param limit: Amount of executions to be retrieved.
        :return: List of executions
        """
        return self._get_historical_elements('market/' + symbol + '/executions', since, before, sort, limit)
    
    def ohlc(self, pair:str, resolution:str = '1h', tick_type: str = 'trade', from_time:int = 0):
        '''
        resolution: "1m", "5m", "15m", "30m", "1h", "4h", "12h", "1d", "1w"
        tick_type:  "spot", "mark", "trade"
        from_time:  epoch timestamp
        '''
        if from_time != "":
            postUrl = "from=%s" % from_time
        else:
            postUrl = ""    
        endpoint = f'api/charts/v1/{tick_type}/{pair}/{resolution}'   
        res = self.make_request("GET", endpoint, postUrl=postUrl)
        return json.loads(res)
    
    # signs a message
    def sign_message(self, endpoint, postData, nonce=""):

        if endpoint.startswith('/derivatives'):
            endpoint = endpoint[len('/derivatives'):]

        # step 1: concatenate postData, nonce + endpoint
        message = postData + nonce + endpoint

        # step 2: hash the result of step 1 with SHA256
        sha256_hash = hashlib.sha256()
        sha256_hash.update(message.encode('utf8'))
        hash_digest = sha256_hash.digest()

        # step 3: base64 decode apiPrivateKey
        secretDecoded = base64.b64decode(self.apiPrivateKey)

        # step 4: use result of step 3 to has the result of step 2 with HMAC-SHA512
        hmac_digest = hmac.new(secretDecoded, hash_digest,
                               hashlib.sha512).digest()

        # step 5: base64 encode the result of step 4 and return
        return base64.b64encode(hmac_digest)

    # creates a unique nonce
    def get_nonce(self):
        # https://en.wikipedia.org/wiki/Modulo_operation
        self.nonce = (self.nonce + 1) & 8191
        return str(int(time.time() * 1000)) + str(self.nonce).zfill(4)

    # sends an HTTP request
    def make_request_raw(self, requestType, endpoint, postUrl="", postBody=""):
        # create authentication headers
        postData = postUrl + postBody

        if self.useNonce:
            nonce = self.get_nonce()
            signature = self.sign_message(endpoint, postData, nonce=nonce)
            authentHeaders = {"APIKey": self.apiPublicKey,
                              "Nonce": nonce, "Authent": signature}
        else:
            signature = self.sign_message(endpoint, postData)
            authentHeaders = {
                "APIKey": self.apiPublicKey, "Authent": signature}

        authentHeaders["User-Agent"] = "cf-api-python/1.0"

        # create request
        if postUrl != "":
            url = self.apiPath + endpoint + "?" + postUrl
        else:
            url = self.apiPath + endpoint

        # print(url)

        request = urllib2.Request(url, str.encode(postBody), authentHeaders)
        request.get_method = lambda: requestType

        # read response
        if self.checkCertificate:
            response = urllib2.urlopen(request, timeout=self.timeout)
        else:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            response = urllib2.urlopen(
                request, context=ctx, timeout=self.timeout)

        # return
        return response

    # sends an HTTP request and read response body
    def make_request(self, requestType, endpoint, postUrl="", postBody=""):
        return self.make_request_raw(requestType, endpoint, postUrl, postBody).read().decode("utf-8")
