from UnitAlg.BaseVector import BaseVector
from numpy.core.numeric import isclose
from UnitAlg.Convertable import Convertable
from numpy.lib.arraysetops import isin
from UnitAlg.helpers.classproperty import all_true
from UnitAlg.helpers import *
from typing import Any, Iterator, Tuple, Type, Union, List, overload
import numpy as np
import math

class Vector3(BaseVector):
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
	
	#----Functions----
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
		p1 = vector_a._value
		v = (vector_b._value-p1)
		d = np.linalg.norm(v)
		return Vector3._from_np(p1 + v*(factor/d))

	#----Operators----
	def __add__(self,other:'Vector3') -> 'Vector3':
		return Vector3._from_np(self.value + other.value)
	def __iadd__(self,other:'Vector3') -> 'Vector3':
		return self + other
	def __sub__(self,other:'Vector3') -> 'Vector3':
		return Vector3._from_np(self.value - other.value)
		
	@overload
	def __mul__(self,other:Union[float,int]) -> 'Vector3': ...
	@overload
	def __mul__(self,other:'Vector3') -> 'Vector3': ...
	def __mul__(self,other):
		if isinstance(other, (float,int)):
			return Vector3._from_np(self.value * other)
		elif isinstance(other,Vector3):
			return Vector3._from_np(self._value * other._value)
		else:
			raise ValueError("Expected float/int or Vector3 not "+str(type(other)))
	def __truediv__(self,other:float) -> 'Vector3':
		if math.isclose(other,0.0):
			return Vector3(math.nan, math.nan, math.nan)
		return Vector3._from_np(np.divide(self.value, other))
	
	def __neg__(self) -> 'Vector3':
		return Vector3(-self._value)
		
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