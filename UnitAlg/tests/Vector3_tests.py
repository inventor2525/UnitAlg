import math
import unittest
from UnitAlg import *
import numpy as np
from math import isclose

class Vector3Tests(unittest.TestCase):
	def test00_constructors(self):
		'''
		Tests that the constructors produce a Vector3 
		correctly, and as a copy of any passed data.
		'''
		v = Vector3(1,3.14,42)
		self.assertTrue(isclose(v.x,1) and isclose(v.y,3.14) and isclose(v.z,42))
		
		_in = [-1,3,-5]
		v = Vector3(_in)
		_in[0] = 2
		_in[1] += _in[2]
		self.assertTrue(isclose(v.x,-1) and isclose(v.y,3) and isclose(v.z,-5))
		
		_in = np.array([99,98,97])
		v = Vector3(_in)
		_in[0] = 2
		_in[1] += _in[2]
		self.assertTrue(isclose(v.x,99) and isclose(v.y,98) and isclose(v.z,97))
		
	def test01_properties(self):
		'''Makes sure the Vector3 properties work.'''
		v = Vector3.one
		self.assertTrue(isclose(v.x,1) and isclose(v.y,1) and isclose(v.z,1))
		v.x = 2
		v.y = 3.14
		v.z = 42
		self.assertTrue(isclose(v.x,2))
		self.assertTrue(isclose(v.y,3.14))
		self.assertTrue(isclose(v.z,42))
		
	def test02_add_sub(self):
		'''Checks adding and subtracting Vector3s'''
		v = Vector3(1,2.2,3)+Vector3.one
		self.assertTrue(isclose(v.x,2) and isclose(v.y,3.2) and isclose(v.z,4))
		v = Vector3(1,2,3)+Vector3(-1,-3,-1)
		self.assertTrue(isclose(v.x,0) and isclose(v.y,-1) and isclose(v.z,2))
		
		v = Vector3(1,2.2,3)-Vector3.one
		self.assertTrue(isclose(v.x,0) and isclose(v.y,1.2) and isclose(v.z,2))
		v = Vector3(1,2,3)-Vector3(-1,-3,-1)
		self.assertTrue(isclose(v.x,2) and isclose(v.y,5) and isclose(v.z,4))
		
	def test03_multiply_devide(self):
		'''Checks multiplying and deviding Vector3s'''
		v = Vector3(1,-2.2,3)*1
		self.assertTrue(isclose(v.x,1) and isclose(v.y,-2.2) and isclose(v.z,3))
		v = Vector3(1,2,3)*0
		self.assertTrue(isclose(v.x,0) and isclose(v.y,0) and isclose(v.z,0))
		v = Vector3(1,2,3)*2
		self.assertTrue(isclose(v.x,2) and isclose(v.y,4) and isclose(v.z,6))
		v = Vector3(1,2.2,3)*2.3
		self.assertTrue(isclose(v.x,2.3) and isclose(v.y,2.2*2.3) and isclose(v.z,3*2.3))
		
		v = Vector3(1,-2.2,3)/1
		self.assertTrue(isclose(v.x,1) and isclose(v.y,-2.2) and isclose(v.z,3))
		v = Vector3(1,-2,3)/0
		self.assertTrue(math.isnan(v.x) and math.isnan(v.y) and math.isnan(v.z))
		v = Vector3(1,2,3)/2
		self.assertTrue(isclose(v.x,.5) and isclose(v.y,1) and isclose(v.z,1.5))
		v = Vector3(1,2.2,3)/2.3
		self.assertTrue(isclose(v.x,1/2.3) and isclose(v.y,2.2/2.3) and isclose(v.z,3/2.3))
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
		