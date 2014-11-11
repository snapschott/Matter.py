import pygame.draw
class Object:

	def __init__(self, xPos, yPos, xDim, yDim):
		self.x_position = xPos
		self.y_position = yPos
		self.prev_position = (self.x_position, self.y_position)
		self.dimension = (xDim, yDim)
	
	def update(self):
		self.prev_position = (self.x_position, self.y_position)
		

	##Checks if two objects are colliding
	def is_colliding(self, object):
		if(self == object): return false
		objDX, objDY = object.dimension
		dX, dY = self.dimension
		if(self.x_position < object.x_position + objDX and self.x_position + dX > object.x_position):
			if(self.y_position < object.y_position + objDY and self.y_position + dY > object.y_position):
				return True
		return False

	#Returns a vector indicating the direction and magnitude of the side of the object
	#which the particle is colliding 
	def get_colliding_side(self, object):
		_collision_side = [0, 0]
		_distances = [ 
			#difference in left side of particle from right side of object
			abs(self.x_position - (object.x_position + object.dimension[0])),
			#Difference in right side of particle from left side of object
			abs((self.x_position + self.dimension[0]) - object.x_position),
			#difference in top side of particle from bottom side of object
			abs(self.y_position - (object.y_position + object.dimension[1])),
			#difference in bottom side of particle from top side of object
			abs((self.y_position + self.dimension[1]) - object.y_position)]

		_smallest_index = 0
		#Determine the smallest difference
		for _index in range(0, 3):
			if(_distances[_index] < _distances[_smallest_index]): _smallest_index = _index
		
		#If the colliding side was the:
		if(_smallest_index == 0):		#Right side
			_collision_side[1] = object.dimension[1]
		elif(_smallest_index == 1):		#Left side
			_collision_side[1] = -object.dimension[1]
		elif(_smallest_index == 2):		#bottom side
			_collision_side[0] = -object.dimension[0]
		else:					#Top side
			_collision_side[0] = object.dimension[0]
		
		return _collision_side


	##Draws this object
	def draw(self, _screen, _camera_x_translation):
		self.clear_shape(_screen, _camera_x_translation)
		self.draw_shape(_screen, _camera_x_translation)
		

	def draw_shape(self, _screen, _camera_x_translation):
		pygame.draw.rect(_screen, self.color, ((self.x_position - _camera_x_translation, self.y_position), self.dimension))

	def clear_shape(self, _screen, _camera_x_translation):
		pygame.draw.rect(_screen, (0, 0, 0), ((self.prev_position[0] - _camera_x_translation + 3, self.prev_position[1]), self.dimension))
		#self.prev_position = (self.x_position, self.y_position)

	def push_left(self, _trans):
		self.x_position -= _trans
