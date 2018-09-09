
from functools  import reduce

class Base(object):


    def __init__(self):
        pass

    def getScore(self, cards):
        if len(cards) > 1:
            sum = 0
            for card in cards:
                sum = sum + card.number
            return sum
        if len(cards) == 1:
            return cards[0].number
        return 0
