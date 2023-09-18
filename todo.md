BUGS:
SO er triggerað of hátt
WS Connection dettur út

logger skrifar hverja færslu nokkrum sinnum


HUX:
ef position er opin og ég breyti um strategy; hvað gerist þá?
  ? loka position
  ? nota nyju strategiu til að loka
  ? nota org strategy til að loka 

DEVOPS:
setja upp docker
setja upp docker compose
hosting
delivery pipeline
github actions ?
monitoring


TODOs:
Fill getur verið að koma inn áður en order er skrifuð í grunn => PnL calc er ekki heyrt á réttum tíma
Backtesting
geta lokað position manually, ef ég hef lokað á vefsíðunni 
  - tengja það við fill
Ef vantar fills, þá þarf að sækja
Runner sjái þegar verða breytingar á bot active state
skilgreina hvaða exchange bot fer á móti

-> hví þarf ég að rounda atom í heila tölu?
"symbol": "pf_atomusd",
            "type": "flexible_futures",
            "tickSize": 0.001,
            "contractSize": 1,
            "tradeable": true,
            "impactMidSize": 10.00,
            "maxPositionSize": 600000.00000000000,
            "openingDate": "2022-03-22T14:23:24.000Z",

take profit orders
logging

panic button
leverage



Muna:
setja max lines aftur í 5000 -> dtm_utils