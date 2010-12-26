""" Track the expected value of a hand in Dominion, as cards are added to the deck """

import random
import utils
from game import Game, Player, Turn
from cards import *

player = Player('me')
game = Game(numPlayers=1, players=[player])

def drawOver():
    quietshuffle()
    player.draw(5)

    player.currentTurn = Turn(player, game)
    turn = player.currentTurn

    # play as many action cards as possible, then as many treasure cards as possible
    def firstActionCard(hand):
        for card in hand:
            if card.action:
                return card

    def firstTreasureCard(hand):
        for card in hand:
            if card.treasure:
                return card

    while turn.actions and firstActionCard(player.hand):
        turn.playCard(firstActionCard(player.hand))
    while firstTreasureCard(player.hand):
        turn.playCard(firstTreasureCard(player.hand))

def printBriefState(player):
    print '%s: %d Act  %d Buy  $ %s  %s%s' % (player,
        player.currentTurn.actions, player.currentTurn.buys, player.currentTurn.money,
        player.cardsInPlay, player.hand)
    
def sample():
    print player.allCards()
    for a in range(10):
        drawOver()
        printBriefState(player)
    act = buy = 0
    mon = '0'
    for a in range(1000):
        drawOver()
        act += player.currentTurn.actions
        buy += player.currentTurn.buys
        mon = utils.addMoney(mon, player.currentTurn.money)
    print 'avg %d Act %d Buy %s Money' % (act, buy, mon)

def _gain(card):
    player.discardPile.append(card)

def gain(card):
    _gain(card)
    sample()

def _trash(card):
    quietshuffle()
    player.deck.remove(card)

def trash(card):
    _trash(card)
    sample()

def quietshuffle():
    """ shuffle in deck to keep the draw quiet """
    player.deck += player.discardPile + player.hand + player.cardsInPlay
    player.discardPile = []
    player.hand = []
    player.cardsInPlay = []
    random.shuffle(player.deck)   

def test(card):
    _gain(card)
    sample()
    _trash(card) 

print '''You should run this interactively ("python -i countdeck.py")
  At the Python prompt, say ... 
  sample()      to see 10 guesses of what your luck will be like with current deck
  gain(card)    gain the card and take a new sample
  trash(card)   trash the card and take a new sample
  test(card)    take a new sample with the card, but don't keep it in the deck. '''
