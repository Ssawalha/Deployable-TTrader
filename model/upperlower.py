import requests

def ticker_high(ticker):
    API_KEY = "pk_2f1d9a6e68164e818677167d936ab8d8"
    ticker = ticker.lower()
    url = "https://cloud.iexapis.com/stable/stock/{}/quote?token="
    response = requests.get((url.format(ticker) + API_KEY))
    close_price = response.json()['close']
    day_high = response.json()['high']
    day_low = response.json()['low']
    open_price =  response.json()['open']
    return {"ticker":ticker, "open":open_price, "close":close_price, "high":day_high, "low":day_low}

print(ticker_high('aapl'))