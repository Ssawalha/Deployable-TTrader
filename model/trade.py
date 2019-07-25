import sqlite3
from time import time
from collections import OrderedDict
from model.orm import ORM
from model import util
from model import position
from model import account

class Trade(ORM):
    '''Python class which inherits from the class ORM. 
    \nTrade represents a single trade record, which contains:
    \npk - INTEGER | primary key (unique identifier for each user)
    \nbuy_sell - VARCHAR | indicates whether the transaction was for a buy or a sell
    \nusername - INTEGER | foreign key (unique identifier for each user)
    \nticker - VARCHAR | stock ticker
    \nshares - INTEGER | the number of shares
    \nprice - FLOAT | price of per stock
    \ntime - FLOAT | unix time
    '''

    tablename = 'trades'
    fields = ['buy_sell', 'username', 'ticker', 'price', 'shares', 'time']

    createsql = '''CREATE TABLE trades (pk INTEGER PRIMARY KEY AUTOINCREMENT,
                buy_sell VARCHAR,
                username VARCHAR,
                ticker VARCHAR(128),
                price FLOAT,
                shares INTEGER,
                time FLOAT,
                FOREIGN KEY(username) REFERENCES accounts(username)
                );''' #add NOT NULLs to ticker, shares, price, and time.

    def __init__(self, **kwargs):
        self.values = OrderedDict()
        self.values['pk'] = kwargs.get('pk')
        self.values['buy_sell'] = kwargs.get('buy_sell')
        self.values['username'] = kwargs.get('username') #get will return None if the key doesnt exist, will not throw error
        self.values['ticker'] = (kwargs.get('ticker')).lower()
        self.values['price'] = kwargs.get('price')
        self.values['shares'] = kwargs.get('shares')
        self.values['time'] = kwargs.get('time') #change default value of time to time.time, so kwargs.get('time', time.time()) #must import time first

    def __repr__(self):
        msg = '<Trade pk:{pk}, buy_sell = {buy_sell}, username:{username} ticker:{ticker}, price:{price}, shares:{shares}, time:{time}>'
        return msg.format(**self.values)

    def json(self):
        return {
            'pk':self.values['pk'],
            'buy_sell':self.values['buy_sell'],
            'username':self.values['username'],
            'ticker':self.values['ticker'],
            'price':self.values['price'],
            'shares':self.values['shares'],
            'time':self.values['time']
        }

    @classmethod
    def all_with_username(cls, username):
        '''return all Trades rows with username'''
        return cls.all_from_where_clause('WHERE username = ?', (username,))