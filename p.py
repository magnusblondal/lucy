from lucy.api.app.models.id import Id
from lucy.api.app.models.domain_model import DomainModel
from lucy.api.app.models.signal import Signal
from datetime import datetime
from lucy.api.app.events.event import DomainEvent
from lucy.api.app.trading.exchange import Exchange
from lucy.api.app.trading.instrument import Instrument

inst = Exchange().instruments()

symb = "pf_xbtusd"
# "rr_xbtusd"
#"pi_xbtusd"
#   "pf_ethusd"
# print(inst[symb])

# for i in inst:
#     print(i.symbol)

pre = [i.symbol[:2] for i in inst]
# for p in pre:
#     print(p)


# fs = [i for i in inst if i.symbol == symb]

# for f in fs:
#     print(f)

# def cont(symb:str) -> str:
#     if symb.rfind('_') > 2:
#         symb = symb[:symb.rfind('_')]
#     return symb[3:-3] 

# symbs = [i.symbol for i in inst]
# for s in symbs:
#     print(s)
#     print(cont(s))