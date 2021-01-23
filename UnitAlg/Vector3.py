from UnitAlg.helpers import *
from typing import Union, List
import numpy as np
import math

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir, gp_Trsf, gp_XYZ, gp_Ax1

class Vector3():
    def __init__(self, x:float, y:float, z:float):
        self.value = [x,y,z]

    @staticmethod
    def _from_np(value: np.ndarray) -> 'Vector3':
        newArr = Vector3.__new__(Vector3)
        newArr._value = value
        return newArr

    #----Common values----
    @classproperty
    def zero() -> 'Vector3':
        return Vector3(0,0,0)
    
    @classproperty
    def left() -> 'Vector3':
        return Vector3(-1,0,0)
    
    @classproperty
    def right() -> 'Vector3':
        return Vector3(1,0,0)

    @classproperty
    def down() -> 'Vector3':
        return Vector3(0,-1,0)

    @classproperty
    def up() -> 'Vector3':
        return Vector3(0,1,0)

    @classproperty
    def back() -> 'Vector3':
        return Vector3(0,0,-1)

    @classproperty
    def forward() -> 'Vector3':
        return Vector3(0,0,1)

    #----Casting----
    #TODO: better python interface to use for this? aka "__Something__"
    @staticmethod
    def from_other(value) -> 'Vector3':
        if isinstance(value, (gp_Vec, gp_Pnt, gp_Dir, gp_XYZ)):
            return Vector3(value.X(), value.Y(), value.Z())
        if isinstance(value, np.ndarray):
            return Vector3(*value)

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

    #----Functions----
    def magnitude(self) -> float:
        ''' Returns the length of this vector '''
        return np.linalg.norm(self.value)

    def normalize(self) -> None:
        '''
        Makes this vector have a magnitude of 1 with same direction as before
        Note: this function will change the current vector.  Use normalized if change is undesired
        '''
        self.value = self.value / self.magnitude()

    @staticmethod
    def normalized(self) -> 'Vector3':
        '''
        Returns the unit vector for current vector
        Note: this function does NOT affect the current vector.  Use Normalized function if change is desired.
        '''
        return Vector3.from_other(self.value/self.magnitude())

    @staticmethod
    def distance(vector_a:'Vector3', vector_b:'Vector3') -> float:
        ''' Returns the distance between two vectors (same as (a-b).magnitude) '''
        return (vector_a - vector_b).magnitude()

    @staticmethod
    def dot(vector_a:'Vector3', vector_b:'Vector3'):
        ''' Dot product between two vectors '''
        return np.dot(vector_a.value,vector_b.value)

    @staticmethod
    def cross(vector_a,vector_b):
        '''Cross product between two vectors '''
        return np.cross(vector_a.value,vector_b.value)

    def angle(from_v:'Vector3', to_v:'Vector3'):
        ''' 
        Returns the unsigned angle between 'fromV' and 'toV' in degrees.  
        Angle is never greater than 180.  
        '''
        return math.degrees(math.acos(Vector3.dot(from_v,to_v)/(from_v.magnitude()*to_v.magnitude())))



    ##TODO:Make functions mimicing Unity's Vector3 class distance
       #lerp, which is a static method

    #----Operators----
    def __str__(self) -> str:
        return str.format('({0}, {1}, {2})',*self._value)
    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self,other:'Vector3') -> bool:
        comparison = self.value == other.value
        return comparison.all()

    def __ne__(self,other:'Vector3') -> bool:
        comparison = self.value != other.value
        return comparison.all()

    def __add__(self,other:'Vector3') -> 'Vector3':
        return Vector3._from_np(self.value + other.value)

    def __sub__(self,other:'Vector3') -> 'Vector3':
        return Vector3._from_np(self.value - other.value)

    def __mul__(self,other:float) -> 'Vector3':
        return Vector3._from_np(self.value * other)

    def __truediv__(self,other:float) -> 'Vector3':
        return Vector3._from_np(np.divide(self.value, other))

    def __iadd__(self,other):
        return self + other

    #----OCC conversion functions----
    def occ_Ax1(self, origin=[0,0,0]) -> gp_Ax1:
        return gp_Ax1(Vector3(origin).occ_Pnt, self.occ_Dir)

    @property
    def occ_Vec(self) -> gp_Vec:
        return gp_Vec(float(self._value[0]), float(self._value[1]), float(self._value[2]))

    @property
    def occ_Dir(self) -> gp_Dir:
        return gp_Dir(float(self._value[0]), float(self._value[1]), float(self._value[2]))

    @property
    def occ_Pnt(self) -> gp_Pnt:
        return gp_Pnt(float(self._value[0]), float(self._value[1]), float(self._value[2]))