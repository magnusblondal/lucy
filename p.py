from lucy.model.id import Id
from lucy.model.domain_model import DomainModel
from lucy.model.signal import Signal
from datetime import datetime
from lucy.application.events.event import DomainEvent
from lucy.application.trading.exchange import Exchange
from lucy.application.trading.instrument import Instrument

import websocket
from threading import Thread
import time

import rel

addr = "wss://api.gemini.com/v1/marketdata/%s"

# if __name__ == "__main__":
#     for symbol in ["BTCUSD", "ETHUSD", "ETHBTC"]:
#         ws = websocket.WebSocketApp(addr % (symbol,), on_message=lambda w, m: print(m))
#         ws.run_forever(dispatcher=rel)
#     rel.signal(2, rel.abort)  # Keyboard Interrupt
#     rel.dispatch()


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        for i in range(3):
            # send the message, then wait
            # so thread doesn't exit and socket
            # isn't closed
            ws.send("Hello %d" % i)
            time.sleep(1)

        time.sleep(1)
        ws.close()
        print("Thread terminating...")

    Thread(target=run).start()


if __name__ == "__main__":
    websocket.enableTrace(True)

    for symbol in ["BTCUSD", "ETHUSD", "ETHBTC"]:
        ws = websocket.WebSocketApp(addr % (symbol,), 
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
        ws.run_forever(dispatcher=rel)
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()


    # if len(sys.argv) < 2:
    #     host = "ws://echo.websocket.events/"
    # else:
    #     host = sys.argv[1]
    # ws = websocket.WebSocketApp(host,
    #                             on_message=on_message,
    #                             on_error=on_error,
    #                             on_close=on_close)
    # rel.signal(2, rel.abort)  # Keyboard Interrupt
    # rel.dispatch()
    # # ws.on_open = on_open
    # ws.run_forever()