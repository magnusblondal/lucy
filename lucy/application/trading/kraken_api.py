import json
import urllib.request as urllib2


class KrakenApi(object):
    def __init__(self):
        self.uri = 'https://api.kraken.com/0/public/'

    def ohlc(self, pair: str, interval: int = 60, since: int = 0):
        url = f"{self.uri}OHLC?pair={pair}&interval={interval}"
        if since > 0:
            url += f"&since={since}"
        request = urllib2.Request(url)
        request.get_method = lambda: "GET"

        response = urllib2.urlopen(request)
        return json.loads(response.read().decode("utf-8"))

