from position_mutator import PositionMutator, Position, Buy
import unittest

class TestPositionMutator(unittest.TestCase):
    def test_simple_optimal_trade(self):
        mutator = PositionMutator(
                50.0,
                [],
                {'AGNC': 1},
                {'AGNC': 49.0})
        self.assertItemsEqual(mutator.optimal_trades(), [Buy(1, 'AGNC')])

    def test_optimal_trade_with_two_targets(self):
        mutator = PositionMutator(
                50.0,
                [],
                {'AGNC': 1, 'NLY': 1},
                {'AGNC': 24.0, 'NLY': 24.0})
        self.assertItemsEqual(mutator.optimal_trades(), [
            Buy(1, 'AGNC'),
            Buy(1, 'NLY'),
        ])

    def test_optimal_trade_with_different_weights(self):
        mutator = PositionMutator(
                33.0,
                [],
                {'AGNC': 2, 'NLY': 1},
                {'AGNC': 10.0, 'NLY': 10.0})
        self.assertItemsEqual(mutator.optimal_trades(), [
            Buy(2, 'AGNC'),
            Buy(1, 'NLY'),
        ])

    def test_optimal_trade_where_three_can_be_bought(self):
        mutator = PositionMutator(
                33.0,
                [],
                {'AGNC': 1},
                {'AGNC': 10.0})
        self.assertItemsEqual(mutator.optimal_trades(), [
            Buy(3, 'AGNC'),
        ])

    def test_optimal_trade_where_already_have_one(self):
        mutator = PositionMutator(
                11.0,
                [Position('AGNC', 1.0)],
                {'AGNC': 1, 'NLY': 1},
                {'AGNC': 10.0, 'NLY': 10.0})
        self.assertItemsEqual(mutator.optimal_trades(), [
            Buy(1, 'NLY'),
        ])

    def test_optimal_trade_where_weighting_buys_would_fail(self):
        mutator = PositionMutator(
                16.0,
                [Position('AGNC', 1.0)],
                {'AGNC': 1, 'NLY': 2},
                {'AGNC': 4.0, 'NLY': 10.0})
        self.assertItemsEqual(mutator.optimal_trades(), [
            Buy(1, 'NLY'),
            Buy(1, 'AGNC'),
        ])

    def test_optimal_trade_equal_equity_picks_lower_price(self):
        mutator = PositionMutator(
                6.0,
                [],
                {'AGNC': 1, 'NLY': 1},
                {'AGNC': 4.0, 'NLY': 5.0})
        self.assertItemsEqual(mutator.optimal_trades(), [
            Buy(1, 'AGNC'),
        ])

if __name__ == "__main__":
    unittest.main()

