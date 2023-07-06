import json
import hashlib
import base64
import hmac
import websocket
import rel

from  .lucy_logging import LucyLogger

from .feeds.socket_router import SocketRouter

class FuturesSocketListener(object):
    '''Web Socket Client'''

    def __init__(self, product_ids, public_feeds_for_products, public_feeds, private_feeds, base_url, api_key="", api_secret="", timeout=5, trace=False):
        websocket.enableTrace(trace)
        self.logger = LucyLogger.get_logger("cf-ws-api")
        self.base_url = base_url
        self.api_key = api_key
        self.api_secret = api_secret
        self.timeout = timeout
        self.product_ids = product_ids
        self.public_feeds_for_products = public_feeds_for_products
        self.public_feeds = public_feeds
        self.private_feeds = private_feeds
        self.ws = None
        self.original_challenge = None
        self.signed_challenge = None
        self.challenge_ready = False
        self.router = SocketRouter()
        self.subscribed = False
        self._connect()

    def _message(self, feed: str, event: str, product_ids: list[str]=None) -> dict:
        request_message = {
            "event": event,
            "feed": feed
        }
        if product_ids is not None:
            request_message["product_ids"] = product_ids
        return request_message
    
    def _signed_message(self, feed: str, event: str) -> dict:
        return {"event": event,
                "feed": feed,
                "api_key": self.api_key,
                "original_challenge": self.original_challenge,
                "signed_challenge": self.signed_challenge}
        
    def _subscribe_public(self):
        for feed in self.public_feeds_for_products:
            self._subscribe_public(feed, self.product_ids)
        for feed in self.public_feeds:
            self._subscribe_public_feed(feed)
    
    def _subscribe_private(self):
        for feed in self.private_feeds:
            self._subscribe_private_feed(feed)
        self.subscribed = True

    def unsubscribe(self):
        for feed in self.public_feeds_for_products:
            self._unsubscribe_public(feed, self.product_ids)

        for feed in self.public_feeds:
            self._unsubscribe_public_feed(feed)

        for feed in self.private_feeds:
            self._unsubscribe_private(feed)

    def _subscribe_public_feed(self, feed: str, product_ids: list[str]=None):
        request_message = self._message(feed, "subscribe", product_ids)        
        self.logger.info("public subscribe to %s", feed)
        request_json = json.dumps(request_message)
        self.ws.send(request_json)

    def _unsubscribe_public_feed(self, feed, product_ids=None):
        """UnSubscribe to given feed and product ids"""
        request_message = self._message(feed, "unsubscribe", product_ids)
        self.logger.info("public unsubscribe to %s", feed)
        request_json = json.dumps(request_message)
        self.ws.send(request_json)

    # Private feeds
    def _subscribe_private_feed(self, feed):
        """Unsubscribe to feed"""

        if not self.challenge_ready:
            self._wait_for_challenge_auth()

        request_message = self._signed_message(feed, "subscribe")
        self.logger.info("private subscribe to %s", feed)
        request_json = json.dumps(request_message)
        self.ws.send(request_json)

    def _unsubscribe_private(self, feed):
        """Unsubscribe to feed"""

        if not self.challenge_ready:
            self._wait_for_challenge_auth()

        request_message = self._signed_message(feed, "unsubscribe")
        self.logger.info("private unsubscribe to %s", feed)
        request_json = json.dumps(request_message)
        self.ws.send(request_json)

    def _connect(self):        
        """Establish a web socket connection"""
        self.ws = websocket.WebSocketApp(self.base_url,
                                         on_message=self._on_message,
                                         on_close=self._on_close,
                                         on_open=self._on_open,
                                         on_error=self._on_error,
                                         )      
        
        self.ws.run_forever(dispatcher=rel, reconnect=3)
        rel.signal(2, self._close)  # Keyboard Interrupt
        rel.dispatch()
        

    def _close(self):
        """Close the web socket connection"""
        print("Closing...")
        self.unsubscribe()
        self.ws.close()
        print("Closed")
        rel.abort()


    def _on_message(self, ws, message):
        """Listen the web socket connection. Block until a message arrives. """

        # def run(*args):
        message_json = json.loads(message)
        self.logger.info(message_json)

        if message_json.get("event", "") == "challenge":
            self.original_challenge = message_json["message"]
            self.signed_challenge = self._sign_challenge(self.original_challenge)
            self.challenge_ready = True
            if not self.subscribed:
                self._subscribe_private()

        else:
            self.router.route(message_json)
        self.logger.info(f"Challenge: {self.challenge_ready}")
        # Thread(target=run, args=()).start()

    def _on_open(self, ws):
        self.logger.info("Connected to %s", self.base_url)
        self._request_challenge()
        self._subscribe_public()


    def _on_close(self, ws, close_status_code, close_msg):
        self.logger.info(f'Connection closed: {close_status_code} {close_msg}')

    def _on_error(self, ws: websocket.WebSocketApp, error: str):
        self.logger.warn(error)


    # def _wait_for_it(self):
    #     self.logger.info("waiting for challenge...")
    #     while not self.challenge_ready:
    #         timer = Timer(1000, self._wait_for_it)
    #         timer.start()

    def _wait_for_challenge_auth(self):
        self._request_challenge()

        self.logger.info("waiting for challenge...")
        # self._wait_for_it()
        # while not self.challenge_ready:
        #     sleep(1)

    def _request_challenge(self):
        """Request a challenge from Crypto Facilities Ltd"""
        self.logger.info("Requesting Challenge...")
        request_message = {
            "event": "challenge",
            "api_key": self.api_key
        }
        request_json = json.dumps(request_message)
        self.ws.send(request_json)

    def _sign_challenge(self, challenge):
        """Signed a challenge received from Crypto Facilities Ltd"""
        self.logger.info("Signing Challenge...")
        # step 1: hash the message with SHA256
        sha256_hash = hashlib.sha256()
        sha256_hash.update(challenge.encode("utf8"))
        hash_digest = sha256_hash.digest()

        # step 3: base64 decode apiPrivateKey
        secret_decoded = base64.b64decode(self.api_secret)

        # step 4: use result of step 3 to has the result of step 2 with HMAC-SHA512
        hmac_digest = hmac.new(secret_decoded, hash_digest, hashlib.sha512).digest()

        # step 5: base64 encode the result of step 4 and return
        sch = base64.b64encode(hmac_digest).decode("utf-8")
        return sch
