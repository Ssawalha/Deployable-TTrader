import os
from time import time
from model.orm import ORM
from model.account import Account
from model.trade import Trade
from model.position import Position

DIR = os.path.dirname(__file__)
DBFILENAME = 'ttrader.db'
DBPATH = os.path.join(DIR, DBFILENAME)

def seed(dbpath=DBPATH):
    ORM.dbpath = dbpath
    
    default = Account(username='sami', balance=10000.00, first = 'sami', last = 's', api_key = "12345678912345678902")
    default.set_password('1234')
    default.save()

    default_buy = Trade(buy_sell = 'Buy', username = 'sami', ticker = 'tsla', price = '100', shares = '10', time = time())
    default_buy.save()

    default_sale = Trade(buy_sell = 'Sell', username = 'sami', ticker = 'tsla', price ='110', shares = '5', time = time())
    default_sale.save()

    default_position = Position(username = 'sami', ticker = 'tsla', shares = '5')
    default_position.save()
    
    # default.buy('tsla',6)
    # default.sell('tsla',1)
