echo 'get_ticker_price'
curl 127.0.0.1:5000/api/get_ticker_price/aapl

echo 'get_api_key'
curl 127.0.0.1:5000/api/12345678912345678902

echo 'get_balance'
curl 127.0.0.1:5000/api/12345678912345678902/balance

echo 'get_positions'
curl 127.0.0.1:5000/api/12345678912345678902/positions

echo 'get_trades'
curl 127.0.0.1:5000/api/12345678912345678902/trades

echo 'put_deposit $100'
curl -X PUT -H 'content-type: application/json' -d '{"deposit":100}' 127.0.0.1:5000/api/12345678912345678902/deposit

echo 'sell_stock {"tsla":1}'
curl -X POST -H 'content-type: application/json' -d '{"ticker":"tsla","shares":1}' 127.0.0.1:5000/api/12345678912345678902/sell

echo 'buy_stock {"tsla":1}'
curl -X POST -H 'content-type: application/json' -d '{"ticker":"tsla","shares":3}' 127.0.0.1:5000/api/12345678912345678902/buy

echo 'create_account'
curl -X POST -H 'content-type: application/json' -d '{"username":"h", "password":"1234", "first_name":"h", "last_name":"h"}' 127.0.0.1:5000/api/create_account

echo 'api_key'
curl -X POST -H 'content-type: application/json' -d '{"username":"sami", "password":"1234"}' 127.0.0.1:5000/api/get_api_key