import pygame.draw, math
from random import randint
from object import Object
class Particle(Object):
	particles_in_system = None
	particle_radius = 10
	max_flee_weight = 1000		#Weight to use if distance away from flee_location is 0

	solid_max_translation = 1
	solid_max_offset = 35
	solid_max_velocity = 30
	solid_max_ind_force = 50
	

	liquid_repel_force = 1
	liquid_max_ind_force = 1.1
	liquid_max_net_force = 6
	liquid_max_velocity = 20
	liquid_containment_force = 8
	liquid_containment_range = 3
	liquid_max_containment_force = 1

	gas_repel_force = 2
	gas_max_ind_force = 2
	gas_max_net_force = 8
	gas_max_velocity = 80
	gas_containment_force = 8
	gas_containment_range = 10
	gas_max_containment_force = 2



	def __init__(self, _xPos, _yPos, _identification):
		Object.__init__(self, _xPos, _yPos, Particle.particle_radius, Particle.particle_radius)
		self.identifier = _identification
		self.row = None
		self.column = None
		self.x_velocity = 0
		self.y_velocity = 0

		#Find row in lattice based on identifier
		_row = self.identifier / 3
		#if(_row < 1) : self.row = 0
		#elif(_row < 2) : self.row = 1
		#else : self.row = 2
		self.row = _row - 1

		#Find column in lattice based on identifier
		self.column = self.identifier % 3
		



	def update(self, _state, _system_position, _system_radius):
		Object.update(self)
		if(_state == 'solid') : 
			self.solid_update(_system_position)
		elif(_state == 'liquid') : 
			self.liquid_update(_system_position, _system_radius)	#TODO: Change from solid_update
			#self.solid_update(_system_position)
		else : 
			#self.solid_update(_system_position)	#TODO: Change from solid)update
			self.gas_update(_system_position, _system_radius)

		self.x_position = int(self.x_position)
		#print(self.x_position)
		self.y_position = int(self.y_position)
		#print(self.y_position)
	
	#Updates a particle in the solid state
	def solid_update(self, _system_position):
		#Find lattice position
		_lattice_x_pos = self.column * Particle.particle_radius * 2
		_lattice_y_pos = self.row * Particle.particle_radius * 2

		_lattice_x_pos += _system_position[0]
		_lattice_y_pos += _system_position[1]

		#print(_lattice_x_pos)
		#print(_lattice_y_pos)

		#IF the particles position is furter than Particle.max_solid_offset from it's lattice position
		#Just seek the lattice position.
		_dist = math.sqrt( (_lattice_x_pos - self.x_position)**2 + (_lattice_y_pos - self.y_position)**2 )
		if(_dist > Particle.solid_max_offset) :
			#Get seek force to seek position in lattice
			_force = self.seek((_lattice_x_pos, _lattice_y_pos))
			
			_force = self.limit_force(_force, Particle.solid_max_ind_force) 

			#Cap incremented velocity
			_inc_velocity = [self.x_velocity + _force[0], self.y_velocity + _force[1]]
			_inc_velocity = self.limit_force(_inc_velocity, Particle.solid_max_velocity)
			

			#assign velocity
			self.x_velocity = _inc_velocity[0]
			self.y_velocity = _inc_velocity[1]

		


			#Translate position by velocity
			self.x_position += (self.x_velocity)
			self.y_position += (self.y_velocity)
		#else, particle is in correct lattice position and should just vibrate
		else :
			#Snap to lattice position
			self.x_position = _lattice_x_pos
			self.y_position = _lattice_y_pos

			#First vibrate and translate
			_x_vib_trans = randint(-Particle.solid_max_translation, Particle.solid_max_translation)
			_y_vib_trans = randint(-Particle.solid_max_translation, Particle.solid_max_translation)
			self.x_position += (_x_vib_trans)
			self.y_position += (_y_vib_trans)

			#if(not self.x_velocity == 0): self.x_velocity = 0
			#if(not self.y_velocity == 0): self.y_velocity = 0

		#Set color for solid color
		self.color = (255, 0, 0)

	#Updates a particle in liquid state: Unfinished
	def liquid_update(self, _system_position, _system_radius):
		#Get total flee force from all other particles in system
		_net_force = [0, 0]

		for particle in Particle.particles_in_system:
			if(not particle == self):
				_force_inc = self.flee((particle.x_position, particle.y_position))
				_force_inc = self.limit_force(_force_inc, Particle.liquid_max_ind_force)
				_force_inc[0] *= Particle.liquid_repel_force
				_force_inc[1] *= Particle.liquid_repel_force
				

				
				_net_force[0] += _force_inc[0]
				_net_force[1] += _force_inc[1]

		#Limit net force
		_net_force = self.limit_force(_net_force, Particle.liquid_max_net_force)

		#Get containment force of system
		_containment_force = self.contain(
				(_system_position[0] + _system_radius, _system_position[1] + _system_radius), 
				_system_radius,
				Particle.liquid_containment_range)

		#Limit the containment force by the maximum possible individual force
		_containment_force = self.limit_force(_containment_force, Particle.liquid_max_containment_force)

		#Scale containment force by Particle constant
		_containment_force[0] *= Particle.liquid_containment_force
		_containment_force[1] *= Particle.liquid_containment_force


		#increment net force by containment force of system
		_net_force[0] += _containment_force[0]
		_net_force[1] += _containment_force[1]

		#Increment new velocity by net force
		_velocity = [self.x_velocity + _net_force[0], self.y_velocity + _net_force[1]]

		#Cap velocity
		_velocity = self.limit_force(_velocity, Particle.liquid_max_velocity)
		
		#Increment velocity by net force
		self.x_velocity = _velocity[0]
		self.y_velocity = _velocity[1]

		#increment position by velocity
		self.x_position += math.floor(self.x_velocity)
		self.y_position += math.floor(self.y_velocity)

		self.color = (0, 0, 255)




	#Updates a particle in gas state: Unfinished
	def gas_update(self, _system_position, _system_radius):
		#Get total flee fource from all other particles in system
		_net_force = [0, 0]

		for particle in Particle.particles_in_system:
			if(not particle == self):
				#get this particles flee force
				_force_inc = self.flee((particle.x_position, particle.y_position))
				
				#limit it
				_force_inc = self.limit_force(_force_inc, Particle.gas_max_ind_force)
				
				#Scale it by the force weight for this state
				_force_inc[0] *= Particle.gas_repel_force
				_force_inc[1] *= Particle.gas_repel_force
				
				#Increment the net force
				_net_force[0] += _force_inc[0]
				_net_force[1] += _force_inc[1]

		#Limit net force
		_net_force = self.limit_force(_net_force, Particle.gas_max_net_force)

		#Get containment force of system
		_containment_force = self.contain(
				(_system_position[0] + _system_radius, _system_position[1] + _system_radius), 
				_system_radius,
				Particle.gas_containment_range)

		#Limit the containment force by the maximum possible individual force
		_containment_force = self.limit_force(_containment_force, Particle.gas_max_containment_force)

		#Scale containment force by Particle constant
		_containment_force[0] *= Particle.gas_containment_force
		_containment_force[1] *= Particle.gas_containment_force


		#increment net force by containment force of system
		_net_force[0] += _containment_force[0]
		_net_force[1] += _containment_force[1]

		#Increment new velocity by net force
		_velocity = [self.x_velocity + _net_force[0], self.y_velocity + _net_force[1]]

		#Cap new velocity
		_velocity = self.limit_force(_velocity, Particle.gas_max_velocity)
		
		#set velocity to new velocity
		self.x_velocity = _velocity[0]
		self.y_velocity = _velocity[1]

		#increment position by velocity
		self.x_position += math.floor(self.x_velocity)
		self.y_position += math.floor(self.y_velocity)

		self.color = (255, 255, 255)


				


	#returns the force vector needed to increment the velocity to get this particle to seek the given pos
	def seek(self, _seek_position):
		_force = [(_seek_position[0] - self.x_position), (_seek_position[1] - self.y_position)]
		#find distance for seek position
		#_dist =  math.sqrt( (_seek_position[0] - self.x_position)**2 + (_seek_position[1] - self.y_position)**2 )
		_dist = self.get_surface_distance(_seek_position[0], _seek_position[1])

		#Scale force by distance
		_force[0] *= _dist

		_force[1] *= _dist
		
		return _force

	#returns the force vector needed to increment toe velocity to get this particle to flee the given position
	def flee(self, _flee_position):
		_force = [-1 * (_flee_position[0] - self.x_position), -1 * (_flee_position[1] - self.y_position)]
		#Find distance from flee position
		#_dist =  math.sqrt( (_flee_position[0] - self.x_position)**2 + (_flee_position[1] - self.y_position)**2 )
		
		_dist = self.get_surface_distance(_flee_position[0], _flee_position[1])

		if(_dist == 0 or _dist < 1/Particle.max_flee_weight): _dist = Particle.max_flee_weight

		#Scale by inverse of distance
		_force[0] *= 1/_dist
		_force[1] *= 1/_dist
		return _force

	def contain(self, _system_center, _system_radius, _containment_range_factor):
		#Create contentment force
		_containment_force = [0, 0]

		#Calculate particle's distance from the center of the system
		_dist =  math.sqrt( (_system_center[0] - self.x_position)**2 + (_system_center[1] - self.y_position)**2 )
		
		#Calculate the containment range
		_containment_range = _system_radius * _containment_range_factor
		
		
		#if the distance is greater than the containment range we must have a non zero containment force
		#if(_dist > _containment_range):
		_containment_force = self.seek(_system_center)

		_diff = _dist - _containment_range

		if(_diff > 0):
			_containment_force[0] *= _diff
			_containment_force[1] *= _diff
		else:
			_containment_force[0] *= 0

		return _containment_force	
		
	def limit_force(self, _force, _max_magnitude):
		#Calculate the magnitude of the force
		_mag = math.sqrt(_force[0]**2 + _force[1]**2)
		if(_mag > _max_magnitude):
			_force[0] = _force[0] * (_max_magnitude/_mag)
			_force[1] = _force[1] * (_max_magnitude/_mag)
		return _force

	#Gets the distance between the surfaces of this
	#particle and the particle at position _x_pos _y_pos
	def get_surface_distance(self, _x_pos, _y_pos):
		_dist = math.sqrt((self.x_position - _x_pos)**2 + (self.y_position - _y_pos)**2) - (2 * Particle.particle_radius)
		return _dist

	#Reflects this particles trajectory over the normal to an axis aligned surface
	#And pushes it out of the collision
	def resolve_collision(self, _colliding_surface):
		_velocity = [self.x_velocity, self.y_velocity]

		#Find reflection axis
		if(_colliding_surface[0] == 0): 	#Reflecting over X
			_velocity[0] *= -2
		elif(_colliding_surface[1] == 0):	#Reflecting over Y
			_velocity[1] *= -2

		#Move position by negative velocity to exit colliding state
		self.x_position += int(-1*math.floor(self.x_velocity))
		self.y_position += int(-1*math.floor(self.y_velocity))

		#Change velocity to new velocity
		self.x_velocity = _velocity[0]
		self.y_velocity = _velocity[1]

	def draw_shape(self, _screen, _camera_x_translation):
		#rad = int(Particle.particle_radius)
		#print(rad)
		pygame.draw.circle(
				_screen, 
				self.color, 
				((self.x_position) + Particle.particle_radius - _camera_x_translation, (self.y_position) + Particle.particle_radius), 
				Particle.particle_radius)

	def clear_shape(self, _screen, _camera_x_translation):
		#rad = int(Particle.particle_radius)
		pygame.draw.circle(
				_screen, 
				(0, 0, 0), 
				((self.prev_position[0]) + Particle.particle_radius - _camera_x_translation + 3, (self.prev_position[1]) + Particle.particle_radius), 
				Particle.particle_radius)
		#self.prev_position = (self.x_position, self.y_position)
