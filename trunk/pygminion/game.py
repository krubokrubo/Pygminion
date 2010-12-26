#!/usr/bin/env python

import cards
import random
import utils

def randomTurnTaker(turn, player, gameState):
    def firstPlayableCard(turnActions, hand):
        for card in hand:
            if turnActions or not card.action:
                return card
    
    print 'DEBUG: %s has hand: %s, deck: %s, discard: %s' % (player, player.hand, player.deck, player.discardPile)
    while firstPlayableCard(turn.actions, player.hand):
        turn.playCard(firstPlayableCard(turn.actions, player.hand))

    print 'DEBUG: %s has %d actions, %d buys, and %s money this turn' % (player, turn.actions, turn.buys, turn.money)
    buyOptions = turn.getBuyOptions()
    if buyOptions:
        buyChoice = random.choice(buyOptions)
        turn.buy(buyChoice)
        print 'DEBUG: %s bought %s' % (player, buyChoice)


class Player:
    """A Dominion player."""
    
    def __init__(self, name, initialCards=None, turnTaker=randomTurnTaker):
        self.name = name
        
        # We start with the cards in the discard pile.
        # They'll be shuffled to create the deck.
        
        if initialCards: self.discardPile = initialCards
        else:            self.discardPile = [cards.copper]*7 + [cards.estate]*3
        
        # Probably not necessary here, more to create a list
        
        self.points  = 0
        self.money   = 0
        self.buys    = 0
        self.actions = 0
        self.cards   = 0
        
        self.cardsInPlay = []
        self.durationCards = []
        self.deck = []
        self.hand = []

        self.turnTaker = turnTaker
        
        self.draw(5)

    def __str__(self):
        return self.name

        
    def draw(self, numCards):
        while numCards:
            try:
                self.hand.append(self.deck.pop(0))
                numCards -= 1
            except IndexError:
                if len(self.discardPile) < 1:
                    print "*** DEBUG: %s can't draw %s cards.  Deck: %s, hand: %s, discard: %s" % (self.name, numCards, len(self.deck), len(self.hand), len(self.discardPile))
                    return True
                else:
                    print "*** DEBUG: Shuffling %s's discard pile into a new deck..." % self.name
                    random.shuffle(self.discardPile)
                    self.deck = list(self.discardPile)
                    self.discardPile = []
                
    def turn(self, gameState):
        self.currentTurn = Turn(self, gameState)
        self.turnTaker(self.currentTurn, self, gameState) 
        self.currentTurn.cleanup()        

# This class is responsible for presenting the available options during each turn 
# Which option is chosen will depend on the player's "turnTaker" callback
class Turn:
    def __init__(self, player, gameState):
        self.player = player
        self.gameState = gameState
        self.actions = 1
        self.buys = 1
        self.money = "0"
        for card in player.durationCards:
            card.cbInitTurn(gameState)
     
    def getActionOptions(self):
        return [card for card in self.player.hand if card.action]

    def playCard(self, card):
        assert(card in self.player.hand, "card not in hand :(")
        if card.action:
            assert(self.actions > 0, "no actions remain in turn :(")
            self.actions -= 1
        self.player.hand.remove(card)
        card.cbPlay(self.gameState)
        self.player.cardsInPlay.append(card)

    def playAllNonActions(self):
        for card in self.player.hand:
            if not card.action:
                self.playCard(card)

    def getBuyOptions(self):
        options = []
        for supply in self.gameState.supplies:
            if not supply.isEmpty():
                if utils.cmpMoney(self.money, supply.cost()) >= 0:
                    options.append(supply)
        return options

    def buy(self, supply):
        assert(utils.cmpMoney(self.money, supply.cost()) >= 0, "not enough money :(")
        assert(self.buys > 0, "no buys remain in turn :(")
        self.buys -= 1
        self.money = utils.subtractMoney(self.money, supply.cost())
        self.player.discardPile.append(supply.buy())

    def cleanup(self):
        self.player.discardPile += self.player.hand
        self.player.hand = []
        self.player.discardPile += self.player.cardsInPlay
        self.player.cardsInPlay = []
        self.player.draw(5)
        
class SupplyPile:
    def __init__(self, card, numCards=10):
        self.pile = numCards*[card]
        self.card = card
    
    def __repr__(self):
        return "%dx[%s (%s)]" % (len(self.pile), self.card.name, self.cost())
    
    def cost(self):
        return self.card.cost
    
    def isEmpty(self):
        return len(self.pile) == 0
    
    def buy(self):
        if not self.isEmpty():
            
            return self.pile.pop(0)
        else:
            raise ValueError

class Game:
    """A Dominion game."""
    
    def __init__(self, numPlayers=2, players=None, supplyCards=None, potions=False, coloniesPlatinums=False):
        if players:
            self.players = players
        else:
            self.players = []
            for i in range(numPlayers):
                self.players.append(Player("Player %s" % (i + 1)))
        
        vpCards = [0, 0, 8, 12, 12, 15, 18][numPlayers]
        
        self.supplies = [SupplyPile(cards.copper, 60), SupplyPile(cards.silver, 60), SupplyPile(cards.gold, 60),
                         SupplyPile(cards.estate, vpCards), SupplyPile(cards.duchy, vpCards), SupplyPile(cards.province, vpCards)]
        self.trash = []
        self.currentPlayer = 0
        
    def isGameOver(self):
        emptySupplies = 0
        for supply in self.supplies:
            if supply.isEmpty():
                if supply.card == cards.province: return True
                if supply.card == cards.colony:   return True
                emptySupplies += 1
        if len(self.players) <= 3:
            return emptySupplies >= 3
        else:
            return emptySupplies >= len(self.players) - 1
    
    def next(self):
        while not self.isGameOver():
            yield self.players[self.currentPlayer].turn(self)
            self.currentPlayer += 1
            if self.currentPlayer >= len(self.players):
                self.currentPlayer = 0
        
        raise StopIteration
    
    def pointTotals(self):
        for i in range(len(self.players)):
            player = self.players[i]
            self.currentPlayer = i
            all_cards = player.hand + player.discardPile + player.deck + player.cardsInPlay + player.durationCards
            for card in all_cards:
                card.cbEndCount(self)
            print "%s: %d -- %s" % (player.name, player.points, all_cards)

