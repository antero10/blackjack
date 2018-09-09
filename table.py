import os

from base import Base
from graphics import Graphics
class Table(Graphics, Base):

    def __init__(self):
        self.cards = []
        pass

    def addCard(self, card):
        self.cards.append(card)


    def render(self):
        self.renderTitle('Table Cards')
        self.renderScore()
        for card in self.cards:
            card.render()
        pass

    def renderScore(self):
        print('%s Score: %s %s' % (os.linesep, self.getScore(), os.linesep)) #Using 2 lines separator at the beginning and at the end

    def getScore(self):
        return super(Table, self).getScore(self.cards)
