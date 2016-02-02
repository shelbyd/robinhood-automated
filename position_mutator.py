class CommonEqualityMixin(object):
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__dict__)

class Position:
    def __init__(self, symbol, quantity):
        self.symbol = symbol
        self.quantity = quantity

class PositionMutator:
    def __init__(self, cash, positions, weights, prices):
        self.cash = cash
        self.positions = positions
        self.weights = weights
        self.prices = prices

    def optimal_trades(self):
        buys = {}
        for symbol in self.weights:
            buys[symbol] = 0

        remaining_cash = self.cash
        while True:
            symbol = self.lowest_equity(buys)

            if remaining_cash <= self.prices[symbol]:
                break

            buys[symbol] += 1
            remaining_cash -= self.prices[symbol]

        return [Buy(buys[symbol], symbol) for symbol in buys if buys[symbol] > 0]

    def lowest_equity(self, buys):
        return min(self.weights.keys(), key=lambda symbol: self.weighted_equity(symbol, buys))

    def weighted_equity(self, symbol, buys):
        quantity = self.position_for_symbol(symbol).quantity + buys[symbol]
        price = self.prices[symbol]
        weight = self.weights[symbol]

        return price * quantity / weight


    def position_for_symbol(self, symbol):
        possibilities = (p for p in self.positions if p.symbol == symbol)
        return next(possibilities, Position(symbol, 0.0))

class Buy(CommonEqualityMixin):
    def __init__(self, amount, symbol):
        self.amount = amount
        self.symbol = symbol

    def __repr__(self):
        return "Buy %d %s" % (self.amount, self.symbol)

    def execute_trade(self, trader):
        print "Would buy %d of %s" % (self.amount, self.symbol)
