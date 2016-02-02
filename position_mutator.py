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
        trades = {}

        remaining_cash = self.cash
        while remaining_cash > min(self.prices.values()):
            for symbol in self.weights:
                trades[symbol] = trades.setdefault(symbol, 0) + self.weights[symbol]
                remaining_cash -= self.prices[symbol] * self.weights[symbol]

        return [Buy(trades[symbol], symbol) for symbol in trades]

class Buy(CommonEqualityMixin):
    def __init__(self, amount, symbol):
        self.amount = amount
        self.symbol = symbol

    def __repr__(self):
        return "Buy %d %s" % (self.amount, self.symbol)

if __name__ == "__main__":
    import unittest

    class TestPositionMutator(unittest.TestCase):
        def test_simple_optimal_trade(self):
            mutator = PositionMutator(
                    50.0,
                    [Position('AGNC', 0.0)],
                    {'AGNC': 1},
                    {'AGNC': 49.0})
            self.assertItemsEqual(mutator.optimal_trades(), [Buy(1, 'AGNC')])

        def test_optimal_trade_with_two_targets(self):
            mutator = PositionMutator(
                    50.0,
                    [
                        Position('AGNC', 0.0),
                        Position('NLY', 0.0),
                    ],
                    {'AGNC': 1, 'NLY': 1},
                    {'AGNC': 24.0, 'NLY': 24.0})
            self.assertItemsEqual(mutator.optimal_trades(), [
                Buy(1, 'AGNC'),
                Buy(1, 'NLY'),
            ])

        def test_optimal_trade_with_different_weights(self):
            mutator = PositionMutator(
                    33.0,
                    [
                        Position('AGNC', 0.0),
                        Position('NLY', 0.0),
                    ],
                    {'AGNC': 2, 'NLY': 1},
                    {'AGNC': 10.0, 'NLY': 10.0})
            self.assertItemsEqual(mutator.optimal_trades(), [
                Buy(2, 'AGNC'),
                Buy(1, 'NLY'),
            ])

        def test_optimal_trade_where_three_can_be_bought(self):
            mutator = PositionMutator(
                    33.0,
                    [
                        Position('AGNC', 0.0),
                    ],
                    {'AGNC': 1},
                    {'AGNC': 10.0})
            self.assertItemsEqual(mutator.optimal_trades(), [
                Buy(3, 'AGNC'),
            ])

    unittest.main()

