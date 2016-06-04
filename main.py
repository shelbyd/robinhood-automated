import getpass
from Robinhood import Robinhood
from position_mutator import Position, PositionMutator

import json
def login(trader):
    successful = False
    while not successful:
        successful = trader.login(
                username=raw_input('Username: '),
                password=getpass.getpass())
        if not successful:
            print 'Incorrect username/password.'

def prices(weights, trader):
    prices = {}
    for symbol in weights:
        prices[symbol] = float(trader.last_trade_price(symbol))
    return prices

def positions(trader):
    positions = []

    for position in trader.positions():
        instrument = trader.instrument(position['instrument'])
        symbol = instrument['symbol']
        quantity = float(position['quantity'])
        positions.append(Position(symbol, quantity))

    return positions

weights = {}
desired_stocks = [
    'AWR',
    'CINF',
    'CL',
    'DOV',
    'EMR',
    'GPC',
    'JNJ',
    'KO',
    'LANC',
    'LOW',
    'MMM',
    'NDSN',
    'NWN',
    'PH',
    'PG',
    'VVC',
]
for stock in desired_stocks:
    weights[stock] = 1

trader = Robinhood()
login(trader)

mutator = PositionMutator(
        float(trader.get_account()['cash']),
        positions(trader),
        weights,
        prices(weights, trader))

for trade in mutator.optimal_trades():
    trade.execute_trade(trader)
