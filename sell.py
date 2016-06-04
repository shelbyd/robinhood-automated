from seller import Seller
from main import Main

import sys

target_cash = float(sys.argv[1])

class MainSeller(Main):
    def get_mutator(self):
        return Seller(
                target_cash - self.cash(),
                self.positions(),
                self.weights(),
                self.prices())

MainSeller().main()
