from UnitAlg.helpers import *
from typing import Union, List, overload
import numpy as np
import numpy.linalg as LA
import math

from UnitAlg import Vector3, Quaternion
from UnitAlg.CoordinateFrame import *

class Transform():
	rtol=1e-12
	atol=1e-11
	
	def __init__(self, mat:np.ndarray=np.identity(4)):
		self.mat = mat
	
	@staticmethod
	def conversion_from_to(frame1:CoordinateFrame, frame2:CoordinateFrame) -> 'Transform':
		f1 = Transform(frame_directions[frame1].rotation_matrix())
		f2 = Transform(frame_directions[frame2].rotation_matrix())
		return  f2* f1.inverse
	
	@classproperty
	def identity() -> 'Transform':
		return Transform()
	
	@staticmethod
	def from_rows(x:Vector3, y:Vector3, z:Vector3, pos:Vector3=Vector3.zero) -> 'Transform':
		return Transform([ #TODO: do this with numpy for speed, and test it with this
			[x.x, y.x, z.x, pos.x],
			[x.y, y.y, z.y, pos.y],
			[x.z, y.z, z.z, pos.z],
			[0,0,0,1]
		])
	@staticmethod
	def from_3x3list(mat:List[float], pos:Vector3=Vector3.zero) -> 'Transform':
		'''
		Takes in a single dimentional list of the top left 3x3 rotation/projection matrix,
		in row major order, and sets the last column to [*pos,1].'''
		return Transform([ #TODO: do this with numpy for speed, and test it with this
			[mat[0], mat[1], mat[2], pos.x],
			[mat[3], mat[4], mat[5], pos.y],
			[mat[6], mat[7], mat[8], pos.z],
			[0,0,0,1]
		])
		
	@staticmethod
	def Translate(translation :Vector3) -> 'Transform':
		t = Transform()
		t.translation = translation
		return t
	
	@staticmethod
	def Rotate(rotation :Quaternion) -> 'Transform':
		t = Transform()
		t.rotation = rotation
		return t
	
	@staticmethod
	def Rotate_about(rotation :Quaternion, origin :Vector3) -> 'Transform':
		return Transform.Translate(origin*-1)*Transform.Rotate(rotation)*Transform.Translate(origin)

	@staticmethod
	def Scale(scale :Vector3) -> 'Transform':
		t = Transform()
		t.localScale = scale
		return t
	
	@staticmethod
	def TRS(translation :Vector3, rotation :Quaternion, scale :Vector3) -> 'Transform':
		t = Transform()
		t.translation = translation
		t.rotation = rotation
		t.localScale = scale
		return t
		
	@staticmethod
	def TR(translation :Vector3, rotation :Quaternion) -> 'Transform':
		t = Transform()
		t.translation = translation
		t.rotation = rotation
		return t
		
	@property
	def mat(self) -> np.ndarray:
		return np.array(self._mat)
	@mat.setter
	def mat(self, new_mat: Union[np.ndarray, List[List[float]]]):
		mat = np.array(new_mat, dtype=np.float64)
		
		if mat.shape == (4,4):
			self._mat = mat
		elif mat.shape == (3,3):
			m = np.identity(4)
			m[0:3,0:3] = mat
			self._mat = m
		else:
			raise ValueError("Expected 4x4 or 3x3 matrix, got "+mat.shape)

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
			#TODO: move document or clean up these shapely?? or OCC? support functions

	@property
	def translation(self) -> Vector3:
		return Vector3._from_np(self.mat[0:3,3])
	@translation.setter
	def translation(self, new_translation: Vector3) -> None:
		self._mat[0:3,3] = new_translation.value
	
	@property
	def localScale(self) -> Vector3:
		'''
		Gets the positive local scale from the transform matrix, does not handle negative scale.
		'''
		m = self._mat
		return Vector3._from_np(LA.norm([m[0:3,0], m[0:3,1], m[0:3,2]], axis=1))
	@localScale.setter
	def localScale(self, new_localScale:Vector3) -> None:
		current_localScale = self.localScale
		self._mat[0:3,0:3] = (self._mat[0:3,0:3]/current_localScale.value)*new_localScale.value
	
	@property
	def rotation_mat(self) -> np.ndarray:
		return self._mat[0:3,0:3] / self.localScale._value
		
	@property
	def rotation(self) -> Quaternion:
		return Quaternion.from_rotation_matrix(self.rotation_mat).normalized

	@rotation.setter
	def rotation(self, rotation:Quaternion):
		#from rospy tf.transformations
		q = np.array(rotation._value, dtype=np.float64, copy=True)
		nq = np.dot(q, q)
		if nq < epsilon:
			return np.identity(4)
		q *= math.sqrt(2.0 / nq)
		q = np.outer(q, q)
		rot_mat = np.array((
			(1.0-q[1, 1]-q[2, 2],     q[0, 1]-q[2, 3],     q[0, 2]+q[1, 3], 0.0),
			(    q[0, 1]+q[2, 3], 1.0-q[0, 0]-q[2, 2],     q[1, 2]-q[0, 3], 0.0),
			(    q[0, 2]-q[1, 3],     q[1, 2]+q[0, 3], 1.0-q[0, 0]-q[1, 1], 0.0),
			(                0.0,                 0.0,                 0.0, 1.0)
			), dtype=np.float64)
			
		self._mat[0:3,0:3] = rot_mat[0:3, 0:3] * self.localScale._value

	@property
	def inverse(self) -> 'Transform':
		 return Transform(LA.inv(self._mat))
		 
	@property
	def transpose(self) -> 'Transform':
		 return Transform(self._mat.T)
		 
	#----Operators----
	def __str__(self) -> str:
		return self._mat.__str__()
	def __repr__(self) -> str:
		return self._mat.__repr__()
	
	@overload
	def __mul__(self, other:'Transform') -> 'Transform': ...
	@overload
	def __mul__(self, other:Vector3) -> Vector3: ...
	def __mul__(self, other):
		if isinstance(other, Transform):
			return Transform(np.matmul( self._mat, other._mat) )
		elif isinstance(other, Vector3):
			v4 = np.array([*other._value, 1])
			v4 = np.dot(self._mat,v4)
			return Vector3(v4[:3])
		else:
			raise ValueError("Transforms can only be multiplied by Vector3's and Transforms, not "+type(other))
	def __rmul__(self, other:'Transform') -> 'Transform':
		return Transform(np.matmul( other._mat, self._mat) )

	def __eq__(self,other:'Transform') -> bool:
		#TODO: speed improvement, flatten coppies
		return all(np.isclose(self._mat.flatten(), other._mat.flatten(), rtol=self.rtol, atol=self.atol))

	def __ne__(self,other:'Transform') -> bool:
		return any(not np.isclose(m1,m2, rtol=self.rtol, atol=self.atol) for m1,m2 in zip(self._mat.flatten(), other._mat.flatten()))

if __name__ == '__main__':
	print(Quaternion.from_euler(0,0,math.pi/2))
	print(Vector3(0,1,0))
	t = Transform.Rotate_about(Quaternion.from_euler(0,0,math.pi/2),Vector3(0,1,0))
	print(t)
	print(t*Vector3(1,0,0))
	print('----')
	
	print(Transform(np.array([
		[1,0,0,0],
		[0,2,0,0],
		[0,0,1,0],
		[0,0,0,1]
	]))*Transform(np.array([
		[1,0,0,1],
		[0,1,0,2],
		[0,0,1,3],
		[0,0,0,1]
	])))
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