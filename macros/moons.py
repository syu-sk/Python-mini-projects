import system.lib.minescript as m
from system.lib.minescript import EventQueue, EventType
from minescript_plus import Util, Inventory, Screen
import smooth_look
import asyncio
import lib_nbt
import time
import threading
import random
import sys
import requests

TOKEN = #BOTTOKEN#
CHAT_ID = #CHAT_ID#
status = [None, None, None, None]	#working, checker, timer, multi-script
stored = None

class Worker():

	@property
	def is_running(self):
		return self in status

class Checker(Worker):

	name = 'CHECKER'
	freq = 0.05

	async def start(self):

		'''Initialisation'''
		global stored
		ori = m.player_orientation()
		pos = m.player_position()
		status[1] = self
		m.echo('§a§l----------\n[CHECKER] Checker is online\n----------')
		ori_trigger = False
		pos_trigger = False
		players_nearby = False
		captcha = False

		while status[0] and self.is_running:

			#orientation
			ori_temp = m.player_orientation()
			if status[0]:
				shifted = any([abs(ori_temp[i] - ori[i]) > status[0].ori_threshold[i] for i in range(2)])
				if shifted:
					m.echo(f'§c§l----------\n[CHECKER] Change in orientation detected...\nTerminating [{status[0].name}]\n----------')
					Util.play_sound(sound = Util.get_soundevents().ANVIL_PLACE, sound_source = Util.get_soundsource().MASTER)
					ori_trigger = True
			ori = ori_temp

			#player nearby
			if len(m.players()) > 1:
				if status[0].name not in ['SKYLER','BURTON']:
					plist = [player.name for player in m.players()]
					m.echo(f'§c§l----------\n[CHECKER] Player nearby detected...\nTerminating [{status[0].name}]\n----------')
					m.echo(f'§c§lPlayers Detected:\n§c{[i for i in plist[1:]]}')
					Util.play_sound(sound = Util.get_soundevents().END_PORTAL_SPAWN, sound_source = Util.get_soundsource().MASTER)
					players_nearby = True
					try:
						tele_send_message('Player detected!')
						m.echo('§a§l[CHECKER] Alert Sent!')
					except Exception as e:
						m.echo(f'§c§l[CHECKER] Failed to send alert: {e}')

			#position
			pos_temp = m.player_position()
			if status[0]:
				moved = any([abs(pos_temp[i] - pos[i]) > status[0].pos_threshold[i] for i in range(3)])
				if moved:
					m.echo(f'§c§l----------\n[CHECKER] Change in position detected...\nTerminating [{status[0].name}]\n----------')
					Util.play_sound(sound = Util.get_soundevents().ANVIL_PLACE, sound_source = Util.get_soundsource().MASTER)
					pos_trigger = True
			pos = pos_temp

			await asyncio.sleep(self.freq)

			#captcha -- this needs to be the last check, otherwise the loop exits without throwing the captcha exception
			if m.player_hand_items().main_hand and m.player_hand_items().main_hand['item'] == 'minecraft:filled_map':
				m.echo(f'§c§l----------\n[CHECKER] Captcha detected...\nTerminating [{status[0].name}]\n----------')
				Util.play_sound(sound = Util.get_soundevents().ANVIL_PLACE, sound_source = Util.get_soundsource().MASTER)
				captcha = True
				try:
					tele_send_message('Captcha detected!')
				except Exception as e:
					m.echo(f'§c§l[CHECKER] Failed to send alert: §c{e}')
				m.echo('§a§l[CHECKER] Alert Sent!')

			if any([ori_trigger, pos_trigger, players_nearby, captcha]):
				stored = status[0]
				status[0], status[1], status[3] = None, None, None

		m.player_press_attack(False)
		m.player_press_forward(False)
		m.player_press_backward(False)
		m.player_press_right(False)
		m.player_press_left(False)
		m.player_press_jump(False)
		m.player_press_use(False)
		m.player_press_sprint(False)
		m.echo(f'§c§l[CHECKER] Checker terminated. Stored [{stored.name}]')
	
	def end(self):
		#shouldnt ever need to use this
		status[1] = None

