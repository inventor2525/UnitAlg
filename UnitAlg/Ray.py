from UnitAlg.Vector3 import Vector3

class Ray():
	def __init__(self, origin:Vector3, direction:Vector3) -> None:
		self.origin = origin
		self.direction = direction
	
	def closest_point(self, point:Vector3) -> Vector3:
		'''
		Returns the closest point on the ray to the point.
		'''
		#Find the vector from the origin to the point
		vector = point - self.origin
		#Find the projection of the vector onto the direction
		projection = Vector3.dot(vector, self.direction)
		#Return the closest point
		return self.origin + self.direction * projection
		
	def refract(self, normal:Vector3, n1:float, n2:float) -> Vector3:
		'''
		Returns the refracted direction of the ray.
		'''
		#source: https://en.wikipedia.org/wiki/Snell%27s_law#Vector_form
		#Find the cosine of the angle between the direction and the normal
		cosine = Vector3.dot(self.direction, normal)
		#Find the ratio of the indices of refraction
		ratio = n1/n2
		#Find the sine of the angle between the refracted direction and the normal
		sine = ratio * (1 - cosine**2)
		#Return the refracted direction
		return self.direction * ratio - normal * (ratio * cosine + sine**0.5)
	
	def skew_point(self, ray:'Ray') -> Vector3:
		'''
		Returns the closest point on this ray to the passed ray.
		'''
		#source: https://en.wikipedia.org/wiki/Skew_lines#Nearest_points
		n = Vector3.cross(self.direction, ray.direction)
		
		#If the rays are nearly parallel:
		if n.sq_magnitude < 0.000001:
			return self.origin
		
		n2 = Vector3.cross(ray.direction, n)
		diff = ray.origin - self.origin
		
		return self.origin + self.direction * (Vector3.dot(diff, n2) / Vector3.dot(self.direction, n2))
	
	def at(self, t:float) -> Vector3:
		'''
		Returns the point on the ray at the given distance.
		'''
		return self.origin + self.direction * t
		
	def __str__(self) -> str:
		return 'Ray(origin: {}, direction: {})'.format(self.origin, self.direction)