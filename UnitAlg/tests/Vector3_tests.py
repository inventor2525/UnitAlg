import math
import unittest
from UnitAlg import *
import numpy as np
from math import isclose


def sq_mag(v:np.ndarray) -> float:
	return v[0]*v[0] + v[1]*v[1] + v[2]*v[2]
			
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
		
	def test04_magnitude(self):
		'''Checks Vector3.(sq)magnitude / distance'''
		v = Vector3.forward
		self.assertTrue(isclose(v.sq_magnitude,1))
		v = Vector3.one
		self.assertTrue(isclose(v.sq_magnitude,3))
		v = Vector3(0,0,0)
		self.assertTrue(isclose(v.sq_magnitude,0))
		v = Vector3(1,2,3)
		self.assertTrue(isclose(v.sq_magnitude, sq_mag(v.value)))
		v = Vector3([4,6,7])
		self.assertTrue(isclose(v.sq_magnitude, sq_mag(v._value)))
		
		v = Vector3(1,2,3)
		self.assertTrue(isclose(v.magnitude, math.sqrt(sq_mag(v.value)) ))
		v = Vector3([4,6,7])
		self.assertTrue(isclose(v.magnitude, math.sqrt(sq_mag(v._value)) ))
		
		v1 = Vector3([4,-6,7])
		v2 = Vector3([-9,9,8])
		self.assertTrue(isclose(
			Vector3.distance(v1,v2),
			math.sqrt(sq_mag([4+9,-6-9,7-8]))
		))
		
	def test05_normalize(self):
		'''Checks Vector3.normalize(d)'''
		v = Vector3(4,2,-1)
		self.assertTrue(isclose(v.normalized.magnitude, 1))
		n = np.array([4,2,-1])
		m = math.sqrt(sq_mag(n))
		N = n/m
		self.assertTrue(
			isclose(v.normalized.x, N[0]) and
			isclose(v.normalized.y, N[1]) and
			isclose(v.normalized.z, N[2])
		)
		v.normalize()
		self.assertTrue(
			isclose(v.x, N[0]) and
			isclose(v.y, N[1]) and
			isclose(v.z, N[2])
		)
	
	def test06_dot(self):
		'''Checks Vector3.dot'''
		v1 = Vector3([4,-6.2,7])
		v2 = Vector3(-9,9,8.1)
		self.assertTrue(isclose(
			Vector3.dot(v1,v2),
			v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]
		))
		
	def test07_equality(self):
		'''
		Checks that the Vector3 equality functions
		work and can handle very close numbers.
		'''
		v1 = Vector3([4,-6.2,7])
		v2 = Vector3(v1._value)+Vector3(1e-12,1e-12,1e-12)
		self.assertTrue(v1==v2)
		self.assertFalse(v1!=v2)
		
		v1 = Vector3([4,-6.2,7])
		v2 = Vector3(v1._value)+Vector3(1e-10,1e-10,1e-10)
		self.assertTrue(v1!=v2)
		self.assertFalse(v1==v2)
		
	def test08_cross(self):
		'''Checks Vector3.cross'''
		def cross(lhs:Vector3,rhs:Vector3):
			return Vector3(
				lhs.y * rhs.z - lhs.z * rhs.y,
				lhs.z * rhs.x - lhs.x * rhs.z,
				lhs.x * rhs.y - lhs.y * rhs.x)
		v1 = Vector3(3,-1,7).normalized
		v2 = Vector3(1,2,9).normalized
		self.assertTrue(cross(v1,v2) == Vector3.cross(v1,v2))
		
		v1 = Vector3(0,0.02,8).normalized
		v2 = Vector3(-10,0,0.001).normalized
		self.assertTrue(cross(v1,v2) == Vector3.cross(v1,v2))
		
	def test09_angle(self):
		'''Checks Vector3.angle'''
		v1 = Vector3.up
		v2 = Vector3.forward
		self.assertTrue(isclose(Vector3.angle(v1,v2), math.pi/2))
		
		v1 = Vector3.up
		v2 = Vector3.down
		self.assertTrue(isclose(Vector3.angle(v1,v2), math.pi))
		
		v1 = Vector3.up
		v2 = Vector3.up
		self.assertTrue(isclose(Vector3.angle(v1,v2), 0))
		
		v1 = Vector3.back
		v2 = Vector3.left
		self.assertTrue(isclose(Vector3.angle(v1,v2), math.pi/2))
		
	def test11_lerp(self):
		'''Checks Vector3.lerp'''
		self.assertTrue(False)
		
if __name__ == 'main':
	unittest.main()
		