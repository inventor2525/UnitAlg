from typing import List, Union, overload, Tuple
from UnitAlg import Vector3, Quaternion, Ray
from multipledispatch import dispatch
import numpy as np

class Plane():
	@dispatch(Vector3,Vector3)
	def __dispatch_init__(self, position:Vector3, normal:Vector3) -> None:
		self.position = position
		self.normal = normal
	@dispatch(Vector3,Vector3,Vector3)
	def __dispatch_init__(self, p1:Vector3, p2:Vector3, p3:Vector3) -> None:
		self.position = p1
		self.normal = Vector3.cross((p2-p1).normalized, (p3-p1).normalized)
	@dispatch((float,int), (float,int), (float,int))
	def __dispatch_init__(self, x_coefficient:Union[float,int], y_coefficient:Union[float,int], z_offset:Union[float,int]) -> None:
		'''#using ax + by + c = z method:'''
		self._a = x_coefficient
		self._b = y_coefficient
		self._c = z_offset
		p1 = Vector3([0,0,z_offset])
		p2 = Vector3([100,0, x_coefficient*100 + z_offset])
		p3 = Vector3([0, 100, y_coefficient*100 + z_offset])
		self.__dispatch_init__(p1, p2, p3)
	
	@overload
	def __init__(self, position:Vector3, normal:Vector3) -> None:
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
	def __init__(self, x_coefficient:Union[float,int], y_coefficient:Union[float,int], z_offset:Union[float,int]) -> None:
		'''
		Creates a plane with coefficients that describe it's equation.
		
		Note: this only works if it is not perpendicular to the xy plane.
		'''
		...
	@overload
	def __init__(self, points:List[Vector3]) -> None:
		'''
		Creates a plane by best fitting to the passed points.
		
		Does not handle planes perpendicular to the xy plane.
		'''
		...
	def __init__(self, *args) -> None:
		self._a:float = None
		self._b:float = None
		self._c:float = None
		if len(args)==1 and isinstance(args[0], list):
			points = args[0]
			coefficients = Plane.fit_coefficients(points)
			self.__init__(*coefficients)
		else:
			self.__dispatch_init__(*args)
	
	#----Main Properties----
	@property
	def position(self) -> Vector3:
		return self._position
	@position.setter
	def position(self, position:Vector3) -> None:
		self._position = position

	@property
	def normal(self) -> Vector3:
		return self._normal
	@normal.setter
	def normal(self, normal:Vector3) -> None:
		self._normal = normal
	
	def _ensure_coefficents(self):
		if self._a is None or self._b is None or self._c is None:
			raise NotImplementedError("TODO: implement calculation of plane coefficents from normal and position.")
			
	@property
	def a(self) -> float:
		self._ensure_coefficents()
		return self._a
	
	@property
	def b(self) -> float:
		self._ensure_coefficents()
		return self._b
		
	@property
	def c(self) -> float:
		self._ensure_coefficents()
		return self._c
		
	@staticmethod
	#from https://math.stackexchange.com/questions/99299/best-fitting-plane-given-a-set-of-points (use the pretty graph one)
	def fit_coefficients(points:List[Vector3]) -> Tuple[float,float,float]:
		'''
		Find the coefficents of a plane given a list of points.
		
		Note, this only works with planes that are not
		perpendicular to the x,y plane.
		'''
		tmp_A = []
		tmp_b = []
		for point in points:
			tmp_A.append([*point[0:2], 1])
			tmp_b.append(point[2])
		b = np.matrix(tmp_b).T
		A = np.matrix(tmp_A)

		fit = (A.T * A).I * A.T * b
		#errors = b - A * fit
		#residual = np.linalg.norm(errors)

		return tuple(np.array(fit)[:,0]) #, errors, residual
		
	#----Functions----
	def raycast(self,ray:Ray) -> Tuple[bool, Vector3]:
		denom = Vector3.dot(ray.direction,self.normal)
		if denom > 0:
			p0 = self.position - ray.origin
			t = Vector3.dot(self.normal, p0)/denom
			return t >= 0, ray.origin + ray.direction*t
		elif denom == 0:
			return False, None
		else:
			negNormal = -self.normal
			denom = Vector3.dot(negNormal, ray.direction)
			p0 = self.position - ray.origin
			t = Vector3.dot(p0, negNormal)/denom
			return t >= 0, ray.origin + ray.direction * t	

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
		Reflect ray off a plane, at an angle equal to incoming angle, and an origin at the intersection position. '''
		...
	def reflect(self,*args):
		return self._reflect(*args)
		
	#----Operators-----
	def __str__(self) -> str:
		return str.format('origin:{0} normal:{1}',self.position, self.normal)
	def __repr__(self) -> str:
		return self.__str__()