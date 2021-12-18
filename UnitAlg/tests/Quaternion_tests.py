import math
import unittest
from UnitAlg import *
from math import isclose
import numpy as np

def sq_mag(v:np.ndarray) -> float:
	return v[0]*v[0] + v[1]*v[1] + v[2]*v[2] + v[3]*v[3]

class QuaternionTests(unittest.TestCase):	
	def test00_constructors(self):
		'''
		Tests that the constructors produce a Quaternion 
		correctly, and as a copy of any passed data.
		'''
		q = Quaternion(1,3.14,42,2)
		self.assertTrue(isclose(q.x,1) and isclose(q.y,3.14) and isclose(q.z,42) and isclose(q.w,2))
		
		_in = [-1,3,-5,-2]
		q = Quaternion(_in)
		_in[0] = 2
		_in[1] += _in[2]
		self.assertTrue(isclose(q.x,-1) and isclose(q.y,3) and isclose(q.z,-5) and isclose(q.w,-2))
		
		_in = np.array([99,98,97,-2])
		q = Quaternion(_in)
		_in[0] = 2
		_in[1] += _in[2]
		self.assertTrue(isclose(q.x,99) and isclose(q.y,98) and isclose(q.z,97) and isclose(q.w,0-2))
		
	def test01_properties(self):
		'''Makes sure the Quaternion properties work.'''
		self.assertTrue(False)
	def test02_multiply(self):
		'''Quaternion multiply.'''
		self.assertTrue(False)
	def test03_normalize(self):
		'''Checks Quaternion.normalize.'''
		self.assertTrue(False)
	def test04_angle_axis(self):
		'''
		Checks creation of Quaternion by angle 
		axis and that it can get them too.
		'''
		self.assertTrue(False)
	def test05_inverse(self):
		'''Checks Quaternion.inverse.'''
		self.assertTrue(False)
	def test06_euler(self):
		'''
		Checks creation of Quaternion by euler 
		angles and that it can get them.
		'''
		self.assertTrue(False)
		
if __name__ == 'main':
	unittest.main()