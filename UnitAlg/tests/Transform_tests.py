import math
import unittest

from numpy.core.numeric import identity
from UnitAlg import *

translations = [
	Vector3(0,0,0),
	Vector3(0,1,0),
	Vector3(2,0,7.3),
	Vector3(1,-6.2,9.6),
	Vector3(-1,-7,-3)
]
rotations = [
			Quaternion.identity,
			Quaternion(1,0,0,0),
			Quaternion(0,1,0,0),
			Quaternion(0,0,1,0),
			Quaternion(2,4,1,.5).normalized,
			Quaternion(-4,1,8,-.35).normalized,
			Quaternion(-4,1,8,-.35).normalized
]
scales = [
	Vector3(1,1,1),
	Vector3(.3,.6,.2),
	Vector3(3,1,-7),
	Vector3(-3,1,-7),
	Vector3(1,1,-1),
	Vector3(1,-1,-1)
]

def quaternion_to_transform(q:Quaternion, scale:Vector3=Vector3(1,1,1), translation:Vector3=Vector3(0,0,0)) -> Transform:
	x = (q * Vector3(1,0,0))*scale.x
	y = (q * Vector3(0,1,0))*scale.y
	z = (q * Vector3(0,0,1))*scale.z
	return Transform([
		[x.x, y.x, z.x, translation.x],
		[x.y, y.y, z.y, translation.y],
		[x.z, y.z, z.z, translation.z],
		[0,   0,   0,   1]
	])
			
