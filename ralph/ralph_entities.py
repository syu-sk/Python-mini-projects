import time
import sys
from ralph_shop import *
from ralph_item_instances import *
if __name__ == '__main__':
    raise NameError('This is the entity implementation for ralph.py -- It is not meant to be run by itself')

'''Entity Implementation'''
class Entity:

    def __init__(self):
        self.statuses = dict()                  #status: no. of turns
        self.is_player = None

    def status_tick(self):

        for status in self.statuses.keys():     #take any by turn actions
            if status.dot:
                self.hp -= status.dot
                print(f'{self.name} takes {status.dot} damage from [{status.effect_name}]!')
                time.sleep(1)
                print(f'{self.name} has {self.hp} HP remaining!')
                time.sleep(1)
            elif status.hot:
                self.hp += status.hot
                print(f'{self.name} heals {status.hot} health from [{status.effect_name}]!')
                time.sleep(1)
                print(f'{self.name} has {self.hp} HP!')
                time.sleep(1)
        
        for status in self.statuses.keys():     #reduce status effects by 1 turn every turn
            self.statuses[status] -= 1
            if self.statuses[status] == 0:
                print(f'{self.name} no longer has [{status.effect_name}].')
        
        self.statuses = {key: value for key, value in self.statuses.items() if value > 0}
            
    '''
    Status modifiers:
    Final modifier values calculated using ALL status effects. Any additional calculation (crit chance, base stats) will be done through Player/Enemy

    Convention: Property internals will define [stat]_modifier, do not duplicate. The ability classes themselves will have an attribute [stat]_mod, do not duplicate.
    '''

    @property
    def attack_modifier(self):
        attack_modifier = 1.0
        for status in self.statuses.keys():
            if status.atk_mod:
                attack_modifier *= status.atk_mod
        return attack_modifier

    @property
    def defense_modifier(self):
        defense_modifier = 1.0
        for status in self.statuses.keys():
            if status.def_mod:
                defense_modifier *= status.def_mod
        return defense_modifier
    
    @property
    def defense_adder(self):
        defense_adder = 0
        for status in self.statuses.keys():
            if status.def_add:
                defense_adder += status.def_add
        return defense_adder

    @property
    def speed_adder(self):
        speed_adder = 0
        for status in self.statuses.keys():
            if status.spd_add:
                speed_adder += status.spd_add
        return speed_adder


