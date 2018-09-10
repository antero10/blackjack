from arts.cards import Arts
from graphics import Graphics
import sys
class Card(Graphics):

    '''
        Card Class.
        Recieve the number of the card and the type (Clubs, Diamonds, Hearts, Spades)
    '''
    def __init__(self, number, type_id):
        self.types = ['clubs', 'diamonds', 'hearts', 'spades']
        self.number = number
        self.value = self.getCardValue(number)
        self.type = self.types[type_id]
        self.Arts = Arts()
        super(Card, self).__init__()

    def render(self):
        number_name = self.getNumberName(self.number)
        print('%s\t' % self.Arts.getArt('CARD_%s_OF_%s' % (number_name, self.type.upper())))

    '''
        Switch number to proper name in arts
    '''
    def getNumberName(self, number):
        '''
            Yeah python don't have a switch statement....
        '''
        if number == 1:
            return 'ACE'
        elif number >= 2 and number <= 10:
            return number
        elif number == 11:
            return 'JACK'
        elif number == 12:
            return 'KING'
        elif number == 13:
            return 'QUEEN'

    '''
        Get the value of the card.
        If the card is a Jack, Queen or King (11,12,13), the value is 10
        If the card is Ace, the value is 11
    '''
    def getCardValue(self, number):
        if number == 1:
            return 11
        if number > 10:
            return 10
        elif number <= 10 or number >= 2:
            return number

    def __str__(self):
        return "Card: %s, Type: %s" % (self.number, self.type)
