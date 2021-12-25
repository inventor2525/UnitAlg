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
	def test01_to_from_Quaternion(self):
		'''
		Tests Transform to and from Quaternion.
		'''
		self.assertTrue(False)
	def test02_multiply(self):
		'''
		Tests multiplying Transforms (and Vectors).
		'''
		self.assertTrue(False)
	def test03_inverse(self):
		'''
		Tests Transform.inverse
		'''
		self.assertTrue(False)
		
	#TODO: Translate, Rotate, Rotate_aout, Scale, TRS, mat property
	#translation localScale rotation properties
	#?rename tofromquaternion to rotation?
if __name__ == 'main':
	unittest.main()