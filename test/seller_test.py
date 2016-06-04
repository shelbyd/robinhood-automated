from purchaser import Position
from seller import Seller, Sell

import unittest

class TestSeller(unittest.TestCase):
    def test_simple_optimal_trade(self):
        mutator = Seller(
                30.0,
                [Position('AGNC', 1)],
                {'AGNC': 1},
                {'AGNC': 49.0})
        self.assertItemsEqual(mutator.optimal_trades(), [Sell(1, 'AGNC')])

    def test_only_sell_one_position(self):
        mutator = Seller(
                30.0,
                [Position('AGNC', 2)],
                {'AGNC': 1},
                {'AGNC': 49.0})
        self.assertItemsEqual(mutator.optimal_trades(), [Sell(1, 'AGNC')])

    def test_only_sell_two_positions(self):
        mutator = Seller(
                60.0,
                [
                    Position('AGNC', 2),
                    Position('NLY', 2),
                ],
                {'AGNC': 1, 'NLY': 1},
                {'AGNC': 49.0, 'NLY': 35.00})
        self.assertItemsEqual(mutator.optimal_trades(), [Sell(1, 'AGNC'), Sell(1, 'NLY')])

