from UnitAlg.helpers import *
from typing import Any, Union, List, Tuple, overload
import numpy as np
import math

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

	#----Operators----
	def __eq__(self,other) -> bool:
		#could also use gp_Quaternion.IsEqual() here but would also increase occ dependency
		return all(self.value == other.value)

	def __ne__(self,other) -> bool:
		return any(self.value != other.value)
	
	def __str__(self) -> str:
		return str.format('angle:{0} axis:({1},{2},{3}) Quaternion:({4},{5},{6},{7})',math.degrees(self.angle),*self.axis.value,*self._value)
	def __repr__(self) -> str:
		return self.__str__()