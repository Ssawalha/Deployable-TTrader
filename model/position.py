import sqlite3
from collections import OrderedDict
from model.orm import ORM
from model import util
from model import account
from model import trade

class Position(ORM):
    '''Python class which inherits from the class ORM. 
    \nPositions represents a single trade record, which contains: 
    \nusername - VARCHAR | foreign key
    \nticker - VARCHAR | stock ticker
    \nshares - INTEGER | the number of shares
    '''

    tablename = "positions"
    fields = ['username','ticker', 'shares']

    createsql = '''CREATE TABLE {} (
                pk INTEGER PRIMARY KEY AUTOINCREMENT, 
                username VARCHAR, 
                ticker VARCHAR, 
                shares INTEGER,
                FOREIGN KEY (username) REFERENCES accounts(username)
                );'''.format(tablename)

    def __init__(self, **kwargs):
        self.values = OrderedDict()
        self.values['pk'] = kwargs.get('pk')
        self.values['username'] = kwargs.get('username')
        self.values['ticker'] = (kwargs.get('ticker')).lower()
        self.values['shares'] = int(kwargs.get('shares'))

    def __repr__(self):
        msg = '<Positions pk:{pk}, username:{username}, ticker:{ticker}, shares:{shares}>'
        return msg.format(**self.values)

    def json(self):
        return {
            'pk':self.values['pk'],
            'username':self.values['username'],
            'ticker':self.values['ticker'],
            'shares':self.values['shares']
        }

    @classmethod
    def all_with_username(cls, username):
        '''return all Position rows with account_pk (username is foreign key in this db)'''
        return cls.all_from_where_clause('WHERE username = ?', (username,))

    