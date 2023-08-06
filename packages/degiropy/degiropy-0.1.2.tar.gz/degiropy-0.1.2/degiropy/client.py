import requests
import json
from collections import defaultdict

default_logger = lambda message : print(message)

class Degiropy:

    BASE_URL = "https://trader.degiro.nl/"

    def __init__(self, username: str, password: str, logger=default_logger, verbose=False):
        self.data = None
        self.int_account = None
        self.verbose = verbose
        self.logger = logger
        self.username = username
        self.password = password

    def _log(self, message):
        if self.verbose:
            self.logger.log(message)

    def _log_status_code(self, method, status_code):
        self._log(f'{method}: Status code: {status_code}')
    
    def login(self):
        self.sess = requests.Session()
        
        url = f'{self.BASE_URL}login/secure/login'
        payload = {
            'username': self.username,
            'password': self.password,
            'isPassCodeReset': False,
            'isRedirectToMobile': False
        }
        header = {
            'content-type': 'application/json'
        }

        r = self.sess.post(url, headers=header, data=json.dumps(payload))
        self._log_status_code('Login', r.status_code)

        set_cookie = r.headers['Set-Cookie']
        session_id_cookie = set_cookie.split(';')[0]
        self.session_id = session_id_cookie.split('=')[1]

    def get_config(self):
        ''' Retrieve user's intAccount number
        '''
        url = f'{self.BASE_URL}pa/secure/client'
        params = {
            'sessionId': self.session_id
        }

        r = self.sess.get(url, params=params)
        self._log_status_code('get_config', r.status_code)

        data = r.json()

        self.int_account = data['data']['intAccount']

        self._log('Account id: {}'.format(self.int_account))

    def init_data(self):
        ''' Retrieves data: orders, news, cash funds.
        Method has to be called everytime you need to sync with Degiro
        '''
        url = f'{self.BASE_URL}trading/secure/v5/update/{str(self.int_account)}'
        url += ';jsessionid=' + self.session_id
        params = {
            'portfolio': 0,
            'totalPortfolio': 0,
            'orders': 0,
            'historicalOrders': 0,
            'transactions': 0,
            'alerts': 0,
            'cashFunds': 0,
            'intAccount': self.int_account,
            'sessionId': self.session_id
        }

        try:
            r = self.sess.get(url, params=params)
            self._log_status_code('Get data', r.status_code)

            self.data = r.json()
            return True
        except Exception:
            return False

    def get_cash_funds(self):
        ''' Retrives cash funds
        '''
        if self.data == None:
            self.init_data()       
        cash_funds = dict()
        for cf in self.data['cashFunds']['value']:
            entry = dict()
            for y in cf['value']:
                if y['name'] == 'currencyCode':
                    key = y['value']
                    continue
                entry[y['name']] = y['value']
            cash_funds[key] = entry

        return cash_funds
    
    # Only returns a summary of the portfolio
    def get_portfolio_summary(self):
        ''' Porfolio summary is a dictionary of cash and money equity of assets:
        { 'equity': 100, 'cash': 100 }
        '''
        pf = self.get_portfolio()
        cf = self.get_cash_funds()
        tot = 0
        for eq in pf['PRODUCT'].values():
            tot += eq['value']     

        summary = dict()
        summary['equity'] = tot
        summary['cash'] = cf['EUR']['value']
        return summary

    def get_portfolio(self, skip_historic: bool = True):
        ''' Retrieves the entire portfolio
        '''
        if self.data == None:
            self.init_data()       
        portfolio = []
        for row in self.data['portfolio']['value']:
            entry = dict()
            for y in row['value']:
                k = y['name']
                v = None
                if 'value' in y:
                    v = y['value']
                entry[k] = v

            if skip_historic and (entry['size'] == 0):
                continue
            portfolio.append(entry)

        ## Restructure portfolio and add extra data
        portf_n = defaultdict(dict)
        # Restructuring
        for r in portfolio:
            pos_type = r['positionType']
            pid = r['id'] # Product ID
            del(r['positionType'])
            del(r['id'])
            portf_n[pos_type][pid]= r

        # Adding extra data
        url = f'{self.BASE_URL}product_search/secure/v5/products/info'
        params = {
            'intAccount': str(self.int_account),
            'sessionId': self.session_id
        }
        header={
            'content-type': 'application/json'
        }
        pid_list = list(portf_n['PRODUCT'].keys())
        r = self.sess.post(url, headers=header, params=params, data=json.dumps(pid_list))
        self._log_status_code('Getting extra data (get_portfolio)', r.status_code)

        extra_data = r.json()
        if 'data' not in extra_data:
            return portf_n
        for k,v in extra_data['data'].items():
            del(v['id'])
            # Some bonds tend to have a non-unit size
            portf_n['PRODUCT'][k]['size'] *= v['contractSize']
            portf_n['PRODUCT'][k].update(v)

        return portf_n

    def get_orders(self):
        ''' Retrieves only orders from portfolio
        '''
        if self.data == None:
            self.init_data()
        orders = []
        for row in self.data['orders']['value']:
            entry = dict()
            for y in row['value']:
                k = y['name']
                v = None
                if 'value' in y:
                    v = y['value']
                entry[k] = v

            orders.append(entry)

        return orders

    def get_portfolio_mini(self):
        ''' Returns mini portfolio (similar to get_portfolio, with no extra data)
        '''
        if self.data == None:
            self.init_data()       
        portfolio = []
        for row in self.data['portfolio']['value']:
            entry = dict()
            for y in row['value']:
                k = y['name']
                v = None
                if 'value' in y:
                    v = y['value']
                entry[k] = v
            # Skip history products
            if entry['size'] != 0:
                portfolio.append(entry)

        ## Restructure portfolio and add extra data
        portf_n = defaultdict(dict)
        # Restructuring
        for r in portfolio:
            pos_type = r['positionType']
            pid = r['id'] # Product ID
            del(r['positionType'])
            del(r['id'])
            portf_n[pos_type][pid]= r

        return portf_n 

    def place_order(self, order):
        ''' Create and confirm an order
        '''
        confirmation = self.check_order(order)
        return self.confirm_new_order(order, confirmation["confirmationId"])

    def check_order(self, order):
        ''' Sends an order to Degiro to check its validity.
        Returns confirmation id if valid.
        '''
        url = f'{self.url_config["tradingUrl"]}v5/checkOrder;jsessionid={self.session_id}'
        params = {
            'intAccount': str(self.int_account),
            'sessionId': self.session_id
        }
        header = {
            'content-type': 'application/json'
        }
        payload = {
            'buySell': order["buysell"],
            'orderType': order["orderType"],
            'productId': order["productId"],
            'timeType': order["timeType"],
            'size': order["size"],
            'price': order["price"]
        }

        r = self.sess.post(url, headers=header, params=params, data=json.dumps(payload))
        self._log_status_code('Check order', r.status_code)

        confirmation = r.json()
        self._log(f'Confirmation id: {confirmation["data"]["confirmationId"]}')
        return {
            "order": order,
            "confirmationId": confirmation["data"]["confirmationId"]
        }

    def confirm_new_order(self, order, confirmation_id):
        return self.confirm_order(order, confirmation_id, True)

    def confirm_update_order(self, order, order_id):
        return self.confirm_order(order, order_id, False)

    def confirm_order(self, order, confirmation_id, is_new: bool = True):
        ''' Confirms a new order or order update.
        Returns order id
        '''
        url = f"{self.url_config['tradingUrl']}v5/order/{confirmation_id};jsessionid={self.session_id}"
        params = {
            'intAccount': str(self.int_account),
            'sessionId': self.session_id
        }
        header={
            'content-type': 'application/json;charset=UTF-8'
        }
        payload = {
            'buySell': order["buysell"],
            'orderType': order["orderType"],
            'productId': order["productId"],
            'timeType': order["timeType"],
            'size': order["size"],
            'price': order["price"]
        }

        if is_new:
            r = self.sess.post(url, data=json.dumps(payload), params=params, headers=header)
            self._log_status_code('Confirm new order', r.status_code)

            order_completed = r.json()
            self._log(f'Order placed, order id: {order_completed["data"]["orderId"]}')
            return order_completed["data"]["orderId"]
        else:
            r = self.sess.put(url, data=json.dumps(payload), params=params, headers=header)
            self._log_status_code('Confirm update order', r.status_code)
            return confirmation_id


    def init_url_config(self):
        ''' Inits url config
        '''
        url = f'{self.BASE_URL}login/secure/config'
        payload = {
            'sessionId': self.session_id
        }
        header={
            'Cookie': f"JSESSIONID={self.session_id};"
        }
        r = self.sess.get(url, params=payload, headers=header)
        self._log_status_code('Init url config', r.status_code)

        data = r.json()
        self.url_config = data['data']

    def search_product_symbol(self, symbol: str):
        ''' Search by product symbol (ticker).
        Note degiro symbol can differ from stock ticker
        '''
        url = f"{self.url_config['productSearchUrl']}v5/products/lookup"

        params = {
            'intAccount': str(self.int_account),
            'sessionId': self.session_id,
            'searchText': symbol
        }
        r = self.sess.get(url, params=params)

        self._log_status_code('Search product symbol', r.status_code)

        data = r.json()
        for search_result in data["products"]:
            if "symbol" not in search_result:
                continue
            if symbol.upper() == search_result["symbol"].upper():
                return search_result
        return None
