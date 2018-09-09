import random
import os
import time
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

    '''
        Stay action, in this action the table/delear plays
    '''

    def stay(self, player):
        card = self.cards[0] # The the first card, that's how deales take cards from the deck
        tableScore = self.table.getScore()
        while tableScore <= 21 and tableScore < player.getScore():
            card = self.cards[0]
            self.table.addCard(card)
            self.removeCardFromDeck(card)
            self.render(player)
            tableScore = self.table.getScore()
            time.sleep(2)
        if tableScore < 21 and (tableScore > player.getScore()):
            self.endGame('You lose!')
        return 



    def nextMove(self, player):
        nextMove = self.renderList(['1) Hit', '2) Stand'])
        if nextMove == 1:
             self.hit(player)
             return
        elif nextMove == 2:
            self.stay(player)
            pass
        elif nextMove != 1 or nextMove != 2:
            print("Incorrect option, please select a correct option:" + os.linesep)
            self.nextMove()
        pass

    def getWinner(self, playerScore, tableScore):

        if (playerScore < 21 and (playerScore > tableScore)) or tableScore > 21 or playerScore == 21:
            self.endGame('Winner Winner Chicken dinner')
        else:
            self.endGame('You lose!')

    def endGame(self, text):
        self.fullScreenText(text)
        self.table.cards = [] # Reset game
        option = self.renderList(['1) Try Again', '2) Exit'])
        if (option == 1):
            self.init()
        else:
            return

    def startGame(self, player, cards):
        isPlayable = True
        isFirstGame = True
        while isPlayable:
            playerScore = player.getScore()
            tableScore = self.table.getScore()
            if (isFirstGame):
                player.cards = cards[0:2] # get the first 2 cards
                self.table.cards = cards[2:3]
                for card in player.cards:
                    self.removeCardFromDeck(card)
                for card in self.table.cards:
                    self.removeCardFromDeck(card)
                isFirstGame = False

            self.render(player)

            if (playerScore >= 21 or tableScore >= 21):
                # It means the game is finish
                isPlayable = False
                self.getWinner(playerScore, tableScore)
            else:
                self.nextMove(player);
        pass

    def init(self):
        player_name = self.getValueInput('Insert Player Name: ')
        self.player = Player(1, player_name)
        self.cards = self.getCards()
        random.shuffle(self.cards)
        self.startGame(self.player, self.cards)


game = Game()

game.init()
