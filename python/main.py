from Robinhood import Robinhood
import getpass
from data import weights
from memoize import Memoize
from purchaser import Position

class Main:
    def main(self):
        optimal_trades = self.get_mutator().optimal_trades()
        for trade in sorted(optimal_trades, key=lambda trade: trade.symbol):
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

    @Memoize
    def cash(self):
        return float(self.trader().get_account()['cash'])

    @Memoize
    def positions(self):
        positions = []

        for position in self.trader().positions():
            instrument = self.trader().instrument(position['instrument'])
            symbol = instrument['symbol']
            quantity = float(position['quantity'])
            positions.append(Position(symbol, quantity))

        return positions

    @Memoize
    def weights(self):
        return weights

    @Memoize
    def prices(self):
        prices = {}
        for symbol in self.weights():
            prices[symbol] = float(self.trader().last_trade_price(symbol))
        return prices
