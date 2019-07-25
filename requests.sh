echo 'get_ticker_price'
curl 127.0.0.1:5000/ttrader/api/get_ticker_price/tsla

echo 'get_api_key'
curl 127.0.0.1:5000/api/account_info/12345678912345678902

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
curl -X POST -H 'content-type: application/json' -d '{"username":"ttrader_api2", "password":"1234", "first_name":"sami", "last_name":""}' 127.0.0.1:5000/api/create_account