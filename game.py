import random
import os
import numpy as np

from base import Base
from player import Player
from card import Card
from graphics import Graphics
from table import Table

class Game(Graphics, Base):

    def __init__(self, title='Blackjack'):
        self.title = title
        self.table = Table()
        self.player = None
        self.cards = []
        self.score = 0
        super(Game, self).__init__()

    '''
        Shift cards, the max should be 52 and 4 for each card
    '''
    def getCards(self):
        cards = []
        for i in range(1, 14):
            for j in range(4):
                cards.append(Card(i,j))
        return cards

    '''
        Remove one card in cards array
    '''
    def removeCardFromDeck(self, discartedCard):
        if discartedCard in self.cards:
            self.cards.remove(discartedCard)
        pass

    def getPlayerName(self):
        return raw_input("Players name?:" + os.linesep)

    def render(self, player):
        player.render()
        self.table.render()
        pass

    '''
        Get one card from the deck and discard same card from cards array
    '''
    def hit(self, player):
        card = self.cards[0] # The the first card, that's how deales take cards from the deck
        player.addCard(card)
        self.removeCardFromDeck(card)
        pass

    def stay(self):
        card = self.cards[0] # The the first card, that's how deales take cards from the deck
        self.table.addCard(card)
        self.removeCardFromDeck(card)
        pass


    def nextMove(self, player):
        nextMove = self.renderList(['1) Hit', '2) Stand'])
        if nextMove == 1:
             self.hit(player)
             return
        elif nextMove == 2:
            self.stay()
            pass
        elif nextMove != 1 or nextMove != 2:
            print("Incorrect option, please select a correct option:" + os.linesep)
            self.nextMove()
        pass

    def getWinner(self, player, table):

        if (player.getScore() < 21 and (player.getScore() > table.getScore())) or table.getScore() > 21:
            self.fullScreenText('Congratulations %s, You\'re the Winner' % player.name)
        else:
            self.fullScreenText('You lose!')
            option = int(raw_input("Try Again? 1) Yes, 2) No:" + os.linesep))
            if (option == 1):
                self.init()
            else:
                return


    def startGame(self, player, cards):
        isPlayable = True
        isFirstGame = True
        while isPlayable:
            print('Score total: %i' % (self.score))
            if (isFirstGame):
                player.cards = cards[0:2] # get the first 2 cards
                for card in player.cards:
                    self.removeCardFromDeck(card)
                isFirstGame = False

            self.render(player)

            if (player.getScore() > 21 or self.table.getScore() > 21):
                # It means the game is finish
                isPlayable = False
                self.getWinner(player, self.table)
            else:
                self.nextMove(player);
        pass

    def init(self):
        player_name = self.getPlayerName()
        self.player = Player(1, player_name)
        self.cards = self.getCards()
        random.shuffle(self.cards)
        self.startGame(self.player, self.cards)


game = Game()

game.init()