class TransformTests(unittest.TestCase):
	def test00_constructors(self):
		'''
		Tests that the constructors produce a Transform 
		correctly, and as a copy of any passed data.
		'''
		for scale in scales:
			for rotation in rotations:
				for translation in translations:
					t = Transform.Scale(scale)
					self.assertTrue(t == Transform([
						[scale.x, 0,       0,       0],
						[0,       scale.y, 0,       0],
						[0,       0,       scale.z, 0],
						[0,       0,       0,       1],
					]))
					t = Transform.Rotate(rotation)
					self.assertTrue(t == quaternion_to_transform(rotation))
					
					t = Transform.Translate(translation)
					self.assertTrue(t == Transform([
						[1, 0, 0, translation.x],
						[0, 1, 0, translation.y],
						[0, 0, 1, translation.z],
						[0, 0, 0, 1],
					]))
					
		
	def test01_equality(self):
		'''
		Checks that the Transform equality functions work.
		'''
		Transform.rtol = 1e-10
		Transform.atol = 1e-6
		
		def check_eq(t1:Transform, t2:Transform):
			self.assertTrue(t1 == t2)
			self.assertFalse(t1 != t2)
		def check_neq(t1:Transform, t2:Transform):
			self.assertTrue(t1 != t2)
			self.assertFalse(t1 == t2)
			
		check_eq(Transform.identity, Transform.identity)
		
		check_neq(Transform.identity, Transform(Transform.identity.mat*1.00001))
		check_eq( Transform.identity, Transform(Transform.identity.mat*1.00000001))
		
		check_neq(Transform.identity, Transform([
			[1,0,0,0.00001],
			[0,1,0,0],
			[0,0,1,0],
			[0,0,0,1]
		]))
		check_eq(Transform.identity, Transform([
			[1,0,0,0.000001],
			[0,1,0,0],
			[0,0,1,0],
			[0,0,0,1]
		]))
		
	def test02_to_from_Quaternion(self):
		'''
		Tests Transform to and from Quaternion.
		'''
		def test(q:Quaternion):
			t = quaternion_to_transform(q)
			_q = Quaternion.from_rotation_matrix(t.mat)
			self.assertTrue(_q == q)
			self.assertTrue(Transform.Rotate(q) == t)
		test(Quaternion.identity)
		test(Quaternion(1,0,0,0))
		test(Quaternion(0,1,0,0))
		test(Quaternion(0,0,1,0))
		
		test(Quaternion(2,4,1,.5).normalized)
		test(Quaternion(-1,2,-9,7).normalized)
		
		def test(q:Quaternion, scale:Vector3):
			t = quaternion_to_transform(q, scale)
			t_normalized = quaternion_to_transform(q)
			self.assertTrue(Transform(t.rotation_mat) == Transform(t_normalized.rotation_mat))
			
			_q = t.rotation
			self.assertTrue(math.isclose(_q.magnitude,1))
			self.assertTrue(_q == q)
		test(Quaternion(2,4,1,.5).normalized, Vector3(3,6,2))
		test(Quaternion(-4,1,8,-.35).normalized, Vector3(1,9,7))
		test(Quaternion(-4,1,8,-.35).normalized, Vector3(3,2,4))
		
	def test03_multiply(self):
		'''
		Tests multiplying Transforms (and Vectors).
		'''
		def mul_TR_transform_vector3(t:Transform, v:Vector3) -> Vector3:
			x = t._mat[0,0]*v.x + t._mat[0,1]*v.y + t._mat[0,2]*v.z #+ t._mat[0,3]*v.w
			y = t._mat[1,0]*v.x + t._mat[1,1]*v.y + t._mat[1,2]*v.z #+ t._mat[1,3]*v.w
			z = t._mat[2,0]*v.x + t._mat[2,1]*v.y + t._mat[2,2]*v.z #+ t._mat[2,3]*v.w
			#w= t._mat[3,0]*v.x + t._mat[3,1]*v.y + t._mat[3,2]*v.z #+ t._mat[3,3]*v.w
			return Vector3(x,y,z)
		def test_rotation_only(q:Quaternion, v:Vector3) -> None:
			t = Transform.Rotate(q)
			self.assertTrue(t == quaternion_to_transform(q))
			self.assertTrue(mul_TR_transform_vector3(t,v) == q*v)
			self.assertTrue(mul_TR_transform_vector3(t,v) == t*v)
			self.assertTrue(q*v == t*v)
		
		for q in rotations:
			test_rotation_only(q, Vector3(3,6,2))
		
		def test_translation_scale_seperate(modifier:Vector3, v:Vector3) -> None:
			t = Transform.Translate(modifier)
			self.assertTrue(t*v == v+modifier)
			
			t = Transform.Scale(modifier)
			self.assertTrue(t*v == modifier*v)
		
		test_translation_scale_seperate(Vector3(0,0,0), Vector3(3,6,2))
		test_translation_scale_seperate(Vector3(0,1,0), Vector3(3,6,2))
		test_translation_scale_seperate(Vector3(2,0,7.3), Vector3(3,6,2))
		test_translation_scale_seperate(Vector3(1,-6.2,9.6), Vector3(3,6,2))
		test_translation_scale_seperate(Vector3(-1,-7,-3), Vector3(3,6,2))
		
		def test_TRS(translation:Vector3, rotation:Quaternion, scale:Vector3, v:Vector3) -> None:
			t_test = quaternion_to_transform(rotation, scale, translation)
			t = Transform.TRS(translation, rotation, scale)
			self.assertTrue(t_test == t)
			
			self.assertTrue(t*v == rotation*(v*scale)+translation)
			
			#test transform*transform:
			_t = Transform.Translate(translation)
			_r = Transform.Rotate(rotation)
			_s = Transform.Scale(scale)
			self.assertTrue(t == _t*_r*_s )
			
		for s in scales:
			for q in rotations:
				for t in translations:
					test_TRS(t, q, s, Vector3(3,6,2))
		
	def test04_inverse(self):
		'''
		Tests Transform.inverse
		'''
		def test(t:Transform):
			self.assertTrue(t * t.inverse == Transform.identity)
			self.assertTrue(t.inverse * t == Transform.identity)
		
		for s in scales:
			for q in rotations:
				for t in translations:
					test(Transform.TRS(t, q, s))
					
if __name__ == 'main':
	unittest.main()