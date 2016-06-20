from purchaser import Purchaser
from main import Main

import sys

cash = None
if len(sys.argv) > 1:
    cash = float(sys.argv[1])

class MainPurchaser(Main):
    def get_mutator(self):
        return Purchaser(
                self.cash() if cash is None else cash,
                self.positions(),
                self.weights(),
                self.prices())

MainPurchaser().main()
