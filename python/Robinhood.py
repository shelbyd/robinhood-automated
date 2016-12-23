import json
import requests
import urllib

class Robinhood:

    endpoints = {
            "login": "https://api.robinhood.com/api-token-auth/",
            "investment_profile": "https://api.robinhood.com/user/investment_profile/",
            "accounts":"https://api.robinhood.com/accounts/",
            "ach_iav_auth":"https://api.robinhood.com/ach/iav/auth/",
            "ach_relationships":"https://api.robinhood.com/ach/relationships/",
            "ach_transfers":"https://api.robinhood.com/ach/transfers/",
            "applications":"https://api.robinhood.com/applications/",
            "dividends":"https://api.robinhood.com/dividends/",
            "edocuments":"https://api.robinhood.com/documents/",
            "instruments":"https://api.robinhood.com/instruments/",
            "margin_upgrades":"https://api.robinhood.com/margin/upgrades/",
            "markets":"https://api.robinhood.com/markets/",
            "notifications":"https://api.robinhood.com/notifications/",
            "orders":"https://api.robinhood.com/orders/",
            "password_reset":"https://api.robinhood.com/password_reset/request/",
            "quotes":"https://api.robinhood.com/quotes/",
            "document_requests":"https://api.robinhood.com/upload/document_requests/",
            "user":"https://api.robinhood.com/user/",
            "watchlists":"https://api.robinhood.com/watchlists/"
    }

    session = None

    username = None

    password = None

    headers = None

    auth_token = None


    ##############################
    #Logging in and initializing
    ##############################

    def __init__(self):
        self.session = requests.session()
        self.session.proxies = urllib.getproxies()
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en;q=1, fr;q=0.9, de;q=0.8, ja;q=0.7, nl;q=0.6, it;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "X-Robinhood-API-Version": "1.0.0",
            "Connection": "keep-alive",
            "User-Agent": "Robinhood/823 (iPhone; iOS 7.1.2; Scale/2.00)"
        }
        self.session.headers = self.headers

    def login(self, username, password):
        self.username = username
        self.password = password
        data = "password=%s&username=%s" % (self.password, self.username)
        res = self.session.post(self.endpoints['login'], data=data)
        res = res.json()
        try:
            self.auth_token = res['token']
        except KeyError:
            return False
        self.headers['Authorization'] = 'Token '+self.auth_token
        return True


    ##############################
    #GET DATA
    ##############################

    def investment_profile(self):
        return self.session.get(self.endpoints['investment_profile']).json()

    def instruments(self, stock=None):
        res = self.session.get(self.endpoints['instruments'], params={'query':stock.upper()})
        res = res.json()
        return res['results']

    def quote_data(self, stock=None):
        #Prompt for stock if not entered
        if stock is None:
            stock = raw_input("Symbol: ");
        url = str(self.endpoints['quotes']) + str(stock) + "/"
        #Check for validity of symbol
        try:
            res = json.loads((urllib.urlopen(url)).read());
            if len(res) > 0:
                return res;
            else:
                raise NameError("Invalid Symbol: " + stock);
        except (ValueError):
            raise NameError("Invalid Symbol: " + stock);

    def get_quote(self, stock=None):
        data = self.quote_data(stock)
        return data["symbol"]

    def print_quote(self, stock=None):
        data = self.quote_data(stock)
        print(data["symbol"] + ": $" + data["last_trade_price"]);

    def print_quotes(self, stocks):
        for i in range(len(stocks)):
            self.print_quote(stocks[i]);

    def ask_price(self, stock=None):
        return self.quote_data(stock)['ask_price'];

    def ask_size(self, stock=None):
        return self.quote_data(stock)['ask_size'];

    def bid_price(self, stock=None):
        return self.quote_data(stock)['bid_price'];

    def bid_size(self, stock=None):
        return self.quote_data(stock)['bid_size'];

    def last_trade_price(self, stock=None):
        return self.quote_data(stock)['last_trade_price'];

    def last_trade_price(self, stock=None):
        return self.quote_data(stock)['last_trade_price'];

    def previous_close(self, stock=None):
        return self.quote_data(stock)['previous_close'];

    def previous_close_date(self, stock=None):
        return self.quote_data(stock)['previous_close_date'];

    def adjusted_previous_close(self, stock=None):
        return self.quote_data(stock)['adjusted_previous_close'];

    def symbol(self, stock=None):
        return self.quote_data(stock)['symbol'];

    def last_updated_at(self, stock=None):
        return self.quote_data(stock)['updated_at'];

    def get_account(self):
        res = self.session.get(self.endpoints['accounts'])
        res = res.json()
        return res['results'][0]

    def positions(self):
        positions_url = self.get_account()['positions']
        return self.session.get(positions_url).json()['results']

    def instrument(self, instrument_url):
        return self.session.get(instrument_url).json()

    ##############################
    #PLACE ORDER
    ##############################

    def place_order(self, instrument, quantity=1, bid_price = None, transaction=None):
        if bid_price == None:
            bid_price = self.quote_data(instrument['symbol'])['bid_price']
        data = 'account=%s&instrument=%s&price=%f&quantity=%d&side=%s&symbol=%s&time_in_force=gfd&trigger=immediate&type=market' % (
            self.get_account()['url'],
            urllib.unquote(instrument['url']),
            float(bid_price),
            quantity,
            transaction,
            instrument['symbol']
        )
        res = self.session.post(self.endpoints['orders'], data=data)
        return res

    def place_buy_order(self, instrument, quantity, bid_price=None):
        transaction = "buy"
        return self.place_order(instrument, quantity, bid_price, transaction)

    def place_sell_order(self, instrument, quantity, bid_price=None):
        transaction = "sell"
        return self.place_order(instrument, quantity, bid_price, transaction)