class George(Worker):

	name = 'GEORGE'
	pos_threshold = [0.2, 0.2, 0.2]
	ori_threshold = [0.2, 0.2]
	sword_slot = 0
	
	async def start(self):
		status[0] = self
		m.echo('§6§l----------\n[GEORGE] Grinding Starting...\n[stop] to terminate\n----------')
		await asyncio.sleep(1)

		#m.player_inventory_select_slot(self.sword_slot)
		while self.is_running:
			if not m.player_get_targeted_entity(max_distance=5):
				await asyncio.sleep(2)
				continue
			m.player_press_attack(True)
			m.player_press_attack(False)
			await asyncio.sleep(random.uniform(0.05,0.1))

		status[0], status[1] = None, None
		m.echo('§6§l[GEORGE] terminated.')

class Mikey(Worker):

	name = 'MIKEY'
	pos_threshold = [27, 0.2, 1]
	ori_threshold = [0.2, 0.2]
	pickaxe_slot = 1

	async def start(self):
		status[0] = self
		m.echo('§6§l----------\n[MIKEY] Mining Starting...\n[stop] to terminate\n----------')
		if not 468 < m.player_position()[2] < 469:
			m.execute('/home mine')
		await asyncio.sleep(1)

		m.player_set_orientation(-90,-90)
		m.player_inventory_select_slot(self.pickaxe_slot)
		await asyncio.sleep(0.5)
		while self.is_running:
			m.player_press_attack(True)
			m.player_press_forward(True)
			await asyncio.sleep(1)

		m.player_press_attack(False)
		m.player_press_forward(False)
		status[0], status[1] = None, None
		m.echo('§6§l[MIKEY] terminated.')

class Melany(Worker):
	
	name = 'MELANY'
	pos_threshold = [200, 6.5, 20]
	ori_threshold = [0.2, 0.2]
	axe_slot = 3
	farm_end_time = 0.5

	async def start(self):
		status[0] = self
		m.echo('§6§l----------\n[MELANY] Melon Farming Starting...\n[stop] to terminate\n----------')
		if m.player_position()[2] > 443 or m.player_position()[0] < 525:
			m.execute('/home melon')
		await asyncio.sleep(1)
		m.player_set_orientation(yaw = 177, pitch = 39.0)
		m.player_inventory_select_slot(self.axe_slot)
		await asyncio.sleep(1)
		m.player_press_right(True)
		m.player_press_attack(True)

		pos = m.player_position()
		while self.is_running:
			await asyncio.sleep(0.3)
			if m.player_position() == pos:				#stationary check
				m.echo('§a§l[MELANY] End of Farm!')
				break
			pos = m.player_position()
			
		m.player_press_right(False)
		m.player_press_attack(False)
		status[0], status[1] = None, None
		m.echo('§6§l[MELANY] terminated.')

class Wilbur(Worker):
	
	name = 'WILBUR'
	pos_threshold = [5, 3, 100]
	ori_threshold = [360, 360]

	pos_check_freq = 0.1	#something low enough to trigger semi-instantaneously, but not so low such that it runs too fast
	builder_wand_slot = 8
	tool_slot = 7

	def __init__(self, iterations):
		self.iterations = iterations	#back and forth
		self.direction = True
		self.completed = 0

	async def start(self):
		status[0] = self
		m.echo('§6§l----------\n[WILBUR] Woodcutting Starting...\n[stop] to terminate\n----------')
		m.execute('/home woodcutting')
		m.player_inventory_select_slot(self.builder_wand_slot)
		await asyncio.sleep(1)
		m.player_set_orientation(-90, -59)
		await asyncio.sleep(1)

		for _ in range(self.iterations):
			'''Building --- Platforms are at y=67 and y=65 respectively'''
			m.player_press_use(True)
			m.player_press_left(True)
			while m.player_position()[1] > 66:			#start breaking
				if not self.is_running:
					break
				await asyncio.sleep(self.pos_check_freq)
			if not self.is_running:
				break
			m.player_press_left(False)
			m.player_press_use(False)
			m.player_inventory_select_slot(self.tool_slot)
			smooth_look.look(-90, -90)
			m.player_press_attack(True)
			m.player_press_left(True)
			while m.player_position()[1] < 66:
				if not self.is_running:
					break
				await asyncio.sleep(self.pos_check_freq)
			if not self.is_running:
				break
			m.player_press_left(False)
			m.player_press_attack(False)
			self.completed += 1
			m.echo(f'§a§l[WILBUR] Finished Iteration! [{self.completed}]')
			m.player_inventory_select_slot(self.builder_wand_slot)
			smooth_look.look(-90, -59)

		status[0], status[1] = None, None
		m.echo('§6§l[WILBUR] terminated.\n----------')

