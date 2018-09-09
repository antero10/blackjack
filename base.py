
from functools  import reduce

class Base(object):


    def __init__(self):
        pass

    '''
        GetScore function, Sum all the number of the cards
    '''
    def getScore(self, cards):
        if len(cards) > 1:
            return reduce((lambda x, y: x + y), list(map(lambda x: x.number, cards)))
        if len(cards) == 1:
            return cards[0].number
        return 0
