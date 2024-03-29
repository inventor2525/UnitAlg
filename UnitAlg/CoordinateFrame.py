from enum import Enum
from typing import Dict, Tuple, Union
import numpy as np

Number = Union[float,int]
TupleVec3 = Tuple[Number,Number,Number]

class CoordinateFrame(Enum):
	Normal_Math=0
	ROS=1
	ROS_IMU=2
	Unity=3
	OpenCV=4
	@staticmethod
	def set(frame: 'CoordinateFrame') -> None:
		'''Sets the coordinate frame for all BaseVectors'''
		from .BaseVector import BaseVector
		BaseVector.coordinate_frame = frame

class Directions(Enum):
	left=1
	right=2
	back=3
	forward=4
	down=5
	up=6
	
class DirectionMap():
	def __init__(self, map:Dict[Directions, TupleVec3]) -> None:
		map[Directions.left] = self.neg(map[Directions.right])
		map[Directions.back] = self.neg(map[Directions.forward])
		map[Directions.down] = self.neg(map[Directions.up])
		self.map = map
	
	@staticmethod
	def neg(x:TupleVec3) -> TupleVec3:
		return (-x[0], -x[1], -x[2])
	
	def __getitem__(self, direction:Directions) -> TupleVec3:
		return self.map[direction]
	
	def rotation_matrix(self) -> np.ndarray:
		'''Returns a 3x3 matrix representing frame'''
		m = self.map
		
		f = np.zeros((3,3), dtype=np.float64)
		f[:,0] = m[Directions.right]
		f[:,1] = m[Directions.forward]
		f[:,2] = m[Directions.up]
		
		return f
		
frame_directions = {
	CoordinateFrame.Normal_Math: DirectionMap({
		Directions.right:(1,0,0),
		Directions.forward:(0,1,0),
		Directions.up:(0,0,1),
	}),
	CoordinateFrame.ROS: DirectionMap({
		Directions.right:(0,-1,0),
		Directions.forward:(1,0,0),
		Directions.up:(0,0,1),
	}),
	CoordinateFrame.ROS_IMU: DirectionMap({
		Directions.right:(0,-1,0),
		Directions.forward:(1,0,0),
		Directions.up:(0,0,-1),
	}),
	CoordinateFrame.Unity: DirectionMap({
		Directions.right:(1,0,0),
		Directions.forward:(0,0,1),
		Directions.up:(0,1,0),
	}),
	CoordinateFrame.OpenCV: DirectionMap({
		Directions.right:(1,0,0),
		Directions.forward:(0,0,1),
		Directions.up:(0,-1,0),
	})
}