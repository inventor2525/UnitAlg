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