from Robinhood import Robinhood
import getpass
from data import weights
from memoize import Memoize
from purchaser import Position

class Main:
    def main(self):
        for trade in self.get_mutator().optimal_trades():
            trade.execute_trade(self.trader())

    @Memoize
    def trader(self):
        trader = Robinhood()
        self.login(trader)
        return trader

    def login(self, trader):
        successful = False
        while not successful:
            successful = trader.login(
                    username=raw_input('Username: '),
                    password=getpass.getpass())
            if not successful:
                print 'Incorrect username/password.'

    def cash(self):
        return float(self.trader().get_account()['cash'])

    def positions(self):
        positions = []

        for position in self.trader().positions():
            instrument = self.trader().instrument(position['instrument'])
            symbol = instrument['symbol']
            quantity = float(position['quantity'])
            positions.append(Position(symbol, quantity))

        return positions

    def weights(self):
        return weights

    def prices(self):
        prices = {}
        for symbol in self.weights():
            prices[symbol] = float(self.trader().last_trade_price(symbol))
        return prices
