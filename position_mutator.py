import itertools

class CommonEqualityMixin(object):
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(frozenset(self.__dict__.iteritems()))

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
        for symbol in self.symbols():
            buys[symbol.name] = 0

        remaining_cash = self.cash
        while True:
            symbol = self.lowest_equity(buys)

            if remaining_cash <= symbol.price:
                break

            buys[symbol.name] += 1
            remaining_cash -= symbol.price

        return [Buy(buys[symbol], symbol) for symbol in buys if buys[symbol] > 0]

    def lowest_equity(self, buys):
        sorted_list = sorted(self.symbols(buys), key=Symbol.weighted_equity)
        grouped_by_equity = itertools.groupby(sorted_list, key=Symbol.weighted_equity)
        minimum_symbols = list(next(grouped_by_equity)[1])
        return min(minimum_symbols, key=lambda s: s.price)

    def position_for_symbol(self, symbol):
        possibilities = (p for p in self.positions if p.symbol == symbol)
        return next(possibilities, Position(symbol, 0.0))

    def symbols(self, buys={}):
        return [
            Symbol(name,
                   self.position_for_symbol(name).quantity + buys.get(name, 0),
                   self.prices[name],
                   self.weights[name])
            for name in self.weights.keys()
        ]

class Buy(CommonEqualityMixin):
    def __init__(self, amount, symbol):
        self.amount = amount
        self.symbol = symbol

    def __repr__(self):
        return "Buy %d %s" % (self.amount, self.symbol)

    def execute_trade(self, trader):
        print "Buy %d of %s" % (self.amount, self.symbol)

class Symbol(CommonEqualityMixin):
    def __init__(self, name, quantity, price, weight):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.weight = weight

    def weighted_equity(self):
        return self.price * self.quantity / self.weight