class Fiona(Worker):

	name = 'FIONA'
	pos_threshold = [0.2, 0.2, 0.2]
	ori_threshold = [35, 12]
	fishing_rod_slot = 6
	sell_every = 8
	water_surface = 79.9375
	too_low = 0.45	#blocks

	def __init__(self):
		self.fished = 0
		self.fishing_site = True

	async def start(self):

		def find_bobber():
			for entity in m.entities():
				if "fishing_bobber" in entity.type.lower():
					return entity
			return None

		def random_look():
			c_yaw, c_pitch = m.player_orientation()
			while True:
				d_yaw, d_pitch = random.uniform(-30, 30), random.uniform(-3, 3)
				if -90 <= c_yaw + d_yaw <= 90 and 7 <= c_pitch + d_pitch <= 18:		#ranges
					f_yaw, f_pitch = c_yaw + d_yaw, c_pitch + d_pitch
					break
			smooth_look.look(f_yaw, f_pitch)

		status[0] = self
		m.echo('§6§l----------\n[FIONA] Fishing Starting...\nType [stop] to terminate\n----------')
		m.player_inventory_select_slot(self.fishing_rod_slot)
		bobber = None
		smooth_look.look(0, 10)
		while self.is_running:
			bobber = find_bobber()
			if not bobber:
				random_look()
				m.player_press_use(True)
				m.player_press_use(False)
				await asyncio.sleep(2)
				continue

			bobber_pos = bobber.position[1]
			if abs(self.water_surface - bobber_pos) > self.too_low:
				m.player_press_use(True)
				m.player_press_use(False)
				await asyncio.sleep(0.35)
				bobber = None
				self.fished += 1
				m.echo(f'§a§l[FIONA] Fish Caught! [{self.fished}]')
			await asyncio.sleep(0.05)

		status[0], status[1] = None, None
		m.echo('§6§l[FIONA] terminated.')

class Carter(Worker):

	name = 'CARTER'
	pos_threshold = [0.2, 0.2, 0.2]
	ori_threshold = [0.2, 0.2]

	async def start(self):
		status[0] = self
		m.echo('§6§l----------\n[CARTER] Crossbow Starting...\n[stop] to terminate\n----------')

		#m.execute('/home crossbow')
		#smooth_look.look(0, -3.2)

		while self.is_running:
			m.player_press_use(True)
			await asyncio.sleep(0.15)
			m.player_press_use(False)

			await asyncio.sleep(0.1)
		
		status[0], status[1] = None, None
		m.echo('§6§l[CARTER] terminated.')

