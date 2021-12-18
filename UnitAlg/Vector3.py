from numpy.core.numeric import isclose
from UnitAlg.Convertable import Convertable
from numpy.lib.arraysetops import isin
from UnitAlg.helpers.classproperty import all_true
from UnitAlg.helpers import *
from typing import Any, Iterator, Tuple, Type, Union, List, overload
import numpy as np
import math

class Vector3(Convertable):
	to_conversions = {}
	from_conversions = {}
	
	@overload
	def __init__(self, x:Union[float,int], y:Union[float,int], z:Union[float,int]=0) -> None: ...
	@overload
	def __init__(self, arr:Union[np.ndarray,List[Union[float,int]], Tuple[Union[float,int]]]) -> None: ...
	@overload
	def __init__(self, arr:Any) -> None: ... #TODO: Is a variable restriciton on typeing possible? based on converison functions?

	def __init__(self, x_other, y=None,z=0) -> None:
		if y is None:
			if isinstance(x_other, (list, tuple)):
				if len(x_other) == 3:
					self.value = x_other
				else:
					raise ValueError("Invalid list or tuple, need size of 3, got {}",len(x_other))
			elif isinstance(x_other, np.ndarray):
				if x_other.shape==(3,):
					self.value = x_other
				elif x_other.shape==(1,3):
					self.value = x_other[0]
				else:
					raise ValueError("invalid numpy array shape {}, expected shape (3,) or (1,3)",x_other.shape)
			else:
				self._value = Vector3._from(x_other)._value
		elif all_true((isinstance(v,(int, float)) for v in (x_other,y,z))):
			self.value = [x_other,y,z]
		else:
			raise ValueError("init can only take 3 real numbers, or 1 list numpy array or some type with a conversion function specified in from_conversions and nothing else.")
				
	#----Common values----
	@classproperty
	def back() -> 'Vector3':
		return Vector3(0,0,-1)
	@classproperty
	def down() -> 'Vector3':
		return Vector3(0,-1,0)
	@classproperty
	def forward() -> 'Vector3':
		return Vector3(0,0,1)
	@classproperty
	def left() -> 'Vector3':
		return Vector3(-1,0,0)
	@classproperty
	def negative_infinity() -> 'Vector3':
		return Vector3(-math.inf,-math.inf,-math.inf)
	@classproperty
	def one() -> 'Vector3':
		return Vector3(1,1,1)
	@classproperty
	def positive_infinity() -> 'Vector3':
		return Vector3(math.inf,math.inf,math.inf)
	@classproperty
	def right() -> 'Vector3':
		return Vector3(1,0,0)
	@classproperty
	def up() -> 'Vector3':
		return Vector3(0,1,0)
	@classproperty
	def zero() -> 'Vector3':
		return Vector3(0,0,0)
		
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
	@staticmethod
	def _from_np(value: np.ndarray) -> 'Vector3':
		newArr = Vector3.__new__(Vector3)
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

	@property
	def normalized(self) -> 'Vector3':
		'''
		Returns the unit vector for current vector
		Note: this function does NOT affect the current vector.  Use normalize function if change is desired.
		'''
		return self / self.magnitude

	@staticmethod
	def distance(vector_a:'Vector3', vector_b:'Vector3') -> float:
		''' Returns the distance between two vectors (same as (a-b).magnitude) '''
		return (vector_a - vector_b).magnitude
	
	@staticmethod 
	def angle(from_v:'Vector3', to_v:'Vector3') -> float:
		''' 
		Returns the unsigned angle between 'fromV' and 'toV' in degrees.  
		Angle is never greater than 180.  
		'''
		return math.acos(Vector3.dot(from_v,to_v)/(from_v.magnitude*to_v.magnitude))
	
	@staticmethod
	def cross(vector_a:'Vector3',vector_b:'Vector3') -> 'Vector3':
		'''Cross product between two vectors '''
		return Vector3._from_np(np.cross(vector_a.value,vector_b.value))
	@staticmethod
	def dot(vector_a:'Vector3', vector_b:'Vector3') -> float:
		''' Dot product between two vectors '''
		return np.dot(vector_a.value,vector_b.value)

	@staticmethod
	def lerp(vector_a:'Vector3', vector_b:'Vector3', factor:float) -> 'Vector3':
		p1 = vector_a.value
		p2 = vector_b.value
		v = (p2-p1)
		d = np.linalg.norm(v)
		v_norm = v/d
		return Vector3._from_np(p1 + v_norm*d*factor)

	#----Operators----
	def __add__(self,other:'Vector3') -> 'Vector3':
		return Vector3._from_np(self.value + other.value)
	def __iadd__(self,other:'Vector3') -> 'Vector3':
		return self + other
	def __sub__(self,other:'Vector3') -> 'Vector3':
		return Vector3._from_np(self.value - other.value)
	
	def __mul__(self,other:float) -> 'Vector3':
		return Vector3._from_np(self.value * other)
	def __truediv__(self,other:float) -> 'Vector3':
		if math.isclose(other,0.0):
			return Vector3(math.nan, math.nan, math.nan)
		return Vector3._from_np(np.divide(self.value, other))
		
	def __eq__(self,other:'Vector3') -> bool:
		return all(np.isclose(self._value, other._value, rtol=1e-12, atol=1e-11))
	def __ne__(self,other:'Vector3') -> bool:
		return any(not np.isclose(v1,v2, rtol=1e-12, atol=1e-11) for v1,v2 in zip(self._value, other._value))
		
	def __getitem__(self, index:int)->float:
		return self._value[index]
	def __setitem__(self,index:int,value:float) -> None:
		self._value[index] = value
		
	def __iter__(self) -> Iterator[float]:
		return self._value.__iter__()
	def __len__(self) -> int:
		return 3
		
	def __hash__(self) -> int:
		return hash((self.x,self.y,self.z))
		
	def __str__(self) -> str:
		return str.format('({0}, {1}, {2})',*self._value)
	def __repr__(self) -> str:
		return self.__str__()
		
if __name__ == "__main__":
	print(Vector3(3,4,5))
	
	print(Vector3(3,4))
	print(Vector3(1,2))
	print(Vector3([0,math.pi,42]))
	try:
		print(Vector3(1))
	except Exception as e: print(e)
	
	try:
		print(Vector3([1,2]))
	except Exception as e: print(e)
	
	try:
		print(Vector3([1,2,3],6))
	except Exception as e: print(e)
	
	try:
		print(Vector3(1,'f'))
	except Exception as e: print(e)