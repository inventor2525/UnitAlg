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
    def from_OCC(trsf : Union[gp_GTrsf, gp_Trsf]):
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
    def coefficients_2d(self):
        m = self._mat
        return [
            mat[0,0],mat[0,1],
            mat[1,0],mat[1,1],
            mat[0,3],mat[1,3]]

    @property
    def coefficients_3d(self):
        m = self._mat
        return [
            mat[0,0],mat[0,1],mat[0,2], 
            mat[1,0],mat[1,1],mat[1,2], 
            mat[2,0],mat[2,1],mat[2,2], 
            mat[0,3],mat[1,3],mat[2,3]]

    @property
    def translation(self) -> np.ndarray:
        return self.mat[0:3,3]
    @translation.setter
    def translation(self, new_translation:Union[np.ndarray, List[float]]) -> None:
        self._mat[0:3,3] = np.array(new_translation)
    
    @property
    def localScale(self) -> np.ndarray:
        m = self._mat
        return LA.norm([m[0:3,0], m[0:3,1], m[0:3,2]], axis=1)
    @localScale.setter
    def localScale(self, new_localScale:Vector3) -> None:
        current_localScale = self.localScale
        self._mat[0:3,0:3] = (self._mat[0:3,0:3]/current_localScale)*new_localScale.value

    @property
    def rotation(self) -> Quaternion:
        rotation_mat = self._mat[0:3,0:3] / self.localScale
        return Quaternion.from_rotation_matrix(rotation_mat)

    @rotation.setter
    def rotation(self, rotation:Quaternion):
        t = gp_Trsf()
        t.SetRotation(rotation.occ_Quaternion)
        self._mat[0:3,0:3] = np.array(Transform.Trsf_to_list( t ))[0:3, 0:3] * self.localScale

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

    def __eq__(self, other) -> bool:
        comparison = self.mat == other.mat
        return comparison.all()

    def __ne__(self, other) -> bool:
        comparison = self.mat != other.mat
        return comparison.all()


if __name__ == '__main__':
    t1 = Transform()
    q1 = Quaternion.from_angle_axis(45,Vector3.up)
    t1.rotation = q1

    print(t1)

    t2 = Transform()
    q2 = Quaternion.from_angle_axis(0,Vector3.up)
    t2.rotation = q2

    print(q1)
    print(q2)
    #print(Quaternion.from_OCC(q1.occ_Quaternion*q2.occ_Quaternion))

    print(t1)
    print(t2)
    print(t1*t2)
    print(math.degrees(t1.rotation.angle), t1.rotation.axis)
    print((t1*t2).rotation.angle_axis)