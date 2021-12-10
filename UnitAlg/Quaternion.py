from UnitAlg.helpers import *
from typing import Any, Union, List, Tuple, overload
import numpy as np
import math
from multipledispatch import dispatch

from UnitAlg import Vector3

class Quaternion():
	@overload
	def __init__(self, x:Union[float,int], y:Union[float,int], z:Union[float,int], w:Union[float,int]) -> None: ...
	@overload
	def __init__(self, arr:Union[np.ndarray, List[Union[float,int]], Tuple[Union[float,int]]]) -> None: ...
	@overload
	def __init__(self, arr:Any) -> None: ... 
	
	def __init__(self, x_other,y=None,z=None,w=None) -> None:
		if y is None:
			if isinstance(x_other, (list, tuple)):
				if len(x_other) == 4:
					self.value = x_other
				else:
					raise ValueError("Invalid list or tuple, need size of 4, got {}",len(x_other))
			elif isinstance(x_other, np.ndarray):
				if x_other.shape==(4,):
					self.value = x_other
				elif x_other.shape==(1,4):
					self.value = x_other[0]
				else:
					raise ValueError("invalid numpy array shape {}, expected shape (4,) or (1,4)",x_other.shape)
			else:
				self._value = Vector3._from(x_other)._value
				self._derived_updated = False
		elif all_true((isinstance(v,(int, float)) for v in (x_other,y,z,w))):
			self.value = [x_other,y,z,w]
		else:
			raise ValueError("init can only take 3 real numbers, or 1 list numpy array or some type with a conversion function specified in from_conversions and nothing else.")
				
	@classproperty
	def identity() -> 'Quaternion':
		return Quaternion(0,0,0,1)

	@staticmethod
	def from_rotation_matrix(mat:Union[np.ndarray, List[List[Union[float,int]]]]) -> 'Quaternion':
		raise NotImplementedError()

	@staticmethod
	def from_angle_axis(angle:float, axis:Vector3) -> 'Quaternion':
		'''
		Use degrees for the angle
		'''
		raise NotImplementedError()

	#----Main Properties----
	@property
	def value(self) -> np.ndarray:
		return np.array(self._value)
	@value.setter
	def value(self, value : Union[np.ndarray, List[float]]) -> None:
		self._value = np.array(value)
		self._derived_updated = False

	@property
	def x(self) -> float:
		return self._value[0]
	@x.setter
	def x(self, x:float) -> None:
		self._value[0] = x
		self._derived_updated = False

	@property
	def y(self) -> float:
		return self._value[1]
	@y.setter
	def y(self, y:float) -> None:
		self._value[1] = y
		self._derived_updated = False
	
	@property
	def z(self) -> float:
		return self._value[2]
	@z.setter
	def z(self, z:float) -> None:
		self._value[2] = z
		self._derived_updated = False
	
	@property
	def w(self) -> float:
		return self._value[3]
	@w.setter
	def w(self, w:float) -> None:
		self._value[3] = w
		self._derived_updated = False

	#----Derived Properties----
	def _ensure_derived(self) -> None:
		'''
		Calculates derived properties like angle and axis,
		keeping them for performance of recal.
		'''
		if not self._derived_updated:
			raise NotImplementedError()
			#TODO: do this without OCC:
			quat = self.occ_Quaternion
			axis = Vector3()
			self._angle = quat.GetVectorAndAngle(axis)
			self._axis = Vector3.from_other(axis)
	
	@property
	def angle(self) -> float:
		self._ensure_derived()
		return self._angle

	@property
	def axis(self) -> Vector3:
		self._ensure_derived()
		return self._axis

	@property
	def angle_axis(self) -> Tuple[float,Vector3]:
		return self.angle, self._axis

	def inverted(self) -> 'Quaternion':
		return Quaternion.from_angle_axis(-(math.degrees(self.angle)), self.axis)

	def conjugate(self) -> 'Quaternion':
		"""Return conjugate of quaternion.
		>>> q0 = random_quaternion()
		>>> q1 = q0.conjugate()
		>>> q1[3] == q0[3] and all(q1[:3] == -q0[:3])
		True
		"""
		return Quaternion(np.array((-self._value[0], -self._value[1],
						-self._value[2], self._value[3]), dtype=np.float64))

	def inverse(self) -> 'Quaternion':
		"""Return inverse of quaternion.
		>>> q0 = random_quaternion()
		>>> q1 = q0.inverse()
		>>> np.allclose(quaternion_multiply(q0, q1), [0, 0, 0, 1])
		True
		"""
		return Quaternion(self.conjugate().value() / np.dot(self._value, self._value))

	def normalize(self) -> None:
		mag = math.sqrt(np.dot(self._value, self._value))
		if mag < np.finfo.tiny:
			return Quaternion.identity()
		return Quaternion(self._value[0] / mag, self._value[1] / mag, self._value[2] / mag, self._value[3] / mag)



	#----Operators----
	def __eq__(self,other) -> bool:
		return all(self.value == other.value)

	def __ne__(self,other) -> bool:
		return any(self.value != other.value)
	
	def __str__(self) -> str:
		return str.format('angle:{0} axis:({1},{2},{3}) Quaternion:({4},{5},{6},{7})',math.degrees(self.angle),*self.axis.value,*self._value)
	
	def __repr__(self) -> str:
		return self.__str__()
	
	def __mul__(self,other)->'Quaternion':
		if isinstance(other, Quaternion):
			x0,y0,z0,w0 = self._value[0], self._value[1], self._value[2], self._value[3]
			x1,y1,z1,w1 = other.x, other.y, other.z, other.w
			return Quaternion(np.array((
			x1*w0 + y1*z0 - z1*y0 + w1*x0,
			-x1*z0 + y1*w0 + z1*x0 + w1*y0,
			x1*y0 - y1*x0 + z1*w0 + w1*z0,
			-x1*x0 - y1*y0 - z1*z0 + w1*w0), dtype=np.float64))
			
		elif isinstance(other, Vector3):
			x = rotation.x * 2.0
			y = rotation.y * 2.0
			z = rotation.z * 2.0
			xx = rotation.x * x
			yy = rotation.y * y
			zz = rotation.z * z
			xy = rotation.x * y
			xz = rotation.x * z
			yz = rotation.y * z
			wx = rotation.w * x
			wy = rotation.w * y
			wz = rotation.w * z

			res = Vector3()
			res.x = (1.0 - (yy + zz)) * other.x + (xy - wz) * other.y + (xz + wy) * other.z
			res.y = (xy + wz) * other.x + (1.0 - (xx + zz)) * other.y + (yz - wx) * other.z
			res.z = (xz - wy) * other.x + (yz + wx) * other.y + (1.0 - (xx + yy)) * other.z
			return res
