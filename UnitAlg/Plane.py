from typing import Union, overload, Tuple
from UnitAlg import Vector3, Quaternion, Ray
from multipledispatch import dispatch

class Plane():
	@dispatch(Vector3,Vector3)
	def __dispatch_init__(self, point:Vector3, normal:Vector3) -> None:
		self.point = point
		self.normal = normal
	@dispatch(Vector3,Vector3,Vector3)
	def __dispatch_init__(self, p1:Vector3, p2:Vector3, p3:Vector3) -> None:
		self.point = p1
		self.normal = Vector3.cross((p2-p1).normalized, (p3-p1).normalized)
	@dispatch((float,int), (float,int), (float,int))
	def __dispatch_init__(self, x_coefficient:Union[float,int], y_coefficient:Union[float,int], z_offset:Union[float,int]) -> None:
		'''#using ax + by + c = z method:'''
		p1 = Vector3([0,0,z_offset])
		p2 = Vector3([100,0, x_coefficient*100 + z_offset])
		p3 = Vector3([0, 100, y_coefficient*100 + z_offset])
		self.__dispatch_init__(p1, p2, p3)
	
	@overload
	def __init__(self, point:Vector3, normal:Vector3) -> None:
		'''
		Creates a plane with a position and normal.
		'''
		...
	@overload
	def __init__(self, p1:Vector3, p2:Vector3, p3:Vector3) -> None:
		'''
		Creates a plane with 3 positions.
		'''
		...
	@overload
	def __init__(self, p1:Vector3, p2:Vector3, p3:Vector3) -> None:
		'''
		Creates a plane with coefficients that describe it's equation.
		
		Note: this only works if it is not perpendicular to the xy plane.
		'''
		...
	def __init__(self, *args) -> None:
		self.__dispatch_init__(*args)
	
	#----Main Properties----
	@property
	def point(self) -> Vector3:
		return self._point
	@point.setter
	def point(self, point:Vector3) -> None:
		self._point = point

	@property
	def normal(self) -> Vector3:
		return self._normal
	@normal.setter
	def normal(self, normal:Vector3) -> None:
		self._normal = normal

	#----Functions----
	def raycast(self,ray:Ray) -> Tuple[bool, Vector3]:
		denom = Vector3.dot(ray.direction,self.normal)
		if denom > 0:
			p0 = self.point - ray.origin
			t = Vector3.dot(self.normal, p0)/denom
			intersection = ray.origin + ray.direction*t
			return t >= 0
		elif denom == 0:
			return False, None
		else:
			negNormal = -self.normal
			denom = Vector3.dot(negNormal, ray.direction)
			p0 = self.point - ray.origin
			t = Vector3.dot(p0, negNormal)/denom
			intersection = ray.origin + ray.direction * t
			return t >= 0	

	@dispatch(Vector3)
	def _reflect(self, direction:Vector3) -> Vector3:
		incoming_angle = Vector3.angle(direction,self.normal)
		if incoming_angle != 0:
			rotation_axis = Vector3.cross(direction, self.normal)
			rotation = Quaternion.from_angle_axis(2*incoming_angle, rotation_axis)
			return rotation*direction
		else:
			return direction
	@dispatch(Ray)
	def _reflect(self, ray:Ray) -> Ray:
		return Ray(self.raycast(ray), self._reflect(ray.direction))
	@overload
	def reflect(self, direction:Vector3) -> Vector3: 
		'''
		Reflect direction off a plane, at an angle equal to incoming angle.
		'''
		...
	@overload
	def reflect(self, ray:Ray) -> Ray:
		'''
		Reflect ray off a plane, at an angle equal to incoming angle, and an origin at the intersection point. '''
		...
	def reflect(self,*args):
		return self._reflect(*args)
		
	#----Operators-----
	def __str__(self) -> str:
		return str.format('origin:{0} normal:{1}',self.point, self.normal)
	def __repr__(self) -> str:
		return self.__str__()