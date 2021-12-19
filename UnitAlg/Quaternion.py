from UnitAlg.BaseVector import BaseVector
from UnitAlg.helpers import *
from typing import Any, Union, List, Tuple, overload
import numpy as np
import math
from multipledispatch import dispatch

from UnitAlg import Vector3

class Quaternion(BaseVector):
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
				self._derived_updated = False #TODO: look over init cause apparently I didnt finish editing this after copy paste
		elif all_true((isinstance(v,(int, float)) for v in (x_other,y,z,w))):
			self.value = [x_other,y,z,w]
		else:
			raise ValueError("init can only take 3 real numbers, or 1 list numpy array or some type with a conversion function specified in from_conversions and nothing else.")
				
	@classproperty
	def identity() -> 'Quaternion':
		return Quaternion(0,0,0,1)

	@staticmethod
	def from_rotation_matrix(m:Union[np.ndarray, List[List[Union[float,int]]]]) -> 'Quaternion':
		#http://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToQuaternion/index.htm
		trace = m[0,0] + m[1,1] + m[2,2]
		if trace > 0:
			s = 0.5 / math.sqrt(trace+ 1)
			return Quaternion([
				(m[2,1] - m[1,2]) * s,
				(m[0,2] - m[2,0]) * s,
				(m[1,0] - m[0,1]) * s,
				0.25 / s
			])
		elif m[0,0] > m[1,1] and m[0,0] > m[2,2]:
			s = 2 * math.sqrt(1 + m[0,0] - m[1,1] - m[2,2])
			return Quaternion([
				0.25 * s,
				(m[0,1] + m[1,0]) / s,
				(m[0,2] + m[2,0]) / s,
				(m[2,1] - m[1,2]) / s
			])
		elif m[1,1] > m[2,2]:
			s = 2 * math.sqrt(1 + m[1,1] - m[0,0] - m[2,2])
			return Quaternion([
				(m[0,1] + m[1,0]) / s,
				0.25 * s,
				(m[1,2] + m[2,1]) / s,
				(m[0,2] - m[2,0]) / s
			])
		else:
			s = 2 * math.sqrt(1 + m[2,2] - m[0,0] - m[1,1])
			return Quaternion([
				(m[0,2] + m[2,0]) / s,
				(m[1,2] + m[2,1]) / s,
				0.25 * s,
				(m[1,0] - m[0,1]) / s
			])
			
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
	def eulers(self) -> Tuple[float,float,float]:
		'''
		Calculates and returns the euler equivalent of this quaternion.
		
		Result in radians about x,y,z (in that order).
		'''
		_x, _y, _z, _w = self._value
		test = _x*_y + _z*_w
		near_point_5 = .5-epsilon
		if test > near_point_5: #singularity at north pole
			y_e = 2 * math.atan2(_x,_w)
			z_e = math.pi/2
			x_e = 0
		elif test < -near_point_5: #singularity at south pole
			y_e = -2 * math.atan2(_x,_w)
			z_e = - math.pi/2
			x_e = 0
		else:
			sqx = _x*_x
			sqy = _y*_y
			sqz = _z*_z
			y_e = math.atan2(2*_y*_w-2*_x*_z , 1 - 2*sqy - 2*sqz)
			z_e = math.asin(2*test)
			x_e = math.atan2(2*_x*_w-2*_y*_z , 1 - 2*sqx - 2*sqz)
		return x_e, y_e, z_e
	
	def inverse(self) -> 'Quaternion':
		#from rospy tf.transformations
		return Quaternion(self.conjugate()._value / np.dot(self._value, self._value))

	def normalize(self) -> None:
		mag = math.sqrt(np.dot(self._value, self._value))
		if mag < epsilon:
			self.value = np.array([0,0,0,1])
		self.value = self._value/mag

	#----Operators----
	def __str__(self) -> str:
		return str.format('angle:{0} axis:{1} Quaternion:({2},{3},{4},{5})',math.degrees(self.angle),self.axis,*self._value)
	
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
