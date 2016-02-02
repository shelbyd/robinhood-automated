import getpass
from Robinhood import Robinhood
from position_mutator import Position, PositionMutator

import json
def json_print(data):
    print json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))

targets = {
        'AGNC': 1,
        'NLY': 1,
        'JNJ': 1,
        'PG': 1,
        'KO': 1,
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
for symbol in targets:
    prices[symbol] = float(trader.last_trade_price(symbol))

mutator = PositionMutator(
        float(trader.get_account()['cash']),
        positions,
        targets,
        prices)

for trade in mutator.optimal_trades():
    trade.execute(trader)
