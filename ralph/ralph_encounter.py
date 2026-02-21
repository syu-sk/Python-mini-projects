import copy
import time
import random
if __name__ == '__main__':
    raise NameError('This is the enemy encounter implementation for ralph.py -- It is not meant to be run by itself')

#loot tables are already tagged to enemy instances, which have been imported to stage
class Fight:

	def __init__(self, stage, room, player, enemies, boss = False):

		self.player = player
		self.enemies = enemies
		self.is_bossfight = boss            #key for whether ability is used

		'''Turn Handling'''
		self.speedcomp = [0, 0]             
		self.turnhistory = [None, None]     #used along with speedcomp to determine turn order. [player, enemy]. to reset upon fight completion

		'''Labelling'''
		self.turn = 1
		self.stage = stage
		self.room = room
	
	def start(self):

		print(f'--------------------\nFLOOR {self.stage} | ROOM {self.room}\n--------------------')                 #Header

		while self.enemies:
			self.current_enemy = copy.deepcopy(self.enemies[-1])    
			#get enemy (if none left this block does not even execute)
			#uses a copy of the enemy instance so the original instance's attributes are not modified

			'''Enemy Description'''
			print(f'Enemy: {self.current_enemy.name}\n\'{self.current_enemy.desc}\'\n--------------------')
			time.sleep(2)
			print(f'Damage: {self.current_enemy.atk}\nHP: {self.current_enemy.hp}\nDefense: {self.current_enemy.defense}\nSpeed: {self.current_enemy.speed}\n')
			if self.is_bossfight:
				print(f'Ability: {self.current_enemy.ability.name}\n{self.current_enemy.ability.desc}')
			print('--------------------')
			print(f'Enemies: [{len(self.enemies)}] remaining')

			'''Fight begins'''
			self.next_turn()
			while True:
				time.sleep(1)
				print(f'--------------------\nTurn {self.turn}\n--------------------')
				time.sleep(1)
				print('--------------------\nStatus:')
				for status, duration in self.player.statuses.items():
					if status.is_effect:
						print(f'--> {status.effect_name}: {duration} turns')
				print(f'HP: {self.player.hp} / {self.player.max_hp}\nMP: {self.player.mp} / {self.player.max_mp}\n\n[{self.current_enemy.name}]\nHP: {self.current_enemy.hp}\nDamage: {self.current_enemy.atk}\nDefense: {self.current_enemy.defense}\nSpeed: {self.current_enemy.speed}\n--------------------')
				time.sleep(1)

				if self.turnhistory[0] == 'player':
					decision = input(f'--------------------\n[INPUT] What will you do?\n1. Attack\n2. Weapon Ability\n3. Armor Ability\n4. Inventory\n--------------------\nAction: ')

					if decision.lower() in ['attack', 'atk'] or decision == '1':
						if not self.player.inventory.is_holding:
							print('You are not holding a weapon!')
							continue
						self.current_enemy.take_damage(self.player.dealt_damage)
						print(f'You strike {self.current_enemy.name} with your {self.player.inventory.is_holding.item_name}!')
						time.sleep(2)
						print(f'{self.current_enemy.name} has {self.current_enemy.hp} HP remaining!')
						time.sleep(1)

						'''On hit abilities'''
						if self.player.ability and self.player.ability.triggers_on_hit and self.player.ability.hits_left > 0:
							if not self.player.ability.is_active and self.player.mp < self.player.ability.mp_cost:
								print(f'Not enough mana to use {self.player.ability.name}.')
							else:
								self.player.ability.on_hit_use(user = self.player, target = self.current_enemy)
								time.sleep(2)
							if self.player.ability.is_active:
								self.player.ability.hits_left -= 1
						if self.player.armor_ability and self.player.armor_ability.triggers_on_hit and self.player.armor_ability.hits_left > 0:
							if not self.player.armor_ability.is_active and self.player.mp < self.player.armor_ability.mp_cost:
								print(f'Not enough mana to use {self.player.armor_ability.name}.')
							else:
								self.player.armor_ability.on_hit_use(user = self.player, target = self.current_enemy)
								time.sleep(2)
							if self.player.armor_ability.is_active:
								self.player.armor_ability.hits_left -= 1

					elif decision.lower() == 'weapon ability' or decision == '2':

						if self.player.ability and self.player.ability.is_usable and self.player.mp >= self.player.ability.mp_cost:
							self.player.ability.use(user = self.player, target = self.current_enemy)
							time.sleep(2)
							if self.player.ability.triggers_on_hit:
								self.player.ability.hits_left = self.player.ability.hits
								print(f'{self.player.ability.name} has been used! Its effect will last for {self.player.ability.hits} turns!')
								time.sleep(2)
							if not self.player.ability.spends_turn:
								continue
						
						else:
							if not self.player.ability:
								print(f'{self.player.inventory.is_holding.item_name} does not have an ability.')
								time.sleep(1)
								continue
							elif not self.player.ability.is_active:
								print(f'{self.player.inventory.is_holding.item_name} has a passive ability. It cannot be used actively during a fight.')
								time.sleep(1)
								continue
							elif self.player.ability.turns_till_use != 0:
								print(f'{self.player.inventory.is_holding.item_name} is still on ability cooldown [{self.player.ability.turns_till_use} turns remaining].')
								time.sleep(1)
								continue
							elif self.player.mp < self.player.ability.mp_cost:
								print('Not enough mp!')
								time.sleep(1)
								continue
					
					elif decision.lower() == 'armor ability' or decision == '3':

						if self.player.armor_ability and self.player.armor_ability.is_usable and self.player.mp >= self.player.armor_ability.mp_cost:
							self.player.armor_ability.use(user = self.player)
							time.sleep(2)
							if self.player.armor_ability.triggers_on_hit:
								self.player.armor_ability.hits_left = self.player.armor_ability.hits
								print(f'{self.player.armor_ability.name} has been used! Its effect will last for {self.player.armor_ability.hits} turns!')
								time.sleep(2)
							if not self.player.armor_ability.spends_turn:
								continue
						
						else:
							if not self.player.armor_ability:
								print(f'{self.player.inventory.is_wearing.item_name} does not have an ability.')
								time.sleep(2)
								continue
							elif not self.player.armor_ability.is_active:
								print(f'{self.player.inventory.is_wearing.item_name} has a passive ability. It cannot be used actively during a fight.')
								time.sleep(2)
								continue
							elif self.player.armor_ability.turns_till_use != 0:
								print(f'{self.player.inventory.is_wearing.item_name} is still on ability cooldown [{self.player.armor_ability.turns_till_use} turns remaining].')
								time.sleep(2)
								continue
							elif self.player.mp < self.player.armor_ability.mp_cost:
								print('Not enough mp!')
								time.sleep(2)
								continue

					elif decision.lower() in ['inventory', 'inv'] or decision == '4':
						print('You choose to open your backpack. You cannot attack anymore this turn.')
						self.player.inventory.get_inv()

					else:
						print('Invalid Input. Either type the action or its index.')
						continue

				elif self.turnhistory[0] == 'enemy':
					if self.current_enemy.ability and self.current_enemy.ability.is_usable:
						'''if effect to self, player.statuses. otherwise current_enemy.statuses'''
						self.current_enemy.ability.message()
						self.current_enemy.ability.use(user = self.current_enemy, target = self.player)
						time.sleep(2)
						if self.current_enemy.ability.triggers_on_hit:
							self.current_enemy.ability.hits_left = self.current_enemy.ability.hits
							print(f'{self.current_enemy.ability.name} has been used! Its effect will last for {self.current_enemy.ability.hits} turns!')
							time.sleep(2)
						
					if not self.is_bossfight or not self.current_enemy.ability or not self.current_enemy.ability.spends_turn:
						time.sleep(1)
						self.player.take_damage(self.current_enemy.dealt_damage)
						print(f'{self.current_enemy.name} strikes you!')
						time.sleep(2)
						print(f'You have {self.player.hp} HP remaining!')
						time.sleep(1)

						'''Enemy on hit abilities'''
						if self.is_bossfight and self.current_enemy.ability.triggers_on_hit and self.current_enemy.ability.hits_left > 0:
							if self.current_enemy.ability.is_effect:
								self.current_enemy.ability.on_hit_use(user = self.current_enemy, target = self.player)
								time.sleep(2)
							if self.current_enemy.ability.is_active:
								self.current_enemy.ability.hits_left -= 1
						'''On struck abilities -- Armor'''
						if self.player.inventory.is_wearing and self.player.armor_ability and self.player.armor_ability.triggers_on_struck:
							self.player.armor_ability.use(user = self.player, target = self.current_enemy)
							time.sleep(2)
							if self.player.armor_ability.is_active:
								self.player.armor_ability.hits_left -= 1
				
				self.turn_end()			#handles cooldown ticking, status ticking, player death, loot distribution
				self.next_turn()        #works alongside turnhistory to determine player input or enemy input -- ive since moved it here so the ability continue statements work
				current_enemy_statuses = list([key.effect_name, value] for key, value in self.current_enemy.statuses.items())
				# print(f'''[DEBUG]\nenemy.statuses: {current_enemy_statuses}\nspeedcomp: [player: {self.speedcomp[0]}, enemy: {self.speedcomp[1]}]\nsouls: {self.player.inventory.is_holding.souls if self.player.inventory.is_holding.item_name == 'Glacierbrand' else 'NA'}''')

				if not self.current_enemy.is_alive:
					#one-off interaction with item Glacierbrand
					try:
						self.player.inventory.is_holding.souls += 1
					except AttributeError:
						pass
					
					#next enemy procedures -- loot distribution handled via turn_end()
					self.speedcomp = [0, 0]
					self.turnhistory = [None, None]
					self.turn = 1
					self.enemies.pop()
					break
		
		self.player.statuses = dict()
		self.player.ability.turns_till_use = 0
		print(f'You have defeated all enemies in Room {self.room}!')

	def turn_end(self):		#this function is meant to be run. hence it doesnt have any return value, it just exists as a block of code to access the next turn
		if not self.inventory.is_holding:		#one-off exception for vaelgrath boss fight.
			pass

		'''Passive mp regen'''
		self.player.mp += 0.5

		'''Reduce all cooldowns by 1'''
		if self.player.ability.turns_till_use > 0:
			self.player.ability.turns_till_use -= 1
		if self.current_enemy.ability and self.current_enemy.ability.turns_till_use > 0:
			self.current_enemy.ability.turns_till_use -= 1
		self.player.status_tick()
		self.current_enemy.status_tick()
		self.turn += 1

		'''End of turn checks'''
		if not self.player.is_alive:                  #fight ends, move onto next enemy or death screen if player dies
			self.player.death()
			#death screen
		elif not self.current_enemy.is_alive:
			#loot distribution
			loot = self.current_enemy.loot.drop()
			print(f'You have defeated {self.current_enemy.name}!')
			time.sleep(1)

			#check for xp, money drop
			if isinstance(loot[0], int) and isinstance(loot[1], int):
				print(f'Obtained {loot[0]} xp and {loot[1]} money!')
				self.player.xp += loot[0]
				self.player.inventory.money += loot[1]

				#any additional drops (minibosses, bosses etc.)
				try:
					for item in loot[2:]:
						print(f'Obtained {item.item_name}!')
						time.sleep(1)
						self.player.inventory.add_item(item)
						time.sleep(1)
				except IndexError:
					pass
			
			#check for chest drop
			else:
				for item in loot:
					print(f'Obtained {item.item_name}!')
					self.player.inventory.add_item(item)
		
		'''Exclusive turn end countdown for stage 2 final boss'''
		if self.current_enemy.name == 'Vael\'Grath, The Great Dragon' and self.current_enemy.ability.calamity_countdown > 0:
			self.current_enemy.ability.calamity_countdown -= 1
			print(f'Calamity arrives in {self.current_enemy.ability.calamity_countdown} turns...')
	

	def next_turn(self):	#this function is meant to be run. hence it doesnt have any return value, it just exists as a block of code to access the next turn
		'''
		Turn Implementation
		- First turn exception -- let player go first always
		- Every turn after that -- if A goes this turn, B has its speedcomp increased. Then at the start of the turn, whoever has higher speedcomp goes first. This allows speed to allow one side to cut turns.
		- When cutting turns, a message should be played to reduce confusion
		- When speedcomps are the same, random person goes first.
		'''

		if not self.turnhistory[0]:                     #default start player
			self.turnhistory[0] = 'player'
		else:                                           #updating speeds
			if self.turnhistory[0] == 'player': 
				self.speedcomp[1] += self.current_enemy.speed
			elif self.turnhistory[0] == 'enemy':
				self.speedcomp[0] += self.player.speed
		
			self.turnhistory[1] = self.turnhistory[0]       #shifting history back to make room for new turn at [0]
			if self.speedcomp[0] > self.speedcomp[1]:       #adding turn holder to [0]
				self.turnhistory[0] = 'player'
			elif self.speedcomp[0] < self.speedcomp[1]:
				self.turnhistory[0] = 'enemy'
			else: 											#same speed
				self.turnhistory[0] = random.choice(['player', 'enemy'])
			
			if self.turnhistory[0] == self.turnhistory[1]:  #custom messages
				if 'player' in self.turnhistory:
					print('[EXTRA TURN] Your agility leaves your opponent in confusion, allowing you one more opening for a hit.')
					time.sleep(2)
				else:
					print(f'Your enemy darts around too fast for your eyes to follow. You are unable to react as {self.current_enemy.name} strikes you again!')
					time.sleep(2)