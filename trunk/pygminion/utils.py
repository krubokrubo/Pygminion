import string

def cmpMoney(a, b):
    ''' Whether a can buy b.  cmp('5','3p') == -1 but also cmp('3p','5') == -1. '''
    a_potions = a.count('p')
    b_potions = b.count('p')
    a_coins = int(a.replace('p',''))
    b_coins = int(b.replace('p',''))
    if a_coins == b_coins and a_potions == b_potions:
        return 0
    elif a_coins < b_coins or a_potions < b_potions:
        return -1
    else:
        return 1
        

def addMoney(a, b):
    a_potions = a.count('p')
    b_potions = b.count('p')
    a_coins = int(a.replace('p',''))
    b_coins = int(b.replace('p',''))
    
    return str(a_coins + b_coins) + "p"*(a_potions + b_potions)
        
def subtractMoney(a, b):
    a_potions = a.count('p')
    b_potions = b.count('p')
    a_coins = int(a.replace('p',''))
    b_coins = int(b.replace('p',''))

    assert(a_coins >= b_coins and a_potions >= b_potions, "not enough money to subtract :(")
    
    return str(a_coins - b_coins) + "p"*(a_potions - b_potions)