class Skyler(Worker):

	name = 'SKYLER'
	pos_threshold = [3, 10, 3]
	ori_threshold = [361, 361]

	async def start(self):
		status[0] = self
		m.echo('§6§l----------\n[SKYLER] Slaying Starting...\n[stop] to terminate\n----------')

		async def find_gk():
			while self.is_running:
				for entity in m.entities(max_distance = 15):
					if entity.name == 'Slime':
						return entity
				m.echo('§6§l[SKYLER] Target not found, scanning...')
				origin = m.player_orientation()
				for i in range(1,4):	#scans in multiples of +-10 yaw from 10 to 30
					m.player_set_orientation(origin[0] + 10*i, 5)
					for entity in m.entities(max_distance = 15):
						if entity.name == 'Slime':
							return entity
					await asyncio.sleep(0.35)
					m.player_set_orientation(origin[0], 5)
					for entity in m.entities(max_distance = 15):
						if entity.name == 'Slime':
							return entity
					await asyncio.sleep(0.35)
					m.player_set_orientation(origin[0] - 10*i, 5)
					for entity in m.entities(max_distance = 15):
						if entity.name == 'Slime':
							return entity
					await asyncio.sleep(0.35)
					m.player_set_orientation(origin[0], 5)
					for entity in m.entities(max_distance = 15):
						if entity.name == 'Slime':
							return entity
					await asyncio.sleep(0.35)
		
		def distance_to(point):
			p_x, p_y, p_z = m.player_position()[0], m.player_position()[1], m.player_position()[2]
			e_x, e_y, e_z = point[0], point[1], point[2]
			distance = ((p_x - e_x) ** 2 + (p_y - e_y) ** 2 + (p_z - e_z) ** 2) ** 0.5
			return distance

		while self.is_running:
			golden_knight = await find_gk()
			to_hit_coordinates = [golden_knight.position[0], 25.5, golden_knight.position[2]]

			smooth_look.look_at(to_hit_coordinates[0], to_hit_coordinates[1], to_hit_coordinates[2])
			m.player_press_attack(True)
			await asyncio.sleep(0.05)
			m.player_press_attack(False)
			await asyncio.sleep(0.20)

		status[0], status[1] = None, None
		m.echo('§6§l[SKYLER] terminated.')

class Burton(Worker):

	name = 'BURTON'
	pos_threshold = [0.2, 0.2, 0.2]
	ori_threshold = [360, 360]
	iterations = 0
	killed = 0
	
	async def start(self):
		status[0] = self
		m.echo('§6§l----------\n[BURTON] Blasting Starting...\n[stop] to terminate\n----------')

		while self.is_running:
			m.echo(f'§6§l[BURTON] Iteration [{self.iterations}]')
			if len(m.entities(max_distance=30)) < 20:
				m.player_press_use(True)
				await asyncio.sleep(0.05)
				m.player_press_use(False)
				m.echo('§6Pausing...')
				await asyncio.sleep(5)
				continue
			for entity in m.entities(max_distance=30, sort='nearest'):
				if 'Slime' in entity.name and entity.position[1] < 60:
					jitter = random.choices([0,1,-1],[95,2.5,2.5])
					var = random.uniform(-0.2,0.2)
					if jitter[0] != 0:
						m.echo('§6Jitter!')
						smooth_look.look_at(entity.position[0]+jitter[0], entity.position[1]-0.75, entity.position[2])
					smooth_look.look_at(entity.position[0]+var, entity.position[1]-0.75+var, entity.position[2]+var)
					m.player_press_use(True)
					await asyncio.sleep(0.05)
					m.player_press_use(False)
					self.killed += 1
				if not self.is_running:
					break
				await asyncio.sleep(0.05)
			if not self.is_running:
				break
			if self.iterations % 5 == 0:
				plist = [player.name for player in m.players()]
				m.echo(f'§d§lPlayers Detected:\n§d{[i for i in plist[1:]]}')
				m.echo(f'§d§lKilled {self.killed} in {self.iterations} iterations')
			self.iterations += 1
		
		m.echo('§6§l[BURTON] terminated')

class Clove(Worker):

	name = 'CLOVE'
	events = {'Manapond': [1059, 1559, 1859, 2259], 'Boss': [1229, 1429, 1629, 1829, 2029, 2229, 29], 'LPS': [2157,], 'Island Wars': [1]}
	refresh = 1			#seconds
	display_time = 15	#display time when mm is 30

	async def start(self):
		'''This script is only reporting time, no player input thus no real need for checker. It should be up all the asyncio.'''
		status[2] = self
		m.echo('§a§l----------\n[CLOVE] Clove is online\n----------')
		while self.is_running:

			curr = time.ctime(time.time())
			hhmm = [i for i in curr.split()[3].split(':')[:-1]]
			int_hhmm = int(''.join(hhmm))

			for event, time_list in self.events.items():
				for event_time in time_list:
					if int_hhmm == event_time:
						m.echo(f'§b§l----------\n[CLOVE] [{event.upper()}] soon!\n----------')
						Util.play_sound(sound = Util.get_soundevents().DRAGON_FIREBALL_EXPLODE, sound_source = Util.get_soundsource().MASTER)
						await asyncio.sleep(60)
			
			if int_hhmm % 100 == self.display_time:
				m.echo(f'§b§l[CLOVE] Time: {str(int_hhmm // 100) + ':' + str(int_hhmm % 100)}')
				await asyncio.sleep(60)
			
			await asyncio.sleep(self.refresh)

		m.echo('§6§l[CLOVE] terminated.')

