from numpy.core.numeric import isclose
from UnitAlg.Convertable import Convertable
from numpy.lib.arraysetops import isin
from UnitAlg.helpers.classproperty import all_true
from UnitAlg.helpers import *
from typing import Any, Iterator, Tuple, Type, Union, List, TypeVar, overload
import numpy as np
import math

T=TypeVar('T')
class BaseVector(Convertable):
	#----Main Properties----
	@property
	def value(self) -> np.ndarray:
		return np.array(self._value)
	@value.setter
	def value(self, value : Union[np.array, List[float]]) -> None:
		self._value = np.array(value, dtype=np.float64)

	@property
	def x(self) -> float:
		return float(self._value[0])
	@x.setter
	def x(self, x:float) -> None:
		self._value[0] = x

	@property
	def y(self) -> float:
		return float(self._value[1])
	@y.setter
	def y(self, y:float) -> None:
		self._value[1] = y
	
	@property
	def z(self) -> float:
		return float(self._value[2])
	@z.setter
	def z(self, z:float) -> None:
		self._value[2] = z
		
	#----Casting----
	@classmethod
	def _from_np(cls:Type[T], value: np.ndarray) -> T:
		newArr = cls.__new__(cls)
		newArr._value = value
		return newArr
	
	#----Functions----
	@property
	def sq_magnitude(self) -> float:
		''' Returns squared length of this vector '''
		return np.dot(self._value, self._value)
	
	@property
	def magnitude(self) -> float:
		''' Returns the length of this vector '''
		return np.linalg.norm(self.value)

	def normalize(self) -> None:
		'''
		Makes this vector have a magnitude of 1 with same direction as before
		Note: this function will change the current vector.  Use normalized if change is undesired
		'''
		self.value = self.value / self.magnitude
		#TODO: handle 0 magnitude through a abstract method in both normalize functions

	@property
	def normalized(self:T) -> T:
		'''
		Returns the unit vector for current vector
		Note: this function does NOT affect the current vector.  Use normalize function if change is desired.
		'''
		return type(self)(self._value / self.magnitude)
	
	def __eq__(self:T,other:T) -> bool:
		return all(np.isclose(self._value, other._value, rtol=1e-12, atol=1e-11))
	def __ne__(self:T,other:T) -> bool:
		return any(not np.isclose(v1,v2, rtol=1e-12, atol=1e-11) for v1,v2 in zip(self._value, other._value))
		
	def __getitem__(self, index:int)->float:
		return self._value[index]
	def __setitem__(self,index:int,value:float) -> None:
		self._value[index] = value
		
	def __iter__(self) -> Iterator[float]:
		return self._value.__iter__()
	def __len__(self) -> int:
		return len(self._value)
	
	def __hash__(self) -> int:
		return hash(tuple(self._value))