class Player(Entity):

    def __init__(self, inventory, name, hp, defense, atk, mp, speed):
        
        self.name = name
        self.inventory = inventory

        '''
        levels:
        vigor - +10 max hp per point
        bulk - +1 defense per point
        lethality - +5% damage per point
        intelligence - +2 max mp per point
        swiftness - +0.5 speed per point

        all calculated before status effects
        '''
        self.levels = {'vigor': 0, 'bulk': 0, 'lethality': 0, 'intelligence': 0, 'swiftness': 0}
        self.xp = 0

        '''
        stats
        '''
        self._hp = hp
        self._defense = defense
        self._speed = speed
        self._mp = mp
        self._max_hp = 1000
        self._max_mp = 10

        '''
        metadata
        '''
        super().__init__()      #this is still needed to inherit parent attributes -- its methods are inherited by default
        self.is_player = True
        self.shop = None
        self.shop_level = 0
        self.stage = 1
        self.room = 0

    @property
    def level(self):
        return sum(self.levels.values())
    @property
    def level_xp(self):
        return 50 + self.level * 50

    @property
    def max_hp(self):
        try:
            return self._max_hp + self.levels['vigor'] * 10 + self.is_wearing.hp_boost
        except AttributeError:
            return self._max_hp + self.levels['vigor'] * 10
    @property
    def max_mp(self):
        return (self._max_mp + self.levels['intelligence'] * 2)
    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, value):
        if value < 0:
            self._hp = 0
        elif value > self.max_hp:
            self._hp = self.max_hp
        else:
            self._hp = round(value, 1)
    @property
    def mp(self):
        return self._mp
    @mp.setter
    def mp(self, value):
        if value < 0:
            self._mp = 0
        elif value > self.max_mp:
            self._mp = self.max_mp
        else:
            self._mp = round(value, 1)
    @property
    def defense(self):
        try:
            return (self._defense + self.inventory.is_wearing.def_value + self.levels['bulk'] * 1) * self.defense_modifier + self.defense_adder
        except AttributeError:
            return (self._defense + self.levels['bulk'] * 1) * self.defense_modifier + self.defense_adder
    @defense.setter
    def defense(self, value):
        if value < 0:
            self._defense = 0
        elif value > 100:
            self._defense = 100
        else:
            self._defense = round(value, 1)
    @property
    def dealt_damage(self):
        damage = self.inventory.is_holding.damage * (1 + self.levels['lethality'] * 0.05) * self.attack_modifier
        return damage
    @property
    def speed(self):
        return self._speed + self.levels['swiftness'] * 0.5 + self.speed_adder

    @property
    def ability(self):
        return self.inventory.is_holding.ability
    @property
    def armor_ability(self):
        try:
            return self.inventory.is_wearing.ability
        except:
            return None
    
    @property
    def is_alive(self):
        return not self.hp == 0
    
    def take_damage(self, dealt_dmg):
        damage = dealt_dmg * (100 - self.defense) / 100
        if damage < 0:
            damage = 0
        self.hp -= damage
    
    def get_menu(self):

        while True:

            print(f'--------------------\n{self.name} | STAGE {self.stage} ROOM {self.room}\n--------------------')
            print(f'HP: {self.hp} / {self.max_hp}\nDefense: {self.defense}\nSpeed: {self.speed}\nMP: {self.mp} / {self.max_mp}\nXP: {self.xp}\nMoney: {self.inventory.money}\n')
            print(f'Currently Equipped:\n[HAND] {self.inventory.is_holding.item_name if self.inventory.is_holding else None}\n[ARMOR] {self.inventory.is_wearing.item_name if self.inventory.is_wearing else None}')
            print('--------------------\nInventory | Shop | Skills | [ENTER] to exit\n--------------------')

            decision = input('[INPUT] Action: ')
            if decision in ['inv', 'Inv', 'inventory', 'Inventory']:
                self.inventory.get_inv()
                continue
            elif decision.lower() == 'shop':
                self.get_shop()
                continue
            elif decision.lower() == 'skills':
                self.get_level_up()
                continue
            elif not decision:
                break
            else:
                print('Invalid Input. Please enter action.')
                time.sleep(1)
                continue
    
    def get_shop(self):

        #shop generation -- only one generation per stage unless reroll. and each stage has a different item pool
        if self.shop_level == 0 and self.shop_level != self.stage:
            self.shop = Shop(self, [ironspear, greatsword, morningstar,  thebat, mangrovedwellerarmor, smallhealthvial, smallmanavial, glowingironchunk], length = 4)
            self.shop_level += 1
        elif self.shop_level == 1 and self.shop_level != self.stage:
            self.shop = Shop(self, [froststaff, flamestaff, agedgrimoire, blizzardbow, icicle, fireball, flareblitzblade, furvest, heroarmor, frostsalve, embersalve, mediumhealthvial, mediummanavial, flaskofregeneration, flaskofstrength, valiantgem], length = 7)
            self.shop_level += 1
        elif self.shop_level == 2 and self.shop_level != self.stage:
            #stage 3 shop
            pass
        
        self.shop.get_shop()
    
    def get_level_up(self):
        print(f'--------------------\nLevel {self.level}\n--------------------')
        for key, value in self.levels.items():
            print(f'[{key.upper()}] | {value}')
        print(f'XP required for next level: {self.level_xp}')
        print('--------------------')
        time.sleep(2)
        if self.xp >= self.level_xp:
            decision = input(f'You have enough xp to level up. Choose an attribute to increase: ')
            if decision.lower() in self.levels.keys():
                print(f'Added one point to [{decision.upper()}]!')
                self.levels[decision.lower()] += 1
                self.xp -= self.level_xp
                time.sleep(1)
            else:
                print('Invalid input. Please key in an attribute.')
                time.sleep(1)
        else:
            _ = input('You do not have enough xp to level up. [ENTER] to proceed.')
    
    def status_tick(self):
        if self.is_player and azarothsheart in self.inventory.items:
            for status in list(self.statuses.keys()):
                if status.effect_name in ('Frostbite', 'Draconic Frostbite'):
                    self.statuses.pop(status)
                    print("Azaroth's Heart cures you of Frostbite!")
                    time.sleep(2)
        elif not self.is_player:
            print('1')
        elif not azarothsheart in self.inventory.items:
            print('2')

        for status in self.statuses.keys():     #take any by turn actions
            if status.dot:
                self.hp -= status.dot
                print(f'{self.name} takes {status.dot} damage from [{status.effect_name}]!')
                time.sleep(1)
                print(f'{self.name} has {self.hp} HP remaining!')
                time.sleep(1)
            elif status.hot:
                self.hp += status.hot
                print(f'{self.name} heals {status.hot} health from [{status.effect_name}]!')
                time.sleep(1)
                print(f'{self.name} has {self.hp} HP!')
                time.sleep(1)
        
        for status in self.statuses.keys():     #reduce status effects by 1 turn every turn
            self.statuses[status] -= 1
            if self.statuses[status] == 0:
                print(f'{self.name} no longer has [{status.effect_name}].')
        
        self.statuses = {key: value for key, value in self.statuses.items() if value > 0}

    def death(self):
        print('You have died...')
        sys.exit(1)

