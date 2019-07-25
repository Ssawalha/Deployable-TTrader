import sqlite3
import os

DIR = os.path.dirname(__file__)
DBFILENAME = "ttrader.db"
DBPATH = os.path.join(DIR, DBFILENAME)

########TODO Figure out what size to assign varchar etc..
def schema(dbpath=DBPATH):
    with sqlite3.connect(dbpath) as conn:
        cur = conn.cursor()
        DROPSQL = "DROP TABLE IF EXISTS {tablename};"

        cur.execute(DROPSQL.format(tablename="accounts"))

        SQL = '''CREATE TABLE accounts (
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR NOT NULL,
            password_hash TEXT,
            balance FLOAT,
            first VARCHAR,
            last VARCHAR,
            api_key VARCHAR(256),
            UNIQUE(username),
            UNIQUE(api_key)
            );'''

        cur.execute(SQL)

        cur.execute(DROPSQL.format(tablename="positions"))

        SQL = '''CREATE TABLE positions(
                pk INTEGER PRIMARY KEY AUTOINCREMENT, 
                username VARCHAR, 
                ticker VARCHAR, 
                shares INTEGER,
                FOREIGN KEY (username) REFERENCES accounts(username)
                );'''

        cur.execute(SQL)

        cur.execute(DROPSQL.format(tablename="trades"))

        SQL = '''CREATE TABLE trades(
                pk INTEGER PRIMARY KEY AUTOINCREMENT,
                buy_sell VARCHAR,
                username VARCHAR,
                ticker VARCHAR(128),
                price FLOAT,
                shares INTEGER,
                time FLOAT,
                FOREIGN KEY(username) REFERENCES accounts(username)
                );'''

        cur.execute(SQL)
