from UnitAlg import Vector3
from OCC.Core.gp import gp_Pln, gp_Pnt, gp_Dir

#class for plane objects in UnitAlg.  Features methods to convert between UnitAlg and OOC's version of planes.

#class to start plane
class Plane():
    def __init__(self, point:'Vector3', direction:'Vector3'):
        self.point = point
        self.direction = direction  

    @staticmethod
    def from_OCC(gpPlane:gp_Pln):
        point = Vector3.from_other(gpPlane.Location())
        direction = Vector3.from_other(gpPlane.Position().Direction())
        return Plane(point, direction)

    #----Main Properties----
    @property
    def point(self) -> 'Vector3':
        return self._point
    @point.setter
    def point(self, point:'Vector3') -> None:
        self._point = point

    @property
    def direction(self) -> 'Vector3':
        return self._direction
    @direction.setter
    def direction(self, direction:'Vector3') -> None:
        self._direction = direction

    #----Operators-----
        
    def __str__(self) -> str:
        return str.format('origin of plane:{0}\ndirection of plane:{1}',self.point, self.direction)
    def __repr__(self) -> str:
        return self.__str__()

    #----OCC conversion functions----
    @property
    def occ_Plane(self):
        #create gp_Dir object and gp_Pnt object, then send as parameters
        pnt = self.point.occ_Pnt
        dir = self.direction.occ_Dir
        return gp_Pln(pnt, dir)
