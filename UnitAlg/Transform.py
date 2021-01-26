from UnitAlg.helpers import *
from typing import Union, List
import numpy as np
import numpy.linalg as LA
import math

from UnitAlg import Vector3, Quaternion
from OCC.Core.gp import gp_Trsf, gp_GTrsf, gp_Mat, gp_XYZ

class Transform():
    def __init__(self, mat=np.identity(4)):
        self.mat = mat

    @staticmethod
    def Trsf_to_list(trsf : Union[gp_Trsf, gp_GTrsf]) -> List[List[float]]:
        t = trsf.TranslationPart()
        return [
            [trsf.Value(1,1), trsf.Value(1,2), trsf.Value(1,3), t.X()],
            [trsf.Value(2,1), trsf.Value(2,2), trsf.Value(2,3), t.Y()],
            [trsf.Value(3,1), trsf.Value(3,2), trsf.Value(3,3), t.Z()],
            [0,0,0,1]
            ]

    @staticmethod
    def from_OCC(trsf : Union[gp_GTrsf, gp_Trsf]) -> 'Transform':
        return Transform(np.array(Transform.Trsf_to_list(trsf)))

    @property
    def mat(self) -> np.ndarray:
        return np.array(self._mat)
    @mat.setter
    def mat(self, new_mat: Union[np.ndarray, List[List[float]]]):
        self._mat = np.array(new_mat)

    @property
    def GTrsf(self) -> gp_GTrsf:
        return gp_GTrsf(
            gp_Mat(*[float(x) for x in chain.from_iterable(self._mat[0:3,0:3])]), 
            gp_XYZ(*[float(x) for x in self.translation])
            )
    @GTrsf.setter
    def GTrsf(self, new_trsf : Union[gp_Trsf, gp_GTrsf]) -> None:
        self.mat = Trsf_to_list(new_trsf)
    
    @property
    def coefficients_2d(self) -> List[List[float]]:
        m = self._mat
        return [
            m[0,0],m[0,1],
            m[1,0],m[1,1],
            m[0,3],m[1,3]]

    @property
    def coefficients_3d(self) -> List[List[float]]:
        m = self._mat
        return [
            m[0,0],m[0,1],m[0,2], 
            m[1,0],m[1,1],m[1,2], 
            m[2,0],m[2,1],m[2,2], 
            m[0,3],m[1,3],m[2,3]]

    @property
    def translation(self) -> Vector3:
        return Vector3._from_np(self.mat[0:3,3])
    @translation.setter
    def translation(self, new_translation: Vector3) -> None:
        self._mat[0:3,3] = new_translation.value
    
    @property
    def localScale(self) -> Vector3:
        m = self._mat
        return Vector3._from_np(LA.norm([m[0:3,0], m[0:3,1], m[0:3,2]], axis=1))
    @localScale.setter
    def localScale(self, new_localScale:Vector3) -> None:
        current_localScale = self.localScale
        self._mat[0:3,0:3] = (self._mat[0:3,0:3]/current_localScale.value)*new_localScale.value

    @property
    def rotation(self) -> Quaternion:
        rotation_mat = self._mat[0:3,0:3] / self.localScale.value
        return Quaternion.from_rotation_matrix(rotation_mat)

    @rotation.setter
    def rotation(self, rotation:Quaternion):
        t = gp_Trsf()
        t.SetRotation(rotation.occ_Quaternion)
        self._mat[0:3,0:3] = np.array(Transform.Trsf_to_list( t ))[0:3, 0:3] * self.localScale.value

    @property
    def inverse(self) -> 'Transform':
         return Transform(np.linalg.inv(self.mat))
         
    #----Operators----
    def __str__(self) -> str:
        return self._mat.__str__()
    def __repr__(self) -> str:
        return self._mat.__repr__()

    def __mul__(self, other:'Transform') -> 'Transform':
        #return Transform(self._mat*other._mat.T)
        return Transform.from_OCC(other.GTrsf*self.GTrsf)
        
    def __rmul__(self, other:'Transform') -> 'Transform':
        #return Transform(other._mat*self._mat.T)
        return Transform.from_OCC(self.GTrsf*other.GTrsf)

    def __eq__(self,other) -> bool:
        return all(self.mat == other.mat)

    def __ne__(self,other) -> bool:
        return any(self.mat != other.mat)

if __name__ == '__main__':
    t1 = Transform()
    q1 = Quaternion.from_angle_axis(45,Vector3.up)
    t1.rotation = q1
    print("1")
    print(t1)
    print("2")
    t2 = Transform()
    q2 = Quaternion.from_angle_axis(0,Vector3.up)
    t2.rotation = q2

    print(q1)
    print("3")
    print(q2)
    print("4")
    #print(Quaternion.from_OCC(q1.occ_Quaternion*q2.occ_Quaternion))

    print(t1)
    print("5")
    print(t2)
    print("6")
    print(t1*t2)
    print("7")
    print(math.degrees(t1.rotation.angle), t1.rotation.axis)
    print("8")
    print((t1*t2).rotation.angle_axis)
    print("9")