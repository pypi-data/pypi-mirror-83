from enum import Enum


class Actions(Enum):
    BUY = 'B'
    SELL = 'S'


class OrderTypes(Enum):
    LIMITED = 0
    MARKET_ORDER = 2
    STOP_LOSS = 3
    STOP_LIMITED = 1


class TimeTypes(Enum):
    DAY = 1
    PERMANENT = 3


class ProductTypes(Enum):
    ALL = None
    SHARES = 1
    BONDS = 2
    FUTURES = 7
    OPTIONS = 8
    INVESTEMED_FUNDS = 13
    LEVERAGED_PRODUCTS = 14
    ETFS = 131
    CFDS = 535
    WARRANTS = 536


class Sort(Enum):
    ASC = 'asc'
    DESC = 'desc'
