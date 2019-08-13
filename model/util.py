import bcrypt
import requests
from model import account as a

import os

TokenPATH = os.path.dirname(__file__)
TokenData = "tokenfile.txt"
TokenDPath = os.path.join(TokenPATH,TokenData) 

FAKE_PRICES = {"symbol":"AAPL","companyName":"Apple, Inc.","calculationPrice":"close","open":201.85,"openTime":1562765400280,"close":203.23,"closeTime":1562788800542,"high":203.73,"low":201.56,"latestPrice":203.23,"latestSource":"Close","latestTime":"July 10, 2019","latestUpdate":1562788800542,"latestVolume":17876375,"iexRealtimePrice":203.18,"iexRealtimeSize":100,"iexLastUpdated":1562788799615,"delayedPrice":203.23,"delayedPriceTime":1562788800542,"extendedPrice":203.25,"extendedChange":0.02,"extendedChangePercent":0.0001,"extendedPriceTime":1562791802875,"previousClose":201.24,"change":1.99,"changePercent":0.00989,"iexMarketPercent":0.032331554915356164,"iexVolume":577971,"avgTotalVolume":24623542,"iexBidPrice":0,"iexBidSize":0,"iexAskPrice":0,"iexAskSize":0,"marketCap":935077488400,"peRatio":16.95,"week52High":233.47,"week52Low":142,"ytdChange":0.284206,"lastTradeTime":1562788800542}
API_KEY = ""
#you can use bcrypt --> advantages -> auto salts, allows you to save salt & hashed_pw in same column in db

def hash_password(password): #add saltedpw to db (same column), lookup salt in db to crack pword
    password = password.encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)

def check_password(username, password):
    user = a.Account()
    user_info = user.one_from_where_clause('WHERE username = ?', (username,))
    if user_info != None:
        hashed_pw = (user_info.values['password_hash'])
        password = password.encode()
        return bcrypt.checkpw(password, hashed_pw)
    else:
        return None #returns True or False

def lookup_price(ticker):
    global API_KEY
    ticker = ticker.lower()
    stem = "https://cloud.iexapis.com/stable/stock/{}/quote?token="
    response = requests.get((stem.format(ticker) + API_KEY))
    price = response.json()["latestPrice"]
    return price

def ticker_high(ticker):
    global API_KEY
    ticker = ticker.lower()
    url = "https://cloud.iexapis.com/stable/stock/{}/quote?token="
    response = requests.get((url.format(ticker) + API_KEY))
    price = response.json()
    return price
        # CHECK THE RESPONSE STATUS CODE IF 200 ITS GOOD, ANYTHING ELSE SHOULD ALERT US

def get_token():
    with open(TokenDPath, "r") as f:
        token = f.read()
    return token

API_KEY = get_token()