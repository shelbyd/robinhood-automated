import getpass
from Robinhood import Robinhood
from position_mutator import Position, PositionMutator

import json
def json_print(data):
    print json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))

weights = {
    'AGNC': 2,
    'NLY': 2,
    'JNJ': 2,
    'PG': 2,
    'KO': 2,
    'HCP': 1,
    'T': 1,
    'MCY': 1,
    'ORI': 1,
    'ABBV': 1,
    'ED': 1,
    'NUE': 1,
    'VVC': 1,
}

trader = Robinhood()

successful = False
while not successful:
    successful = trader.login(
            username=raw_input('Username: '),
            password=getpass.getpass())
    if not successful:
        print 'Incorrect username/password.'

positions = []

for position in trader.positions():
    instrument = trader.instrument(position['instrument'])
    symbol = instrument['symbol']
    quantity = float(position['quantity'])
    positions.append(Position(symbol, quantity))

prices = {}
for symbol in weights:
    prices[symbol] = float(trader.last_trade_price(symbol))

mutator = PositionMutator(
        float(trader.get_account()['cash']),
        positions,
        weights,
        prices)

for trade in mutator.optimal_trades():
    trade.execute_trade(trader)
