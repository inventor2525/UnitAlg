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
	def from_rotation_matrix(matrix:Union[np.ndarray, List[List[Union[float,int]]]]) -> 'Quaternion':
		#from rospy tf.transformations
		q = np.empty((4, ), dtype=np.float64)
		M = np.array(matrix, dtype=np.float64, copy=False)[:4, :4]
		t = np.trace(M)
		if t > M[3, 3]:
			q[3] = t
			q[2] = M[1, 0] - M[0, 1]
			q[1] = M[0, 2] - M[2, 0]
			q[0] = M[2, 1] - M[1, 2]
		else:
			i, j, k = 0, 1, 2
			if M[1, 1] > M[0, 0]:
				i, j, k = 1, 2, 0
			if M[2, 2] > M[i, i]:
				i, j, k = 2, 0, 1
			t = M[i, i] - (M[j, j] + M[k, k]) + M[3, 3]
			q[i] = t
			q[j] = M[i, j] + M[j, i]
			q[k] = M[k, i] + M[i, k]
			q[3] = M[k, j] - M[j, k]
		q *= 0.5 / math.sqrt(t * M[3, 3])
		return Quaternion(q)

	@staticmethod
	def from_angle_axis(angle:float, axis:Vector3) -> 'Quaternion':
		'''
		Use degrees for the angle
		'''
		q = Quaternion(*(axis.normalized._value*np.sin(angle/2)), np.cos(angle/2))
		q.normalize
		q._angle = angle
		q._axis = axis
		q._derived_updated = True
		return q
	
	@staticmethod
	def from_euler(x:float,y:float,z:float) -> 'Quaternion':
		#https://www.euclideanspace.com/maths/geometry/rotations/conversions/eulerToQuaternion/index.htm
		x /= 2
		y /= 2
		z /= 2
		c1 = math.cos(y)
		s1 = math.sin(y)
		c2 = math.cos(z)
		s2 = math.sin(z)
		c3 = math.cos(x)
		s3 = math.sin(x)
		c1c2 = c1*c2
		s1s2 = s1*s2
		return Quaternion([
			c1c2*s3 + s1s2*c3,
			s1*c2*c3 + c1*s2*s3,
			c1*s2*c3 - s1*c2*s3,
			c1c2*c3 - s1s2*s3
		])
	
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
		#https://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToAngle/index.htm
		if not self._derived_updated:
			_w = self.w
			if _w > 1: self.normalize()
			self._angle = 2 * math.acos(_w)
			s = math.sqrt(1-_w*_w)
			if s < epsilon:
				self._axis = Vector3(*(self._value[0:3]))
			else:
				self._axis = Vector3(*(self._value[0:3]/s))
			self._derived_updated = True
	
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
		#from rospy tf.transformations
		return Quaternion(np.array((-self._value[0], -self._value[1],
						-self._value[2], self._value[3]), dtype=np.float64))

	def inverse(self) -> 'Quaternion':
		#from rospy tf.transformations
		return Quaternion(self.conjugate()._value / np.dot(self._value, self._value))

	def normalize(self) -> None:
		mag = math.sqrt(np.dot(self._value, self._value))
		if mag < np.finfo.tiny:
			self.value = np.array([0,0,0,1])
		self.value = self._value/mag


	#----Operators----
	def __eq__(self,other) -> bool:
		return all(self.value == other.value)

	def __ne__(self,other) -> bool:
		return any(self.value != other.value)
	
	def __str__(self) -> str:
		return str.format('angle:{0} axis:({1},{2},{3}) Quaternion:({4},{5},{6},{7})',math.degrees(self.angle),*self.axis.value,*self._value)
	
	def __repr__(self) -> str:
		return self.__str__()
	
	@overload
	def __mul__(self,other:'Quaternion')->'Quaternion':...
	@overload
	def __mul__(self,other:Vector3)->Vector3:...

	def __mul__(self,other):
		if isinstance(other, Quaternion):
			x0,y0,z0,w0 = self._value[0], self._value[1], self._value[2], self._value[3]
			x1,y1,z1,w1 = other.x, other.y, other.z, other.w
			return Quaternion(np.array((
			x1*w0 + y1*z0 - z1*y0 + w1*x0,
			-x1*z0 + y1*w0 + z1*x0 + w1*y0,
			x1*y0 - y1*x0 + z1*w0 + w1*z0,
			-x1*x0 - y1*y0 - z1*z0 + w1*w0), dtype=np.float64))

		elif isinstance(other, Vector3):
			x = self._value[0] * 2.0
			y = self._value[1] * 2.0
			z = self._value[2] * 2.0
			xx = self._value[0] * x
			yy = self._value[1] * y
			zz = self._value[2] * z
			xy = self._value[0] * y
			xz = self._value[0] * z
			yz = self._value[1] * z
			wx = self._value[3] * x
			wy = self._value[3] * y
			wz = self._value[3] * z
			
			_x = (1.0 - (yy + zz)) * other.x + (xy - wz) * other.y + (xz + wy) * other.z
			_y = (xy + wz) * other.x + (1.0 - (xx + zz)) * other.y + (yz - wx) * other.z
			_z = (xz - wy) * other.x + (yz + wx) * other.y + (1.0 - (xx + yy)) * other.z
			return Vector3(_x,_y,_z)
