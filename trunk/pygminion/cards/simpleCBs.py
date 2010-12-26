import utils

def add(actions=0, cards=0, money="0", buys=0, points=0):
    def func(gameState, actions=actions, cards=cards, money=money, buys=buys, points=points):
        currentPlayer = gameState.players[gameState.currentPlayer]
        currentTurn = currentPlayer.currentTurn
        currentTurn.actions += actions
        currentTurn.buys += buys
        currentTurn.money = utils.addMoney(currentTurn.money, money)
        currentPlayer.draw(cards)
        currentPlayer.points += points
    
    return func
