import random
import time
from ralph_item_instances import *
if __name__ == '__main__':
    raise NameError('This is the shop implementation for ralph.py -- It is not meant to be run by itself')

'''Shop Implementation'''

class Shop():

    def __init__(self, player, items, length = 1):
        self.player = player
        self.items = items
        self.length = length
        self.full = None
    
    def generate_shop(self):
        self.full = random.sample(self.items, k = self.length)

    def get_shop(self):
        if not self.full:       #part of the mechanism for a permanent shop -- unless rerolling
            self.generate_shop()

        while True:
            time.sleep(1)
            print('--------------------\nSHOP\n--------------------')
            for index, item in enumerate(self.full):
                print(f'{index + 1}: {item.item_name} | [{item.value}]')
            print('--------------------\nBuy | Sell | Reroll | [ENTER] to exit\n--------------------')
            decision = input('[INPUT] Action: ')

            if decision.lower() == 'buy':
                to_buy = input('[INPUT] Select item to buy. To close, press [ENTER]. ')

                if not to_buy:
                    break

                try:        #possible exceptions: number out of list, not enough money
                    to_buy = int(to_buy)
                    if not 1 <= to_buy <= len(self.full):
                        print('Invalid item to buy. Submit number or name.')
                        continue
                    view_item = self.full[to_buy - 1]
                    view_item.view()
                    decision = input('[INPUT] Are you sure you want to buy this item? Press [ENTER] to confirm.')
                    if not decision or decision in ['Yes', 'Y', 'yes', 'y']:
                        self.player.inventory.buy_item(view_item)
                        time.sleep(0.5)
                        continue
                    elif decision.lower() in ['no', 'n']:
                        print('Buy cancelled.')
                        continue
                    else:
                        print('Invalid input. Try again.')
                        continue
                except ValueError:
                    if to_buy.lower() not in [item.name.lower() for item in self.full]:
                        print('Invalid item to buy. Submit number or name.')
                        continue
                    try:    #possible exceptions: not enough money

                        index = [item.name.lower() for item in self.full].index(to_buy.lower())
                        view_item = self.full[index]
                        print(f'--------------------\n{view_item.name} [{view_item.rarity.upper()}]:\n{view_item.desc}\n--------------------\nCost: {view_item.value}')
                        decision = input('[INPUT] Are you sure you want to buy this item? Press [ENTER] to confirm.')

                        if not decision or decision in ['Yes', 'Y', 'yes', 'y']:
                            self.player.inventory.buy_item(view_item)
                            time.sleep(0.5)
                            continue
                        elif decision.lower() in ['no', 'n']:
                            print('Buy cancelled.')
                            continue
                        else:
                            print('Buy cancelled.')
                            continue
                    except IndexError:
                        continue
                except IndexError:      #if not enough money. This is produced by inventory
                    print(f'Not enough money! {view_item.item_name} costs {view_item.value} but you only have {self.player.inventory.money}.')
                    continue

            elif decision.lower() == 'sell':
                self.player.inventory.items.sort(key = lambda x: x.item_name)
                print('--------------------')
                for index, item in enumerate(self.player.inventory.items):
                    print(f'{index + 1}: [{item.rarity.upper()}] {item.item_name}')
                print('--------------------')
                while True:
                    decision = input('Which item to sell? [ENTER] to cancel: ')
                    try:
                        if 1 <= int(decision) <= len(self.player.inventory.items):
                            self.player.inventory.sell_item(self.player.inventory.items[int(decision)])
                        elif not decision:
                            break
                        else:
                            print('Invalid input. Please key in index.')
                            continue
                    except:
                        print('Invalid input. Please key in index.')
                        continue
                    
            elif decision.lower() == 'reroll':
                decision = input('Are you sure you want to reroll the shop? It will cost 20 money: ')
                if decision.lower() in ['yes', 'y', 'reroll']:
                    self.player.inventory.money -= 20
                    self.reroll_shop()
                    print('Shop rerolled!')
                    continue
                else:
                    print('Reroll cancelled.')
                    continue

            elif not decision:
                break

            else:
                print('Invalid Input. Please enter action.')

    def reroll_shop(self):    #tbh the only thing different from generating shop is its name
        self.full = random.sample(self.items, k = self.length)