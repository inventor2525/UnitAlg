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

    def Normalize(self) -> None:
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
    def Distance(VectorA:'Vector3', VectorB:'Vector3') -> float:
        ''' Returns the distance between a and b (same as (a-b).magnitude) '''
        return (VectorA-VectorB).magnitude()

    def Angle(fromV:'Vector3', toV:'Vector3'):
        ''' Returns the angle in degrees betwen 'fromV' and 'toV' '''
        #placeholder until I get the dot product function working
        x = 5



    ##TODO:Make functions mimicing Unity's Vector3 class distance
    # dot, cross
    #angle between vectors
    #use Numpy methods where applicable

    #lerp, which is a static method

    #----Operators----
    def __str__(self) -> str:
        return str.format('({0}, {1}, {2})',*self._value)
    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self,other) -> bool:
        comparison = self.value == other.value
        return comparison.all()

    def __ne__(self,other) -> bool:
        comparison = self.value != other.value
        return comparison.all()

    def __add__(self,other) -> 'Vector3':
        return Vector3._from_np(self.value + other.value)

    def __sub__(self,other) -> 'Vector3':
        return Vector3._from_np(self.value - other.value)

    def __mul__(self,other) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3._from_np(self.value * other.value)
        return Vector3._from_np(np.multiply(self.value, other))

    '''
    right multiplication just passes the argument to the left multiplacation function for now
    '''
    def __rmul__(self,other) -> 'Vector3':
        return self.__mul__(other)

    def __truediv__(self,other) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3._from_np(self.value / other.value)
        return Vector3._from_np(np.divide(self.value, other))

    def __iadd__(self,other):
        return self + other

  



    #----OCC conversion functions----
    def occ_AX1(self, origin=[0,0,0]) -> gp_Ax1:
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