from typing import overload
from UnitAlg import Vector3, Quaternion, Ray
from multipledispatch import dispatch

class Plane():
	''' 
	class for plane objects in UnitAlg.  Features methods to convert between UnitAlg and OOC's version of planes. 
	'''
	def __init__(self, point:Vector3, normal:Vector3):
		self.point = point
		self.normal = normal 

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
		raise NotImplementedError()
	@overload
	def reflect(self, direction:Vector3) -> Vector3: 
		''' reflect direction off a plane, at an angle equal to incoming angle. '''
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