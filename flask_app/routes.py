#!/usr/bin/env python3

from flask import request, jsonify
from flask_app.app import app
from model.util import lookup_price
from model.util import hash_password
from model.account import Account

@app.route('/')
def home():
    return jsonify({'Welcome to':'TTrader api'})

@app.route('/api/create_account', methods=['POST'])
def create_account():
    if not request.json:
        return jsonify({'error':'bad request'}), 400
    if 'username' not in request.json or 'password' not in request.json or 'first' not in request.json or 'last' not in request.json:
        return jsonify({'error':'bad request'}), 400
    username = request.json['username']
    password = request.json['password']
    first = request.json['first_name']
    last = request.json['last_name']
    pword_hash = hash_password(password)
    new_account = Account(username=username, password_hash=pword_hash, balance=10000, first = first, last = last)
    new_account.save()
    new_account.generate_api_key
    return jsonify({"Your account was created successfully.":"You start with a balance of $10,000."})

@app.route('/api/get_ticker_price/<ticker>', methods=['GET'])
def get_ticker_price(ticker):
    ticker_price = lookup_price(ticker)
    return jsonify({'ticker price is ': ticker_price})

@app.route('/api/<api_key>', methods=['GET'])
def get_account_info(api_key):
    api_login_attempt = Account.api_authenticate(api_key)
    if api_login_attempt != None:
        return jsonify({"username": api_login_attempt.values['username'], "balance":api_login_attempt.values['balance'], "first_name": api_login_attempt.values['first'], "last_name": api_login_attempt.values['last']})
    else:
        return jsonify({"error":"404"})

@app.route('/api/<api_key>/balance', methods=['GET'])
def get_balance(api_key):
    api_login_attempt = Account.api_authenticate(api_key)
    if api_login_attempt != None:
        return jsonify(({'balance':api_login_attempt.values['balance']}))
    else:
        return jsonify({"error":"404"})

@app.route('/api/<api_key>/positions',methods=['GET'])
def get_positions(api_key):
    api_login_attempt = Account.api_authenticate(api_key)
    if api_login_attempt != None:
        positions = api_login_attempt.get_positions()
        return jsonify({"positions":[position.json() for position in positions]}) #should i remove pk from response?
    else:
        return jsonify({"error":"404"})

@app.route('/api/<api_key>/trades')
def get_trades(api_key):
    api_login_attempt = Account.api_authenticate(api_key)
    if api_login_attempt != None:
        trades = api_login_attempt.get_trades()
        return jsonify({"trades":[trade.json() for trade in trades]}) #should i remove pk from response?
    else:
        return jsonify({"error":"404"})

@app.route('/api/<api_key>/deposit', methods=['PUT'])
def put_deposit(api_key):
    api_login_attempt = Account.api_authenticate(api_key)   
    if not request.json:
        return jsonify({'error':'bad request'}), 400 
    if 'deposit' not in request.json:
    #if 'deposit' in request.json and type(request.json['deposit']) != bytes:
        return jsonify({'error':'bad request'}), 400 
    if api_login_attempt != None:
        current_bal = api_login_attempt.values['balance']
        new_bal = current_bal + float(request.json['deposit'])
        api_login_attempt.values['balance'] = new_bal
        api_login_attempt.save()
        return jsonify({'deposit successful, new balance is':api_login_attempt.values['balance']})

@app.route('/api/<api_key>/sell', methods=['POST'])
def sell_stock(api_key):
    api_login_attempt = Account.api_authenticate(api_key)   
    if not request.json:
        return jsonify({'error':'bad request'}), 400     
    if 'ticker' not in request.json or 'shares' not in request.json:
        return jsonify({'error':'bad request'}), 400
    ticker = request.json['ticker']
    shares = request.json['shares']
    
    api_login_attempt.sell(ticker, shares)

    new_position = api_login_attempt.get_position_for(ticker)
    return jsonify({"sale successful, new position is":new_position.json()})
 

@app.route('/api/<api_key>/buy', methods=['POST']) #buy and sell should return a json {"ticker":aapl, "shares":INTEGER}
def buy_stock(api_key):
    api_login_attempt = Account.api_authenticate(api_key)   
    if not request.json:
        return jsonify({'error':'bad request'}), 400     
    if 'ticker' not in request.json or 'shares' not in request.json:
        return jsonify({'error':'bad request'}), 400
    ticker = request.json['ticker']
    shares = request.json['shares']
    
    api_login_attempt.buy(ticker, shares)

    new_position = api_login_attempt.get_position_for(ticker)
    return jsonify({"purchase successful, new position is":new_position.json()})


#pep3333 --> wsgi | uwhiskey --> uses binary language (not py)
#using nginx instead of apache (open-source and free, apache is bad for scaling will crash after 10k users at the same time)

#swap reassign some requests from RAM to disk temporarily 

#ADD UNIT TESTS FOR ALL ROUTES

#CRON --> linux scheduler to check for updates and run codes at certain times 
#^ good to test that your flask app is running

#selenium will move the mouse and click on shit for you --> can do "headless" as well

#push to github prior to deploying