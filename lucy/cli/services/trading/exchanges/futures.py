import ccxt

path = "https://futures.kraken.com/"
public = "3EWPFVk88Cmol8hw8falnfA67Q5RAhnT8jysgfif9gnKmhf0KacIddHA"
private = "D06lgIZD5y/9z6bZL17S7SioS0zwEEQGQH0T7+kVfto1CePZbvzR7UQUoKZzBT/uWEyVy/vmwislBLfCc9/a7Ip2"

exchange = ccxt.kraken({
    'apiKey': public,
    'secret': private,
    'enableRateLimit': True, # required https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
    'options': {
        'defaultType': 'future',
        },
    })

kraken = ccxt.kraken({
    'apiKey': public,
    'secret': private,
})

# print(exchange.load_markets())

def monkey(pair):
    kraken.fetchMyTrades(pair)
