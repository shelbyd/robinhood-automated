from purchaser import Purchaser
from main import Main

import sys

class MainPurchaser(Main):
    def get_mutator(self):
        if len(sys.argv) > 1:
            cash = float(sys.argv[1])
        else:
            cash = self.cash()

        return Purchaser(
                cash,
                self.positions(),
                self.weights(),
                self.prices())

MainPurchaser().main()
