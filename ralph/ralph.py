import time
from ralph_entities import *
from ralph_stage import *
from ralph_inventory import *

#add list
#sell multiplier
#xp system, thereby introducing perks
#weapon abilities
#boss abilities
#status effects

'''
          Dependencies:

INVENTORY --> RALPH <--------------------------=
    |   \       |                =---------> STAGE <--- ENCOUNTER
= ITEMS  \   ENTITIES -----> ENEMY INST        |
|   |     |   |    |            |   ^        LOOT
|   |     |   |   SHOP          |   =----------|
|   |     \   |    |            |
|   =-----> ITEM INST <---------|   
=--------------------------- ABILITIES
'''

def main():

    '''Game Initiation'''

    player_name = input('What is your name? ')
    
    # while True:
    #     difficulty = input('Difficulty Level (1 - 3): ')
    #     try:
    #         difficulty = int(difficulty)
    #         if not 1 <= difficulty <= 3:
    #             print('Invalid difficulty -- Try again')
    #             continue
    #         break
    #     except ValueError:
    #         print('Invalid difficulty -- Try again')
    # time.sleep(1)
    print(f'Starting save. Name: {player_name}')

    '''Profile Initiation'''
    Player_Inventory = Inventory()
    player = Player(inventory = Player_Inventory, name = player_name, hp = 100, defense = 0, atk = 0, mp = 10, speed = 3)
    Player_Inventory.player = player
    Player_Inventory.add_item(rustyironsword)
    time.sleep(1)
    
    '''Pre-game Preparation'''
    print(f'Welcome {player.name}! You begin your journey up Ralph\'s Tower!')
    time.sleep(1)
    print('Please make sure to equip a weapon before embarking on your journey.')
    time.sleep(1)
    player.get_menu()
    
    '''Floor One'''
    stage1 = Stage(player, 1, 1)
    stage1.do_stage()

    print('CONGRATULATIONS! You have completed [STAGE 1]!')

    stage2 = Stage(player, 2, 1)
    stage2.do_stage()

if __name__ == '__main__':
    main()