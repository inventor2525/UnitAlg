import math
import unittest
from UnitAlg import *
import numpy as np

class Vector3Tests(unittest.TestCase):
	def test00_constructors(self):
		'''
		Tests that the constructors produce a Vector3 
		correctly, and as a copy of any passed data.
		'''
		v = Vector3(1,3.14,42)
		self.assertTrue(v.x==1 and v.y==3.14 and v.z==42)
		
		_in = [-1,3,-5]
		v = Vector3(_in)
		_in[0] = 2
		_in[1] += _in[2]
		self.assertTrue(v.x==-1 and v.y==3 and v.z==-5)
		
		_in = np.array([99,98,97])
		v = Vector3(_in)
		_in[0] = 2
		_in[1] += _in[2]
		self.assertTrue(v.x==99 and v.y==98 and v.z==97)
		
	def test01_properties(self):
		'''Makes sure the Vector3 properties work.'''
		v = Vector3.zero
		v.x = 1
		v.y = 3.14
		v.z = 42
		self.assertTrue(v.x==1)
		self.assertTrue(v.y==3.14)
		self.assertTrue(v.z==42)
		
	def test02_add_sub(self):
		'''Checks adding and subtracting Vector3s'''
		self.assertTrue(False)
	def test03_multiply_devide(self):
		'''Checks multiplying and deviding Vector3s'''
		self.assertTrue(False)
	def test04_cross(self):
		'''Checks Vector3.cross'''
		self.assertTrue(False)
	def test05_dot(self):
		'''Checks Vector3.dot'''
		self.assertTrue(False)
	def test06_magnitude(self):
		'''Checks Vector3.(sq)magnitude / distance'''
		self.assertTrue(False)
	def test07_normalize(self):
		'''Checks Vector3.normalize(d)'''
		self.assertTrue(False)
	def test08_lerp(self):
		'''Checks Vector3.normalize(d)'''
		self.assertTrue(False)
		
if __name__ == 'main':
	unittest.main()
		