class Enemy(Entity):

    def __init__(self, name, desc, hp, atk, speed, defense = 0, loot = None, ability = None):
        super().__init__()
        self.name = name
        self.desc = desc
        self._hp = hp
        self._atk = atk
        self._speed = speed
        self._defense = defense
        self.loot = loot    #a LootTable object
        self.ability = ability
        self.is_player = False
    
    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, value):
        if value < 0:
            self._hp = 0
        else:
            self._hp = round(value, 1)
    
    @property
    def atk(self):
        return self._atk * self.attack_modifier
    @atk.setter
    def atk(self, value):
        self._atk = value
    
    @property
    def defense(self):
        return self._defense * self.defense_modifier + self.defense_adder
    @defense.setter
    def defense(self, value):
        if value < 0:
            self._defense = 0
        elif value > 100:
            self._defense = 100
        else:
            self._defense = round(value, 1)
    
    @property
    def speed(self):
        return self._speed + self.speed_adder
    @speed.setter
    def speed(self, value):
        self._speed = value
    
    @property
    def dealt_damage(self):
        damage = self.atk
        return damage
    
    @property
    def is_alive(self):
        return not self.hp == 0
    
    def take_damage(self, dealt_dmg):
        damage = dealt_dmg * (100 - self.defense) / 100
        if damage < 0:
            damage = 0
        self.hp -= damage

class Boss(Enemy):

    def __init__(self, name, desc, hp, atk, speed, defense = 0, loot = None, ability = None):
        super().__init__(name, desc, hp, atk, speed, defense, loot)       #inherits all attributes from enemy class -- i.e the WHOLE __init__ block
        self.ability = ability


'''Damage Implementation - DEPRECATED'''

'''Since player has additional calculations in their damage such as held weapon, atk, strength etc, there needs to be two separate calculations depending on whether the player is the damage dealer or receiver'''

def eff_dmg(dealer, receiver):      #how much damage from A to B
    if dealer.is_player:
        effective = dealer.held.damage * (100 + dealer.atk) / 100 * (100 - receiver.defense) / 100
    elif receiver.is_player:
        effective = dealer.atk * (100 - receiver.defense) / 100
    return effective
'''Alternatively, damage implementation could be further rooted into the entity classes themselves. For example, there could be a method in each entity class that defines how much *total* damage they send out, as well as a method that processes how much damage they take, taking into account damage reduction effects. That way I only need a simple deal_damage function that takes two arguments (dealer, receiver) which uses both the above methods to instantly compute the real damage each party takes.'''