class Chester(Worker):
	
	name = 'CHESTER'
	ori_threshold = [1, 1]
	pos_threshold = [0.2, 0.2, 0.2]

	async def start(self):
		status[0] = self
		m.echo('§6§l----------\n[CHESTER] Selling...\n[stop] to terminate\n----------')
		m.execute('/home heads')
		await asyncio.sleep(1)

		while self.is_running:

			Inventory.open_targeted_chest()
			await asyncio.sleep(1.3)

			head_slot = Inventory.find_item(item_id='minecraft:player_head', container=True)
			if head_slot is None:
				m.echo('§6§l[CHESTER] No heads left...')
				return
			for i in range(15):
				if i + head_slot > 53:
					break
				Inventory.shift_click_slot(i + head_slot)
				await asyncio.sleep(0.2)
			Screen.close_screen()
			await asyncio.sleep(0.5)

			m.execute('/kilton')
			await asyncio.sleep(0.5)
			Inventory.click_slot(4)
			await asyncio.sleep(0.3)
		
		status[0], status[1] = None, None
		m.echo('§6§l[CHESTER] terminated.')

class Selena(Worker):

	name = 'CHESTER'
	ori_threshold = [1, 1]
	pos_threshold = [1, 5, 1]

	top_y_threshold = 116.1
	bottom_y_threshold = 84.2 #threshold as having a floor would cancel fly

	pos_check_freq = 0.1
	sell_wand_slot = 3

	def __init__(self):
		self.going_up = True

	async def start(self):
		status[0] = self
		m.echo('§6§l----------\n[SELENA] Selling...\n[stop] to terminate\n----------')
		m.execute('/home chests')
		await asyncio.sleep(1)
		m.player_inventory_select_slot(self.sell_wand_slot)

		while self.is_running and m.player_position()[2] > 472:
			if self.going_up:
				m.player_press_jump(True)
				m.player_press_use(True)
			else:
				m.player_press_sneak(True)
				m.player_press_use(True)

			if round(m.player_position()[1], 1) > self.top_y_threshold:
				m.player_press_jump(False)
				m.player_press_use(False)
				m.player_press_left(True)
				await asyncio.sleep(0.5)
				m.player_press_left(False)
				m.player_press_sneak(True)
				m.player_press_use(True)
				await asyncio.sleep(0.3)
				self.going_up = False
			elif round(m.player_position()[1], 1) < self.bottom_y_threshold:
				m.player_press_sneak(False)
				m.player_press_use(False)
				m.player_press_left(True)
				await asyncio.sleep(0.5)
				m.player_press_left(False)
				m.player_press_jump(True)
				m.player_press_use(True)
				await asyncio.sleep(0.3)
				self.going_up = True
			
			await asyncio.sleep(self.pos_check_freq)
		
		m.echo('§a§l----------\n[SELENA] Selling complete! Terminating [SELENA]\n----------')
		m.player_press_sneak(False)
		m.player_press_use(False)
		await asyncio.sleep(1)
		status[0], status[1] = None, None
		m.echo('§6§l[SELENA] terminated')


