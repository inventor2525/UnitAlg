import math
import unittest
from UnitAlg import *

class TransformTests(unittest.TestCase):
	def test00_constructors(self):
		'''
		Tests that the constructors produce a Transform 
		correctly, and as a copy of any passed data.
		'''
		self.assertTrue(False)
		
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
			x = q * Vector3(1,0,0)
			y = q * Vector3(0,1,0)
			z = q * Vector3(0,0,1)
			t = Transform([
				[x.x, y.x, z.x, 0],
				[x.y, y.y, z.y, 0],
				[x.z, y.z, z.z, 0],
				[0,   0,   0,   1]
			])
			_q = Quaternion.from_rotation_matrix(t.mat)
			self.assertTrue(_q == q)
			self.assertTrue(Transform.Rotate(q) == t)
		test(Quaternion.identity)
		test(Quaternion(1,0,0,0))
		test(Quaternion(0,1,0,0))
		test(Quaternion(0,0,1,0))
		
		test(Quaternion(2,4,1,.5).normalized)
		test(Quaternion(-1,2,-9,7).normalized)
		
	def test03_multiply(self):
		'''
		Tests multiplying Transforms (and Vectors).
		'''
		self.assertTrue(False)
	def test04_inverse(self):
		'''
		Tests Transform.inverse
		'''
		self.assertTrue(False)
		
	#TODO: Translate, Rotate, Rotate_aout, Scale, TRS, mat property
	#translation localScale rotation properties
	#?rename tofromquaternion to rotation?
if __name__ == 'main':
	unittest.main()