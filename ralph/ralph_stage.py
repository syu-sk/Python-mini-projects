import random
import time
from ralph_encounter import *
from ralph_loot import *
from ralph_enemy_instances import *
from ralph_item_instances import *
if __name__ == '__main__':
    raise NameError('This is the stage implementation for ralph.py -- It is not meant to be run by itself')


'''Stage Implementation'''
class Stage:
    '''
    I suppose main program flow will be in this class instead
    Stage 1: 5 Rooms. 
    Stage 2: 7 Rooms. 
    Stage 3: 9 Rooms. 
    Each stage may contain up to one chest room or one library. shops are now to be in the main menu.
    Upon completing a room, there will be 2 choices to choose from to go to next room.
    Each choice will reveal information about the room, about its tenacity, or its nature.
    '''
    def __init__(self, player, stage, difficulty):
        self.player = player
        self.stage = stage
        self.difficulty = difficulty

        self.stagelength = 3 + self.stage * 2
        self.chest_counter = 0
        self.library_counter = 0
        self.next_room_type = None
        self.next_room_choices = [None, None]

    def do_stage(self):
        self.begin_stage()
        for _ in range(self.stagelength):
            self.player.room += 1
            self.room()
        self.player.room = 0
        self.player.stage += 1
        print(f'Stage {self.stage} completed!')
        
    def begin_stage(self):
        print('Your journey up the tower starts!')
        time.sleep(0.5)
        print(f'----------\nFloor {self.stage}\n----------')
        time.sleep(0.5)

    def room(self):

        '''Pre-room preparation'''
        print('Before you start the next room, you may choose to prepare.')
        
        while True:
            time.sleep(1)
            print('--------------------\nMenu | [ENTER] to proceed\n--------------------')
            decision = input('[INPUT] Action: ')
            if decision.lower() == 'menu':
                self.player.get_menu()
                continue
            elif not decision:
                break
            else:
                print('Invalid input. Please try again.')
                continue

        if self.player.room == 1:      #boss room
            print('The end of the floor is before you. Yet, what stands between would be your hardest challenge yet. ')
            self.generate_room('boss', self.difficulty)
        
        else:
            print('You have two rooms ahead of you.')
            time.sleep(0.5)


            for i in range(2):                                      #room generation algorithm
                room = random.randint(1,5)
                if room == 1 and self.chest_counter == 0:
                    self.next_room_choices[i] = 'chest'
                elif room == 2 and self.library_counter == 0:
                    self.next_room_choices[i] = 'library'
                elif room == 3:
                    self.next_room_choices[i] = 'miniboss'
                else:
                    tenacity = random.randint(1,2)
                    self.next_room_choices[i] = ['enemy', tenacity]

            for i in range(2):                                      #room description message
                sides = ['left', 'right']
                if self.next_room_choices[i] == 'library':
                    print(f'[{sides[i].upper()}] --> A faint yellow light pours out of the room, along with the sound of someone murmuring echoes through. You peek inside and see what looks like library.')
                elif self.next_room_choices[i] == 'chest':
                    print(f'[{sides[i].upper()}] --> You look into the room and see that there is a singular chest in the centre.')
                elif self.next_room_choices[i] == ['enemy', 1]:
                    print(f'[{sides[i].upper()}] --> It appears the room has a number of enemies inside. Pursuing it may be dangerous.')
                elif self.next_room_choices[i] == ['enemy', 2]:
                    print(f'[{sides[i].upper()}] --> The room is only partially opened. You are only able to make out a few shadowy figures and walls riddled with scratches.')
                elif self.next_room_choices[i] == 'miniboss':
                    print(f'[{sides[i].upper()}] --> You feel a strong force of bloodlust emanating from that room. Your instincts tell you what lingers inside is not to be underestimated. Still, with greater risks come greater rewards.')

            time.sleep(0.5)
            while True:
                picked_room = input('[INPUT] Pick a room: ')
                picked_room = picked_room.lower()
                if picked_room == 'left':
                    self.generate_room(self.next_room_choices[0], self.difficulty)
                    time.sleep(0.5)
                    break
                elif picked_room == 'right':
                    self.generate_room(self.next_room_choices[1], self.difficulty)
                    time.sleep(0.5)
                    break
                else:
                    print('Invalid input. Please try again.')
                
    def generate_room(self, room, difficulty):

        def generate_library_room(difficulty):
            print('You have entered the library! Don\'t worry, you are safe in here.')
            time.sleep(1)
            while True:
                time.sleep(0.5)
                print('You may choose to proceed or view the library.\nTo view the library, type open. To proceed to the next room, press [ENTER].')
                time.sleep(2)
                decision = input('[INPUT] Proceed or view library? ')
                if decision.lower() == 'open':
                    print('You grab a book, flipping through the page. You feel an influx of knowledge surging through.')
                    time.sleep(1)
                    xp_gain = random.randint(200,400) * self.stage
                    self.player.xp += xp_gain
                    print(f'You have gained {xp_gain} xp! You now have {self.player.xp} xp.')
                    time.sleep(1)
                    print(f'--------------------\nYou have completed Room {self.player.room} of Stage {self.stage}!\n--------------------')
                    break
                elif not decision:
                    print('You choose not to view the library.')
                    time.sleep(1)
                    break
                else:
                    print('Invalid input, please try again.')
                    time.sleep(0.5)
                    continue
        
        def generate_chest_room(difficulty):            #a lil more complicated as there is an enemy encounter built-in.
                                                        #seems that ill also need to include a separate case for each stage.
            print('You chance upon a treasure chest!')
            time.sleep(1)
            while True:
                time.sleep(0.5)
                print('You may choose to open the chest or leave it. To open, type open. To leave the chest, press [ENTER].')
                time.sleep(0.5)
                decision = input('[INPUT] Open or leave chest? ')
                if decision.lower() == 'open':
                    if random.randint(1, 4) == 1:       #mimic chance encounter
                        print('The chest sprung open and charged at you!')
                        time.sleep(0.5)
                        if self.stage == 1:     #try to keep each fight assigned to 'fight', to keep names clean
                            fight = Fight(self.stage, self.player.room, self.player, [mangrovemimic,])
                            fight.start()
                            time.sleep(1)
                            print(f'--------------------\nYou have completed Room {self.player.room} of Stage {self.stage}!\n--------------------')
                            break
                        elif self.stage == 2:
                            if random.randint(1,2) == 1:
                                fight = Fight(self.stage, self.player.room, self.player, [frostmimic,])
                                fight.start()
                                time.sleep(1)
                                print(f'--------------------\nYou have completed Room {self.player.room} of Stage {self.stage}!\n--------------------')
                                break
                            else:
                                fight = Fight(self.stage, self.player.room, self.player, [volcanicmimic,])
                                fight.start()
                                time.sleep(1)
                                print(f'--------------------\nYou have completed Room {self.player.room} of Stage {self.stage}!\n--------------------')
                                break
                        elif self.stage == 3:
                            pass
                        break
                    else:
                        print('You open the chest.')
                        time.sleep(0.5)
                        if self.stage == 1:
                            loot = stage1_chest_loot.drop()
                            self.player.inventory.add_items(loot)
                            time.sleep(1)
                            print(f'--------------------\nYou have completed Room {self.player.room} of Stage {self.stage}!\n--------------------')
                            break
                        elif self.stage == 2:
                            loot = stage2_chest_loot.drop()
                            self.player.inventory.add_items(loot)
                            time.sleep(1)
                            print(f'--------------------\nYou have completed Room {self.player.room} of Stage {self.stage}!\n--------------------')
                            break
                        elif self.stage == 3:
                            pass
                elif not decision:
                    print('You choose not to open the chest, perhaps out of wisdom.')
                    time.sleep(0.5)
                    break
                else:
                    print('Invalid input, please try again.')
                    time.sleep(0.5)
                    continue

        def generate_enemy1_room(difficulty):
            print('You walk into an enemy room.')
            time.sleep(1)
            if self.stage == 1:     #try to keep each fight assigned to 'fight', to keep names clean
                fight = Fight(self.stage, self.player.room, self.player, random.choices([mangrovecrocodile, mangrovebandit, mangroveslime], k=2))
                fight.start()
                print(f'--------------------\nYou have completed Room {self.player.room} of Stage {self.stage}!\n--------------------')
            elif self.stage == 2:
                fight = Fight(self.stage, self.player.room, self.player, random.choices([frostwraith, blazeling, icegolem, infernal], k=2))
                fight.start()
                print(f'--------------------\nYou have completed Room {self.player.room} of Stage {self.stage}!\n--------------------')
            elif self.stage == 3:
                pass
    
        def generate_enemy2_room(difficulty):
            print('You walk into an enemy room. Your opponents seem more innumerable than usual.')
            time.sleep(1)
            if self.stage == 1:
                fight = Fight(self.stage, self.player.room, self.player, random.choices([mangrovecrocodile, mangrovebandit, mangroveslime], k=3))
                fight.start()
                print(f'--------------------\nYou have completed Room {self.player.room} of Stage {self.stage}!\n--------------------')
            elif self.stage == 2:
                fight = Fight(self.stage, self.player.room, self.player, random.choices([frostwraith, blazeling, icegolem, infernal], k=3))
                fight.start()
                print(f'--------------------\nYou have completed Room {self.player.room} of Stage {self.stage}!\n--------------------')
            elif self.stage == 3:
                pass

        def generate_miniboss_room(difficulty):
            print('You walk into an enemy room. The prowess of your adversary perks your senses.')
            time.sleep(1)
            if self.stage == 1:
                fight = Fight(self.stage, self.player.room, self.player, [ursoc,], boss = True)
                fight.start()
                print(f'--------------------\nYou have completed Room {self.player.room} of Stage {self.stage}!\n--------------------')
            elif self.stage == 2:
                fight = Fight(self.stage, self.player.room, self.player, [lichking,], boss = True)
                fight.start()
                self.player.inventory.add_item(azarothsheart)
                print(f'--------------------\nYou have completed Room {self.player.room} of Stage {self.stage}!\n--------------------')
            elif self.stage == 3:
                pass
        
        def generate_boss_room(difficulty):
            print('You stand face to face with the floor boss. Only one leaves the floor alive.')
            time.sleep(1)
            if self.stage == 1:
                fight = Fight(self.stage, self.player.room, self.player, [assassin,], boss = True)
                fight.start()
                print(f'--------------------\nYou have completed Room {self.player.room} of Stage {self.stage}!\n--------------------')
            elif self.stage == 2:
                fight = Fight(self.stage, self.player.room, self.player, [righthead, lefthead])
                fight.start()
                time.sleep(2)
                print('The two heads dissolve into the body, with a third emerging shortly after!')
                fight = Fight(self.stage, self.player.room, self.player, [vaelgrath,], boss = True)
                fight.start()
                print(f'--------------------\nYou have completed Room {self.player.room} of Stage {self.stage}!\n--------------------')
            elif self.stage == 3:
                pass

        if room == 'library':
            generate_library_room(difficulty)
        elif room == 'chest':
            generate_chest_room(difficulty)
        elif room == ['enemy', 1]:
            generate_enemy1_room(difficulty)
        elif room == ['enemy', 2]:
            generate_enemy2_room(difficulty)
        elif room == 'miniboss':
            generate_miniboss_room(difficulty)
        elif room == 'boss':
            generate_boss_room(difficulty)
        else:
            raise NameError('No such room exists!')