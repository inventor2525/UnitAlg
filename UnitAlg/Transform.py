from .helpers import *
from typing import Union, List
import numpy as np

from .Vector3 import Vector3
from .Quaternion import Quaternion
from OCC.Core.gp import gp_Trsf, gp_GTrsf

class Transform():
    def __init__(self, mat=np.identity(4)):
        self._mat = mat

    @staticmethod
    def Trsf_to_list(trsf : Union[gp_Trsf, gp_GTrsf]) -> List[List[float]]:
        t = trsf.TranslationPart()
        return [
            [trsf.Value(1,1), trsf.Value(1,2), trsf.Value(1,3), t.X()],
            [trsf.Value(2,1), trsf.Value(2,2), trsf.Value(2,3), t.Y()],
            [trsf.Value(3,1), trsf.Value(3,2), trsf.Value(3,3), t.Z()],
            [0,0,0,1]
            ]

    @property
    def mat(self) -> np.ndarray:
        return self._mat
    @mat.setter
    def mat(self, new_mat: Union[np.ndarray, List[List[float]]]):
        self._mat = np.array(new_mat)

    @property
    def GTrsf(self) -> gp_GTrsf:
        return gp_GTrsf(
            gp_Mat(*[float(x) for x in chain.from_iterable(self.mat[0:3,0:3])]), 
            gp_XYZ(*[float(x) for x in self.translation])
            )
    @GTrsf.setter
    def GTrsf(self, new_trsf : Union[gp_Trsf, gp_GTrsf]) -> None:
        self.mat = Trsf_to_list(new_trsf)
    
    @property
    def translation(self) -> np.ndarray:
        return self.mat[0:3,3]
    @translation.setter
    def translation(self, new_translation:Union[np.ndarray, List[float]]) -> None:
        self.mat[0:3,3] = np.array(new_translation)
    
    @property
    def localScale(self) -> np.ndarray:
        m = self.mat
        return LA.norm([m[0:3,0], m[0:3,1], m[0:3,2]], axis=1)
    @localScale.setter
    def localScale(self, new_localScale:Union[np.ndarray, List[float]]) -> None:
        current_localScale = self.localScale
        self.mat[0:3,0:3] = (self.mat[0:3,0:3]/current_localScale)*np.array(new_localScale)

    @property
    def rotation(self) -> Quaternion:
        rotation_mat = self.mat[0:3,0:3] / self.localScale
        return Quaternion.from_rotation_matrix(rotation_mat)

    @rotation.setter
    def rotation(self, rotation:Quaternion):
        t = gp_Trsf()
        t.SetRotation(axis, angle)
        self.mat[0:3,0:3] = np.array(Trsf_to_list( t ))[0:3, 0:3] * self.localScale