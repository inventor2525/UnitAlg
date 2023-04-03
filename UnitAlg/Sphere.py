from UnitAlg import Vector3, Quaternion, Ray

class Sphere():
	def __init__(self, position:Vector3, radius:float) -> None:
		self.position = position
		self.radius = radius
	
	@classmethod
	def from_points(cls, points:list) -> 'Sphere':
		'''
		Returns the smallest sphere that contains all the points.
		'''
		#Find the center of the sphere
		center = Vector3.average(points)
		#Find the radius of the sphere
		radius = 0
		for point in points:
			radius = max(radius, Vector3.distance(point, center))
		#Return the sphere
		return cls(center, radius)
	
	@classmethod
	def best_fit(cls, points:list) -> 'Sphere':
		'''
		Returns the sphere that best fits the points.
		'''
		#Find the center of the sphere
		center = Vector3.average(points)
		#Find the radius of the sphere
		radius = 0
		for point in points:
			radius += Vector3.distance(point, center)
		radius /= len(points)
		#Return the sphere
		return cls(center, radius)
	
	@classmethod
	def from_bounding_box(cls, box:BoundingBox) -> 'Sphere':
		'''
		Returns the smallest sphere that contains the bounding box.
		'''
		#Find the center of the sphere
		center = box.position + box.size/2
		#Find the radius of the sphere
		radius = Vector3.magnitude(box.size)/2
		#Return the sphere
		return cls(center, radius)
		
	def contains_point(self, point:Vector3) -> bool:
		'''
		Returns whether the sphere contains the point.
		'''
		return Vector3.distance(point, self.position) <= self.radius
	
	def contains_sphere(self, sphere:'Sphere') -> bool:
		'''
		Returns whether the sphere contains the other sphere.
		'''
		return Vector3.distance(sphere.position, self.position) + sphere.radius <= self.radius
	
	def intersects_sphere(self, sphere:'Sphere') -> bool:
		'''
		Returns whether the sphere intersects the other sphere.
		'''
		return Vector3.distance(sphere.position, self.position) <= sphere.radius + self.radius
	
	def intersects_ray(self, ray:Ray) -> bool:
		'''
		Returns whether the sphere intersects the ray.
		'''
		#Find the closest point on the ray to the sphere
		closest = ray.closest_point(self.position)
		#Return whether the closest point is inside the sphere
		return Vector3.distance(closest, self.position) <= self.radius
	
	def intersects_plane(self, plane:Plane) -> bool:
		'''
		Returns whether the sphere intersects the plane.
		'''
		#Find the distance from the sphere to the plane
		distance = plane.distance_to_point(self.position)
		#Return whether the sphere is inside the plane
		return abs(distance) <= self.radius
	
	