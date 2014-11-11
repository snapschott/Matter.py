import pygame.display, pygame.time, pygame.event, math, sys
from itertools import ifilter
from random import randint
from player import Player
from obstacle import Obstacle


class MatterGame:

	def __init__(self):
		#self.screen = pygame.display.set_mode((1024, 768))
		self.screen = pygame.display.get_surface()
		self.clock = pygame.time.Clock()
		self.camera_translation = 0
		self.spawn_rate = 300
		self.spawn_timer = 0
		self.player = Player(self.screen.get_width() / 2, self.screen.get_height() / 2, 'solid')
		self.objects = []
		self.objects.append(self.player)
		self.running = 1
		self.add_random_obstacle()
		self.paused = False

	#Adds a random obstacle to self.obstacles
	def add_random_obstacle(self):
		#Select random allowed state for obstacle
		_rnd_state_index = randint(0, 3)
		_rnd_state = None
		if(_rnd_state_index == 0): _rnd_state = 'solid'
		elif(_rnd_state_index == 1): _rnd_state = 'liquid'
		else: _rnd_state = 'gas'

		#Create obstacle
		_obstacle = Obstacle(self.screen.get_width() + self.camera_translation, 0, 200, self.screen.get_height(), _rnd_state)
		#Add obstacle to list of objects
		self.objects.append(_obstacle)


	#Runs the game
	def run(self):
		while self.running:			#Start the game loop
			self.clock.tick(30)		#Allow game to run at a maximum of 30 loops per second
			
			#Input management
			#Keyboard
			for event in pygame.event.get():
				if hasattr(event, 'key'):
					if event.key == pygame.K_ESCAPE: self.running = 0


		        #Update game logic
			#Spawn obstacles
			self.spawn_timer += 1
			if(self.spawn_timer >= self.spawn_rate):
				self.spawn_timer = 0
				self.add_random_obstacle()
	
	

			#Update objects
			for _object in self.objects:
				_object.update()
				#Collision detection for player
				if(self.player.is_colliding(_object)):
					#If player is colliding with something, set player
					#Back to previous position
					self.player.x_position = self.player.prev_position[0]
					self.player.y_position = self.player.prev_position[1]


			#Screen bounds check
			self.objects[:] = ifilter(lambda e: self.is_on_screen(e), self.objects)
			if(self.player not in self.objects):
				print("Game over")
				self.running = 0

		        #Draw Code
			for _object in self.objects:
				_object.draw(self.screen, self.camera_translation)
			pygame.display.update()					#Update display

			#Slide camera
			self.camera_translation += 3

	#returns whether or not the object is to the right of the left side of the screen.
	#True if the object has not fallen off the screen
	#False if the object has falled off the screen
	def is_on_screen(self, _object):
		return (_object.x_position + _object.dimension[0] >self.camera_translation)

	def read_file(self, file_path):
		pass

	def write_file(self, file_path):
		pass
	


#Program starts here if this file is ran from command line
def main():
	pygame.init()
	pygame.display.set_mode((0, 0), pygame.RESIZABLE)
	game = MatterGame()
	game.run()
	print("closing")

#In case of name mangling
if __name__ == '__main__':
	main()
