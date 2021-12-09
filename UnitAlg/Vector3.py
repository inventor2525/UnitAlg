from UnitAlg.helpers import *
from typing import Iterator, Union, List
import numpy as np
import math

class Vector3():
    def __init__(self, x:float, y:float, z:float=0):
        self.value = [x,y,z]

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
        self._value = np.array(value)

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
    def sq_magnitude(self) -> float:
        ''' Returns squared length of this vector '''
        return np.linalg.norm(self.value)
        
    def magnitude(self) -> float:
        ''' Returns the length of this vector '''
        return np.linalg.norm(self.value)

    def normalize(self) -> None:
        '''
        Makes this vector have a magnitude of 1 with same direction as before
        Note: this function will change the current vector.  Use normalized if change is undesired
        '''
        self.value = self.value / self.magnitude()

    @property
    def normalized(self) -> 'Vector3':
        '''
        Returns the unit vector for current vector
        Note: this function does NOT affect the current vector.  Use normalize function if change is desired.
        '''
        return self / self.magnitude()

    @staticmethod
    def distance(vector_a:'Vector3', vector_b:'Vector3') -> float:
        ''' Returns the distance between two vectors (same as (a-b).magnitude) '''
        return (vector_a - vector_b).magnitude()
    
    @staticmethod 
    def angle(from_v:'Vector3', to_v:'Vector3') -> float:
        ''' 
        Returns the unsigned angle between 'fromV' and 'toV' in degrees.  
        Angle is never greater than 180.  
        '''
        return math.degrees(math.acos(Vector3.dot(from_v,to_v)/(from_v.magnitude()*to_v.magnitude())))
    
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
        return Vector3._from_np(np.divide(self.value, other))
        
    def __eq__(self,other:'Vector3') -> bool:
        return all(self.value == other.value)
    def __ne__(self,other:'Vector3') -> bool:
        return any(self.value != other.value)
        
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