# degiropy

Unofficial Degiro API in Python

## Getting Started

### Installing

```
pipenv --python 3
pipenv install requests
pipenv install degiropy
```

### Usage

```python
from degiropy import Degiropy
from degiropy.types import Actions, OrderTypes, TimeTypes, ProductTypes, Sort

degiro = Degiropy(username, password, verbose=True)
# Initialization
degiro.login()
degiro.get_config()
degiro.init_url_config()
degiro.init_data()

# Usage examples
cf = degiro.get_cash_funds()
print(cf['EUR']['value']) # prints EUR amount

degiro.get_portfolio_summary() # returns object with `equity` and `cash` properties

degiro.get_portfolio(False) # Returns portfolio skipping historical data

order = {} # Fill order data
degiro.place_order(order) # Places an order 
```

## Development

```
python setup.py build
python setup.py install
```

## License

[BSD 2](https://github.com/alexberazouski/degiropy/blob/main/LICENSE)