class Rafaela(Worker):

	name = 'RAFAELA'

	def __init__(self, tasks, loop = False):
		'''
		A multi-job script that switches between scripts.
		- Every 10 mins, do melany.
		- Every iteration of wilbur takes ~1 min. Do 12 iterations per batch.
		- mikey, george and fiona can do any amount of asyncio.
		'''
		self.tasks: list[Worker] = tasks
		self.temp_tasks = tasks		#copy of tasks, to edit whenever a job is done to list what's remaining
		self.loop = loop

	def report_tasks(self):
		m.echo('§6§l----------\n[RAFAELA] Tasks Remaining: ')
		for index, task in enumerate(self.temp_tasks):
			m.echo(f'§6§l[{index + 1}] {task.name}')
		m.echo('§6§l----------')

	def report_current_task(self, task):
		m.echo(f'§a§lCurrent Task: [{task.name}]')
	
	async def start(self):
		status[3] = self
		m.echo('§a§l----------\n[RAFAELA] Rafaela is online\n[stop] to terminate\n----------')
		await asyncio.sleep(1)

		while self.is_running:

			for task in self.tasks:
				m.echo(f'§6§l[RAFAELA] Starting {task.name}...')
				await asyncio.sleep(1)
				asyncio.create_task(task.start())
				await asyncio.sleep(3)
				asyncio.create_task(checker.start())
				report_jobs()

				if status[0].name in ['GEORGE', 'MIKEY', 'FIONA']:
					temp_time = time.ctime(time.time())
					temp_hhmm = int(''.join([i for i in temp_time.split()[3].split(':')[:-1]]))
					finish_time = temp_hhmm + 5
					while temp_hhmm < finish_time and self.is_running:
						# m.echo(f'[DEBUG] {task.name} not done yet...')
						self.report_current_task(task)
						temp_time = time.ctime(time.time())
						temp_hhmm = int(''.join([i for i in temp_time.split()[3].split(':')[:-1]]))
						await asyncio.sleep(30)		#roughly, 5 - 5.5 mins per mining/grinding task
				else:
					while status[0] and self.is_running:
						# m.echo(f'[DEBUG] {task.name} not done yet...')
						self.report_current_task(task)
						await asyncio.sleep(20)		#checks every 20 seconds to see if finite tasks (woodcutting, melon) are done

				if not self.is_running:
					break

				m.echo(f'§a§l[RAFAELA] {task.name} completed!')
				await asyncio.sleep(1)
				m.echo(f'§6§l[RAFAELA] Temporarily pausing [CHECKER] to proceed to next task...')
				status[1] = None
				status[0] = None
				await asyncio.sleep(1)
			
			if self.loop and self.is_running:
				m.echo('§6§l[RAFAELA] Looping...')
				continue
			m.echo('§6§l[RAFAELA] No Tasks remaining, terminating...')
			await asyncio.sleep(0.5)
			break
		m.echo('§6§l[RAFAELA] terminated')


checker = Checker()
george = George()
mikey = Mikey()
melany = Melany()
fiona = Fiona()
wilbur = Wilbur(iterations = 20)
wilbur8 = Wilbur(iterations = 8)
wilbur12 = Wilbur(iterations = 12)
carter = Carter()
skyler = Skyler()
burton = Burton()
chester = Chester()
selena = Selena()
clove = Clove()
rafaela_1 = Rafaela([melany, fiona, mikey, melany, wilbur8, george, melany, wilbur8, george], loop = True)
rafaela_2 = Rafaela([melany, george, fiona], loop = True)
rafaela_3 = Rafaela([melany, wilbur12], loop = True)

workers = {
    'george': george,
    'mikey': mikey,
    'melany': melany,
    'wilbur': wilbur,
    'fiona': fiona,
	'carter': carter,
    'skyler': skyler,
	'burton': burton,
    'chester': chester,
    'selena': selena,
    'rafaela1': rafaela_1,
    'rafaela2': rafaela_2,
	'rafaela3': rafaela_3
}

