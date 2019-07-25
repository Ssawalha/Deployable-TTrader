def mainmenu():
    print("\nWelcome to TTrader!\n")
    print("1) Create Account")
    print("2) Log In")
    print("3) Quit")
    selection = int(input("\nYour choice: "))
    return selection

def create_account():
    print("\nAccount Creation\n")
    username = input("Choose a username: ")
    password = input("Choose a password: ")
    password_confirm = input("Please, confirm your password: ")
    while password != password_confirm:
        password = input("Choose a password: ")
        password_confirm = input("Please, confirm your password: ")
    if password == password_confirm:
        first_name = input("First name: ")
        last_name = input("Last name: ")
        return username, password, first_name, last_name

def create_acc_success(username):
        print("\nWelcome {}! Your account has been created, you have a balance of $10,000.".format(username))

def login_credentials():
    username = input("\nEnter your username: ")
    password = input("Enter your password: ")
    return username, password

def view_api_key(api_key):
    print(api_key)

def account_options(username):
    print("\nHello {}\n".format(username))
    print("1) Check balance")
    print("2) Check portfolio positions")
    print("3) Check trade history")
    print("4) Buy stocks")
    print("5) Sell stocks")
    print("6) View API Key")
    print("7) Sign out")
    login_selection = int(input("\nYour Choice: "))
    return login_selection

def show_balance(balance):
    print("\nYour balance is ${}".format(balance))

def show_portfolio(positions):
    if positions == []:
        print('You do not own any stocks, buy some stocks to start a portfolio.')
    else:
        print(positions)

def show_position(account):
    ticker = input("Enter desired stock's ticker: ")
    position = account.get_position_for(ticker)
    print(position)

def show_all_trades(trade_history):
    if trade_history == []:
        print('You have not exucted any transactions yet.')
    else:
        print(trade_history)

def choose_stock():
    ticker = input("\nSearch for ticker: ")
    return ticker

def invalid_ticker():
    print('Ticker not found.')

def num_of_shares(ticker, ticker_price):
    print('The price of 1 share of {} is ${}.'.format(ticker, ticker_price))
    amount = input('Enter # of shares to transact. ')
    return amount

def confirm(ticker, amount, total):
    confirmation = input('{} of {} shares total ${}.\nEnter Y or y to execute transaction. '.format(amount, ticker, total))
    return confirmation

def purchase_success():
    print('Your purchase was succussful.')

def sale_success():
    print('Your sale was successful.')

def insufficient_funds():
    print('!!! INSUFFICIENT FUNDS !!!')

def insufficient_shares():
    print('!!! INSUFFICIENT SHARES !!!')

