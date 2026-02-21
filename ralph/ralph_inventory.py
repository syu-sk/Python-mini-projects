import time
from ralph_item_instances import *
if __name__ == '__main__':
    raise NameError('This is the inventory implementation for ralph.py -- It is not meant to be run by itself')

'''Inventory Implementation'''
class Inventory:

    def __init__(self, player = None):
        self.player = player
        self.items: list[Item] = []
        self.money = 100
        self.is_holding = None
        self.is_wearing = None
    
    def get_inv(self):

        while True:

            self.items.sort(key = lambda x: x.item_name)
            print('--------------------')
            print('Items:')
            for index, item in enumerate(self.items):
                print(f'{index + 1}: [{item.rarity.upper()}] {item.item_name}')
            print('--------------------\nEquip | Use | View | [ENTER] to exit\n--------------------')
            decision = input('[INPUT] Action: ')

            if decision.lower() == 'equip':
                to_equip = input('[INPUT] What would you like to equip? ')
                try:    #possible errors: not a number, number not within list
                    if 1 <= int(to_equip) <= len(self.items):
                        self.equip(self.items[int(to_equip) - 1])
                        continue
                    else:
                        print('Invalid input. Please key in the index.')
                        continue
                except ValueError:
                    print('Invalid input. Please key in the index.')
                    continue
            
            elif decision.lower() == 'use':
                to_use = input('[INPUT] What would you like to use? ')
                try:    #possible errors: not a number, number not within list
                    if 1 <= int(to_use) <= len(self.items):
                        self.use(self.items[int(to_use) - 1])
                        continue
                    else:
                        print('Invalid input. Please key in the index.')
                        continue
                except ValueError:
                    print('Invalid input. Please key in the index.')
                    continue
            
            elif decision.lower() == 'view':
                to_view = input('[INPUT] What would you like to view? ')
                try:    #possible errors: not a number, number not within list
                    if 1 <= int(to_view) <= len(self.items):
                        self.items[int(to_view) - 1].view()
                        continue
                    else:
                        print('Invalid input. Please key in the index.')
                        continue
                except ValueError:
                    print('Invalid input. Please key in the index.')
                    continue
            
            elif not decision:
                break

            else:
                print('Invalid input. Please type an appropriate action.')
                time.sleep(1)
                continue

    def equip(self, item):
        if isinstance(item, Weapon):
            self.is_holding = item
            print(f'{item.item_name} has been equipped!')
            time.sleep(1)
        elif isinstance(item, Armor):
            self.is_wearing = item
            print(f'{item.item_name} has been equipped!')
            time.sleep(1)
        else:
            print(f'You try equipping {item.item_name}. Nothing happens.')
            time.sleep(1)
    
    def use(self, item):
        if isinstance(item, Consumable):
            if item.heal_value:
                self.player.hp += item.heal_value
                print(f'{item.item_name} has been used! HP restored by {item.heal_value}.')
                time.sleep(1)
            if item.mp_value:
                self.player.mp += item.mp_value
                print(f'{item.item_name} has been used! MP restored by {item.mp_value}.')
                time.sleep(1)
            if item.effect:
                item.effect.use(self.player)
                print(f'{item.effect.effect_name} has been applied on you for {item.effect.duration} turns!')
                time.sleep(1)
            self.remove_item(item)
        elif item.item_name == 'Glowing Iron Chunk':
            if rustyironsword not in self.items:
                print('The Glowing Iron Chunk does not seem to have any use.')
                time.sleep(1.5)
            else:
                print('Its strange golden hue seems to resonate with your Rusty Iron Sword.')
                time.sleep(2)
                decision = input('Use Glowing Iron Chunk? ')
                if decision.lower() in ['yes', 'y', 'use']:
                    print('The Glowing Iron Chunk fuses with your Rusty Iron Sword to form a New Iron Sword!')
                    time.sleep(2)
                    self.remove_items([rustyironsword, glowingironchunk])
                    self.add_item(newironsword)
                else:
                    print('You decide not to use the Glowing Iron Chunk.')
                    time.sleep(1.5)
        elif item.item_name == 'Valiant Gem':
            if newironsword not in self.items:
                print('The Valiant Gem does not seem to have any use.')
                time.sleep(1.5)
            else:
                print('Its strange golden hue seems to resonate with your New Iron Sword.')
                time.sleep(2)
                decision = input('Use Valiant Gem? ')
                if decision.lower() in ['yes', 'y', 'use']:
                    print('The Valiant Gem fuses with your New Iron Sword! In a bright flash, the New Iron Sword transform into the Hero Sword!')
                    time.sleep(2)
                    self.remove_items([newironsword, valiantgem])
                    self.add_item(herosword)
                else:
                    print('You decide not to use the Valiant Gem.')
                    time.sleep(1.5)
        else:
            print(f'You try using {item.item_name}. Nothing happens.')
            time.sleep(1)

    def buy_item(self, item):
        if self.money >= item.value:
            self.money -= item.value
            print(f'Bought {item.item_name} for {item.value} money!')
            time.sleep(1)
            self.add_item(item)
        else:
            time.sleep(0.5)
            raise IndexError
        
    def sell_item(self, item):
        try:
            self.money += item.value * 0.6
            self.items.remove(item)
            print(f'Sold {item.item_name} for {item.value * 0.6} money!')
        except AttributeError:
            print('Invalid Item sold.')
        except ValueError:
            print('Item is not in inventory.')
    
    def add_item(self, item):
        self.items.append(item)
        print(f'Added [{item.rarity.upper()}] {item.item_name} to inventory!')
    
    def add_items(self, itemlist):
        for item in itemlist:
            self.items.append(item)
            print(f'Added [{item.rarity.upper()}] {item.item_name} to inventory!')

    def remove_item(self, item):
        self.items.remove(item)
    
    def remove_items(self, itemlist):
        for item in itemlist:
            self.items.remove(item)