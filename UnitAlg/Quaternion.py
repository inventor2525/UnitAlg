from UnitAlg.helpers import *
from typing import Union, List, Tuple
import numpy as np
import math

from OCC.Core.gp import gp_Ax1, gp_Pnt, gp_Vec, gp_Dir, gp_Quaternion, gp_Trsf, gp_GTrsf, gp_XYZ, gp_Mat, gp_OZ
from UnitAlg import Vector3

class Quaternion():
    def __init__(self, x:float, y:float, z:float, w:float):
        self.value = [x,y,z,w]

    @classproperty
    def identity() -> 'Quaternion':
        return Quaternion(0,0,0,1)

    @staticmethod
    def from_OCC(quat : gp_Quaternion) -> 'Quaternion':
        return Quaternion(quat.X(),quat.Y(),quat.Z(),quat.W())

    @staticmethod
    def from_rotation_matrix(mat:Union[np.ndarray, List[List[float]]]) -> 'Quaternion':
        #TODO: do this without OCC:
        quat = gp_Quaternion(gp_Mat(*[float(x) for x in chain.from_iterable(mat)]))
        return Quaternion.from_other(quat)

    @staticmethod
    def from_angle_axis(angle:float, axis:Vector3):
        '''
        Use degrees for the angle
        '''
        quat = gp_Quaternion(axis.occ_Vec, math.radians(angle))
        return Quaternion.from_other(quat)

    #----Casting----
    #TODO: better python interface to use for this? aka "__Something__"
    @staticmethod
    def from_other(value) -> 'Quaternion':
        if isinstance(value, gp_Quaternion):
            return Quaternion(value.X(), value.Y(), value.Z(), value.W())
        if isinstance(value, np.ndarray):
            return Quaternion(*value)

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

    def __str__(self) -> str:
        return str.format('angle:{0} axis:({1},{2},{3}) Quaternion:({4},{5},{6},{7})',math.degrees(self.angle),*self.axis.value,*self._value)
    def __repr__(self) -> str:
        return self.__str__()

    #----Derived Properties----
    def _ensure_derived(self) -> None:
        if not self._derived_updated:
            #TODO: do this without OCC:
            quat = self.occ_Quaternion
            axis = gp_Vec()
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
    def angle_axis(self) -> Tuple[float,float]:
        return self.angle, self._axis

    def inverted(self):
        return Quaternion.from_angle_axis(-(math.degrees(self.angle)), self.axis)

    #----Operators----
    def __eq__(self,other) -> bool:
        #could also use gp_Quaternion.IsEqual() here but would also increase occ dependency
        return all(self.value == other.value)

    def __ne__(self,other) -> bool:
        return any(self.value != other.value)

    def __mul__(self,other: Union[Vector3, 'Quaternion']) -> Union[Vector3, 'Quaternion']:
        quat = self.occ_Quaternion
        if isinstance(other, Quaternion):
            occQuat = quat.Multiplied(other.occ_Quaternion)
            return Quaternion.from_other(occQuat)
        if isinstance(other, Vector3):
            occVec = quat.Multiply(other.occ_Vec)
            return Vector3.from_other(occVec)


    #----OCC conversion functions----
    @property
    def occ_Quaternion(self) -> gp_Quaternion:
        return gp_Quaternion(self._value[0], self._value[1], self._value[2], self._value[3])