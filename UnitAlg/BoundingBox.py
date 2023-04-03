class BoundingBox:
	def __init__(self, position:Vector3, size:Vector3) -> None:
		self.position = position
		self.size = size
	
	@classmethod
	def from_points(cls, points:list) -> 'BoundingBox':
		'''
		Returns the smallest bounding box that contains all the points.
		'''
		#Find the center of the box
		center = Vector3.average(points)
		#Find the size of the box
		size = Vector3.zero()
		for point in points:
			size.x = max(size.x, abs(point.x - center.x))
			size.y = max(size.y, abs(point.y - center.y))
			size.z = max(size.z, abs(point.z - center.z))
		#Return the box
		return cls(center, size)
	
	@classmethod
	def from_spheres(cls, spheres:list) -> 'BoundingBox':
		'''
		Returns the smallest bounding box that contains all the spheres.
		'''
		#Find the center of the box
		center = Vector3.average([sphere.position for sphere in spheres])
		#Find the size of the box
		size = Vector3.zero()
		for sphere in spheres:
			size.x = max(size.x, sphere.radius + abs(sphere.position.x - center.x))
			size.y = max(size.y, sphere.radius + abs(sphere.position.y - center.y))
			size.z = max(size.z, sphere.radius + abs(sphere.position.z - center.z))
		#Return the box
		return cls(center, size)