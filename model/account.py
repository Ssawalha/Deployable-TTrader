import sqlite3
from time import time
from collections import OrderedDict
from model.orm import ORM
from model import util
from model import position as p
from model import trade as t    

from random import randint

class Account(ORM):

    tablename = "accounts"
    fields = ["username", "password_hash", "balance", "api_key", "first", "last"]

    createsql = '''CREATE TABLE {} (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR NOT NULL,
        password_hash TEXT,
        balance FLOAT,
        first VARCHAR,
        last VARCHAR,
        api_key VARCHAR(256),
        UNIQUE(username),
        UNIQUE(api_key),
        );'''.format(tablename)

    def __init__(self, **kwargs):
        self.values = OrderedDict()
        self.values['pk'] = kwargs.get('pk')
        self.values['username'] = kwargs.get('username')
        self.values['password_hash'] = kwargs.get('password_hash')
        self.values['balance'] = kwargs.get('balance')
        self.values['first'] = kwargs.get('first')
        self.values['last'] = kwargs.get('last')
        self.values['api_key'] = kwargs.get('api_key')

    def __repr__(self):
        msg = '<Account pk:{pk}, username:{username}, password_hash:{password_hash}, balance:{balance}, first:{first}, last:{last}, api_key:{api_key}>'
        return msg.format(**self.values)

    def json(self):
        return {
            'pk':self.values['pk'],
            'username':self.values['username'],
            'password_hash':self.values['password_hash'],
            'balance':self.values['balance'],
            'first':self.values['first'],
            'last':self.values['last'],
            'api_key':self.values['api_key']
        }

    @classmethod
    def api_authenticate(cls, api_key):
        return cls.one_from_where_clause("WHERE api_key = ?",(api_key,))

    def generate_api_key(self):
        rand_key = str(randint(1000000000000000000,99999999999999999999))
        self.values['api_key'] = rand_key
        self.save()

    def set_password(self, password):
        self.values['password_hash'] = util.hash_password(password)
    
    @classmethod
    def login(cls, username, password):
        """ login: is a class method of Account class,
             \nit checks the username and password_hash
             \nin ttrader.db accounts table
             \nand returns an instance of that account"""
        check_password_bool = util.check_password(username, password)
        if check_password_bool == True:
            return cls.one_from_where_clause("WHERE username = ?",(username,))

    def get_positions(self):
        return p.Position.all_with_username(self.values['username'])

    def get_position_for(self, ticker):
        """ return a Position object for the user. if the position does not 
        exist, return a new Position with zero shares."""
        ticker = ticker.lower()
        position = p.Position.one_from_where_clause(
            "WHERE ticker =? AND username =?", (ticker, self.values['username']))
        if position is None:
            return p.Position(username=self.values['username'], ticker=ticker, shares=0)
        return position

    def get_trades(self):
        """ return all of the user's trades ordered by time. returns a list of
        Trade objects """
        trades_lst = t.Trade.all_with_username(self.values['username'])
        return trades_lst

    def trades_for(self, ticker):
        """ return all of the user's trades for a given ticker. """
        ticker = ticker.lower()
        trades_lst = t.Trade.all_from_where_clause(
            "WHERE ticker =? AND username =?", (ticker, self.values['username']))
        return trades_lst
    
    def buy(self, ticker, amount):
        """ make a purchase! raise KeyError for a nonexistent stock and
        ValueError for insufficient funds. will create a new Trade and modify
        a Position and alters the user's balance. returns nothing """
        ticker = ticker.lower()
        amount = int(amount)
        try:
            ticker_price = util.lookup_price(ticker)
            if (ticker_price * amount) > self.values['balance']:
                raise ValueError
            else:
                self.values['balance'] = (self.values['balance'] - ticker_price * amount)
                self.save()
                
                transaction = t.Trade(buy_sell = 'Buy', username = self.values['username'], 
                 ticker = ticker, price = ticker_price, 
                 shares = amount, time = time())
                transaction.save()
                
                position = self.get_position_for(ticker) #
                position.values['shares'] = (position.values['shares'] + amount)
                position.save()
        except:
            raise KeyError

    def sell(self, ticker, amount):
        """ make a sale! raise KeyError for a non-existent Position and
        ValueError for insufficient shares. will create a new Trade object,
        modify a Position, and alter the self.balance. returns nothing."""
        ticker = ticker.lower()
        amount = int(amount)
        try:
            ticker_price = util.lookup_price(ticker)
            position = self.get_position_for(ticker)
            if position.values['shares'] < amount:
                raise ValueError
            else:
                position.values['shares'] -= amount
                position.save()

                transaction = t.Trade(buy_sell = 'Sell', username = self.values['username'],
                 ticker = ticker, price = ticker_price,
                 shares = amount, time = time())
                transaction.save()
                self.values['balance'] += (ticker_price * amount)
                self.update_row()
        except:
            raise KeyError

    def ticker_buy_lst(self, ticker):
        ticker_trades_lst = self.trades_for(ticker)
        buy_trades = []
        for trade in ticker_trades_lst:
            if trade.values['buy_sell'] == 'Buy':
                buy_trades.append(trade)
        return buy_trades

    def ticker_sell_lst(self, ticker):
        ticker_trades_lst = self.trades_for(ticker)
        sell_trades = []
        for trade in ticker_trades_lst:
            if trade.values['buy_sell'] == 'Sell':
                sell_trades.append(trade)
        return sell_trades

    def buy_market_value(self, ticker):
        buy_lst = self.ticker_buy_lst(ticker)
        market_value = 0
        for trade in buy_lst:
            market_value += (trade.values['shares'] * trade.values['price'])
        return market_value

    def buy_trade_volume(self, ticker):
        buy_lst = self.ticker_buy_lst(ticker)
        trade_volume = 0
        for trade in buy_lst: 
            trade_volume += trade.values['shares']
        return trade_volume
   
    def sell_market_value(self, ticker):
        sell_lst = self.ticker_sell_lst(ticker)
        market_value = 0
        for trade in sell_lst:
            market_value += (trade.values['shares'] * trade.values['price'])
        return market_value

    def sell_trade_volume(self, ticker):
        sell_lst = self.ticker_sell_lst(ticker)
        trade_volume = 0
        for trade in sell_lst: 
            trade_volume += trade.values['shares']
        return trade_volume

    def profit_loss(self, ticker):
        buy_mkt_value = self.buy_market_value(ticker)
        sell_mkt_value = self.sell_market_value(ticker)
        net_mkt_value = sell_mkt_value - buy_mkt_value

        buy_mkt_volume = self.buy_trade_volume(ticker)
        sell_mkt_volume = self.sell_trade_volume(ticker)
        net_mkt_volume = buy_mkt_volume - sell_mkt_volume

        if net_mkt_volume > 0:
            return (net_mkt_volume * util.lookup_price(ticker)) + net_mkt_value
        else:
            return net_mkt_value