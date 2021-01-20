from UnitAlg.helpers import *
from typing import Union, List
import numpy as np
import math

from OCC.Core.gp import gp_Pnt, gp_Vec, gp_Dir, gp_Trsf, gp_XYZ, gp_Ax1

class Vector3():
    def __init__(self, x:float, y:float, z:float):
        self.value = [x,y,z]

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
    '''
    Returns the length of this vector
    '''
    def magnitude(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    '''
    Makes this vector have a magnitude of 1 with same direction as before
    Note: this function will change the current vector.  Use normalized if change is undesired
    '''
    def Normalize(self):
        self.value = self.value / self.magnitude()

    '''
    Returns the unit vector for current vector
    Note: this function does NOT affect the current vector.  Use Normalized function if change is desired.
    '''
    def normalized(self):
        return self.value/self.magnitude()


    ##TODO:Make functions mimicing Unity's Vector3 class magnitude, distance, normalized
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
        return Vector3.from_other(self.value + other.value)

    def __sub__(self,other) -> 'Vector3':
        return Vector3.from_other(self.value - other.value)

    def __mul__(self,other) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3.from_other(self.value * other.value)
        return Vector3.from_other(np.multiply(self.value, other))

    '''
    right multiplication just passes the argument to the left multiplacation function for now
    '''
    def __rmul__(self,other) -> 'Vector3':
        return self.__mul__(other)

    def __truediv__(self,other) -> 'Vector3':
        if isinstance(other, Vector3):
            return Vector3.from_other(self.value / other.value)
        return Vector3.from_other(np.divide(self.value, other))

    # This doesn't work just yet...this is called when '+=' operator is called
    # doesn't work because the type is not retained and changes to NoneType
    def __iadd__(self,other):
        if isinstance(other, Vector3):
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