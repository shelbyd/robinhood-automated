from purchaser import Purchaser
from main import Main

class MainPurchaser(Main):
    def get_mutator(self):
        return Purchaser(
                self.cash(),
                self.positions(),
                self.weights(),
                self.prices())

MainPurchaser().main()
