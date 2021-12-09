from UnitAlg import Vector3, Quaternion
from OCC.Core.gp import gp_Pln, gp_Pnt, gp_Dir

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
	def reflect(self, ray:Vector3) -> Vector3:
		''' reflect ray from plane, at an angle equal to incoming angle '''
		incoming_angle = Vector3.angle(ray,self.normal)
		if incoming_angle != 0:
			rotation_axis = Vector3.cross(ray, self.normal)
			rotation = Quaternion.from_angle_axis(2*incoming_angle, rotation_axis)
			return rotation*ray
		else:
			return ray

	#----Operators-----
	def __str__(self) -> str:
		return str.format('origin:{0} normal:{1}',self.point, self.normal)
	def __repr__(self) -> str:
		return self.__str__()

