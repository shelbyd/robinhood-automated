from purchaser import CommonEqualityMixin, Purchaser, Symbol

import itertools

class Seller(Purchaser):
    def __init__(self, cash_needed, positions, weights, prices):
        self.cash_needed = cash_needed
        self.positions = positions
        self.weights = weights
        self.prices = prices

    def optimal_trades(self):
        sells = {}
        for symbol in self.symbols():
            sells[symbol.name] = 0

        remaining_cash_needed = self.cash_needed
        while remaining_cash_needed > 0:
            symbol = self.highest_equity(sells)

            sells[symbol.name] -= 1
            remaining_cash_needed -= symbol.price

        return [Sell(-sells[symbol], symbol) for symbol in sells if sells[symbol] < 0]

    def highest_equity(self, sells):
        sorted_list = reversed(sorted(self.symbols(sells), key=Symbol.weighted_equity))
        grouped_by_equity = itertools.groupby(sorted_list, key=Symbol.weighted_equity)
        maximum_symbols = list(next(grouped_by_equity)[1])
        return min(maximum_symbols, key=lambda s: s.price)

class Sell(CommonEqualityMixin):
    def __init__(self, amount, symbol):
        self.amount = amount
        self.symbol = symbol

    def __repr__(self):
        return "Sell %d %s" % (self.amount, self.symbol)

    def execute_trade(self, trader):
        print "Sell %d of %s" % (self.amount, self.symbol)
