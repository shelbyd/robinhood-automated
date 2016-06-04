import getpass
from Robinhood import Robinhood
from purchaser import Position, Purchaser
from data import weights

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

trader = Robinhood()
login(trader)

mutator = Purchaser(
        float(trader.get_account()['cash']),
        positions(trader),
        weights,
        prices(weights, trader))

for trade in mutator.optimal_trades():
    trade.execute_trade(trader)
