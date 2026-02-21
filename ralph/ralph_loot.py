import random
if __name__ == '__main__':
    raise NameError('This is the loot table implementation for ralph.py -- It is not meant to be run by itself')

#Loottables always return xp, then money, then loot drops

class LootTable:

    def __init__(self, xp = None, money = None, weights = None, loot = None):
        self.xp = xp
        self.money = money
        self.loot = [] if loot is None else list(loot)        #loot refers to items, in a list.
        self.weights = weights

    def loot_list(self):
        return self.loot
    
    def drop(self):
        raise AttributeError('Loot drop not yet implemented')
    
class EnemyLoot(LootTable):

    def __init__(self, xp, money, variation = 0, weights = None):
        super().__init__(xp, money)
        self.variation = variation
        self.weights = weights
    
    def drop(self):
        xpdrop = random.randint(round((1 - self.variation / 100) * self.xp), round((1 + self.variation / 100) * self.xp))
        moneydrop = random.randint(round((1 - self.variation / 100) * self.money), round((1 + self.variation / 100) * self.money))
        return [xpdrop, moneydrop]

class BossLoot(LootTable):

    def __init__(self, xp, money, loot = None, weights = None, variation = 0):
        super().__init__(xp, money)
        self.loot = loot
        self.weights = weights
        self.variation = variation
    
    def drop(self):
        xpdrop = random.randint(round((1 - self.variation / 100) * self.xp), round((1 + self.variation / 100) * self.xp))
        moneydrop = random.randint(round((1 - self.variation / 100) * self.money), round((1 + self.variation / 100) * self.money))
        itemdrop = random.choice(self.loot)
        return [xpdrop, moneydrop, itemdrop]
    
class ChestLoot(LootTable):

    def __init__(self, loot, weights = None, rolls = 1):
        super().__init__(loot = loot, weights = weights)
        self.rolls = rolls
    
    def drop(self):
        return random.choices(self.loot, weights = self.weights, k = self.rolls)
