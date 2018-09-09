import os

from base import Base
from graphics import Graphics
from random import randint
from functools import reduce

class Player(Graphics, Base):

    def __init__(self, id, name = '', cards = [], credits = 500):
        self.name = name if name != '' else self.createRandomName()
        self.cards = cards
        self.credits = credits
        super(Player, self).__init__()

    def render(self):
        self.renderTitle('Player %s' % self.name)
        self.renderScore()
        for card in self.cards:
            card.render()

    def addCard(self,card):
        self.cards.append(card)


    def createRandomName(self):
        names = ['Bob', 'Mike', 'MoneyMaker', 'TheCashLord', 'YourWorstNightmare']
        return names[randint(0, len(names) - 1 )]

    def renderScore(self):
        print('Player: %s %sScore: %i %s ' % (self.name, os.linesep, self.getScore(), os.linesep))

    def getScore(self):
        return super(Player, self).getScore(self.cards)

    def __str__(self):
        return 'Player: %s, Cards: %s' % (self.name, self.cards)