'''
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''

def tele_send_message(message):		#does through httpx
	url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
	payload = {'chat_id': CHAT_ID, 'message_thread_id': 2, 'text': message}
	response = requests.post(url, json=payload, timeout=5)
def report_jobs():
	m.echo('§6§l----------\nActive Programs:\n')
	for item in status:
		if item is not None:
			m.echo(f'§b--> {item.name}')
	m.echo('§6§l----------')

async def main():
	global stored
	with EventQueue() as eq:
		eq.register_outgoing_chat_interceptor(prefix = 'hi')
		eq.register_outgoing_chat_interceptor(prefix = 'stop')
		eq.register_world_listener()
		eq.register_chat_listener()
		eq.register_key_listener()
		m.echo('§6§l----------\nAvailable Programs:\n--> [GEORGE]\n--> [MIKEY]\n--> [MELANY]\n--> [WILBUR]\n--> [FIONA]\n--> [CARTER]\n--> [SKYLER]\n--> [BURTON]\n--> [CHESTER]\n--> [SELENA]\n--> [RAFAELA1]\n--> [RAFAELA2]\n--> [RAFAELA3]\n----------')
    staff = []

		while True: 
			event = await asyncio.to_thread(eq.get)

			if event.type == EventType.OUTGOING_CHAT_INTERCEPT:
				if event.message.startswith('hi'):
					worker_name = event.message.split(' ')[1]
					if worker_name in workers:
						target_worker = workers[worker_name]
						worker_task = asyncio.create_task(target_worker.start())
						await asyncio.sleep(2.5)
						if not status[1] and worker_name not in ['skyler', 'rafaela1', 'rafaela2', 'rafaela3']:
							checker_task = asyncio.create_task(checker.start())
							m.echo(f'§a[CHECKER] is not active. It will start via [{target_worker.name}].')
							await asyncio.sleep(1)
					if worker_name == 'clove':
						if status[2]:
							m.echo('§a§l[Clove] is already active.')
						else:
							clock_task = asyncio.create_task(clove.start())
					elif worker_name == 'rapunzel':
						pass

					report_jobs()
				elif event.message == 'stop':
					status[0], status[1], status[3] = None, None, None
					worker_task.cancel()
					report_jobs()
				elif event.message == 'stopall':
					status[0], status[1], status[2], status[3] = None, None, None, None
					worker_task.cancel()

			if event.type == EventType.WORLD:
				if event.connected:
					m.echo(f'§6§l----------\nChanged world.\nClosing all active programs.\n----------')
					status[0], status[1], status[3] = None, None, None
					await asyncio.sleep(1)
					if not status[2]:
						m.echo('§a§l----------\n[CLOVE] is not active. It will automatically start.\n----------')
						clock_task = asyncio.create_task(clove.start())
						await asyncio.sleep(1)
					report_jobs()
			if event.type == EventType.CHAT:
				if '->' in event.message and 'You' in event.message:
					'''[Name] -> You [Text]'''
					sender = event.message.split(' ')[0][6:]
					text = ' '.join(event.message.split(' ')[3:])[3:]
					if 'You' not in event.message.split(' ')[0]:
						try:
							m.echo('§b§lDM received!')
							Util.play_sound(sound = Util.get_soundevents().VILLAGER_YES, sound_source = Util.get_soundsource().MASTER)
							tele_send_message(f'DM received!\nSender: {sender}\nText: {text}')
						except Exception as e:
							Util.play_sound(sound = Util.get_soundevents().CONDUIT_ACTIVATE, sound_source = Util.get_soundsource().MASTER)
						if sender in staff:
							Util.play_sound(sound = Util.get_soundevents().GHAST_SCREAM, sound_source = Util.get_soundsource().MASTER)
			if event.type == EventType.KEY:
				if event.key == 295 and event.action == 1:
					m.echo(f'§6§lStop triggered')
					if status[0]:
						stored = status[0]
						m.echo(f'§6§lTerminating [{stored.name}]')
						status[0], status[1], status[3] = None, None, None
					#worker_task.cancel()
					else:
						m.echo('§c§lNo task running, unable to stop.')
				if event.key == 296 and event.action == 1:
					try:
						if not status[0]:
							m.echo(f'§a§lResuming [{stored.name}]...')
							worker_task = asyncio.create_task(stored.start())
							await asyncio.sleep(1)
							if not status[1] and worker_name not in ['skyler', 'rafaela1', 'rafaela2', 'rafaela3']:
								checker_task = asyncio.create_task(checker.start())
								m.echo(f'§a[CHECKER] is not active. It will start via [{target_worker.name}].')
						else:
							m.echo(f'§a§lCurrent Task: [{status[0].name}]')

					except UnboundLocalError:
						m.echo('§c§lNo saved task, unable to resume.')
			await asyncio.sleep(0.05)
	
if __name__ == '__main__':
	asyncio.run(main())
