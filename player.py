import pygame.mouse, math
from object import Object
from particlesystem import ParticleSystem
class Player(Object):
	swap_point_limit = 5
	

	def __init__(self, xPos, yPos, state):
		Object.__init__(self, xPos, yPos, 60, 60)
		self.state = state
		self.color = (255, 0, 0)
		self.state_swap_points = [0, 0, 0]
		_dx, _dy = self.dimension
		self.particle_sys = ParticleSystem(xPos, yPos, _dx, _dy)

	def update(self):
		mouseChange = pygame.mouse.get_rel()
		x, y = mouseChange
		x = pow(x, 2)
		y = pow(y, 2)
		mag = math.sqrt(x + y)
		self.update_state(mag)
		
		#Update particle system's position
		self.particle_sys.x_position = self.x_position
		self.particle_sys.y_position = self.y_position

		#Update particle system
		self.particle_sys.update(self.state)

	def is_colliding(self, object):
		if(object == self): return false
		_collided = False
		_collided = self.particle_sys.resolve_collisions(object)
		if(not _collided):
			_collided = Object.is_colliding(self, object)
		return _collided
		
		
	def push_left(self, _trans):
		Object.push_left(self, _trans)
		self.particle_sys.push_left(_trans)

	def update_state(self, mag):
		if(mag == 0):
			self.state_swap_points[0] += 1
			if(self.state_swap_points[0] >= self.swap_point_limit):
				self.state = 'solid'
				self.color = (255, 0, 0)
				self.state_swap_points[0] = 0
				self.state_swap_points[1] = 0
				self.state_swap_points[2] = 0
		elif(mag < 50):
			self.state_swap_points[1] += 1
			if(self.state_swap_points[1] >= self.swap_point_limit):
				self.state = 'liquid'
				self.color = (0, 0, 255)
				self.state_swap_points[0] = 0
				self.state_swap_points[1] = 0
				self.state_swap_points[2] = 0
		else:
			self.state_swap_points[2] += 1
			if(self.state_swap_points[2] >= self.swap_point_limit):
				self.state = 'gas'
				self.color = (255, 255, 255)
				self.state_swap_points[0] = 0
				self.state_swap_points[1] = 0
				self.state_swap_points[2] = 0

	def draw(self, _screen):
		#Object.draw(self, _screen)
		self.particle_sys.draw(_screen)
