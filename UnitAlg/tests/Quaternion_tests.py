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
		q = Quaternion(-2,0,4,3)
		self.assertTrue(isclose(q.x,-2) and isclose(q.y,0) and isclose(q.z,4) and isclose(q.w,3))
		q.x = 2
		q.y = 3.14
		q.z = 42
		q.w = 42.1
		self.assertTrue(isclose(q.x,2))
		self.assertTrue(isclose(q.y,3.14))
		self.assertTrue(isclose(q.z,42))
		self.assertTrue(isclose(q.w,42.1))
		
		_q = np.array([1,2,3,4])
		q.value = _q
		_q[0] = -3
		_q[1] = -9
		_q[2] = -7
		self.assertTrue(isclose(q.x,1) and isclose(q.y,2) and isclose(q.z,3) and isclose(q.w,4))
		
		q.x = 3.14
		q.y = 6.37
		q.z = -4.6
		q.w = 2.3
		self.assertTrue(isclose(q.x,3.14) and isclose(q.y,6.37) and isclose(q.z,-4.6) and isclose(q.w,2.3))
	
	def test02_equality(self):
		'''Checks Quaternion (non) equality.'''
		q1 = Quaternion([4,-6.2,7,1])
		q2 = Quaternion(q1._value+np.array([1e-12,1e-12,1e-12,1e-12]))
		self.assertTrue(q1==q2)
		self.assertFalse(q1!=q2)
		
		q1 = Quaternion([4,-6.2,7,1])
		q2 = Quaternion(q1._value+np.array([1e-10,1e-10,1e-10,1e-10]))
		self.assertTrue(q1!=q2)
		self.assertFalse(q1==q2)
		
	def test03_normalize(self):
		'''Checks Quaternion.normalize.'''
		q = Quaternion(4,2,-1,3)
		self.assertTrue(isclose(q.normalized.magnitude, 1))
		n = np.array([1,22,-3,7])
		q = Quaternion(n)
		m = math.sqrt(sq_mag(n))
		N = n/m
		self.assertTrue(
			isclose(q.normalized.x, N[0]) and
			isclose(q.normalized.y, N[1]) and
			isclose(q.normalized.z, N[2]) and
			isclose(q.normalized.w, N[3])
		)
		q.normalize()
		self.assertTrue(
			isclose(q.x, N[0]) and
			isclose(q.y, N[1]) and
			isclose(q.z, N[2]) and
			isclose(q.w, N[3])
		)
		
	def test04_angle_axis(self):
		'''
		Checks creation of Quaternion by angle 
		axis and that it can get them too.
		'''
		#https://www.energid.com/resources/orientation-calculator
		
		Quaternion.rtol = 1e-10
		Quaternion.atol = 1e-6
		
		def test(angle:float, axis:Vector3, ground_truth:Quaternion) -> None:
			def check(q:Quaternion):
				if math.isclose(q.angle, 0):
					self.assertTrue(math.isclose(q.angle, 0))
				else:
					self.assertTrue(
						(q.axis == axis and math.isclose(q.angle, angle)) or
						(q.axis == -axis and math.isclose(q.angle, -angle))
					)					
					
			q = Quaternion.from_angle_axis(angle, axis)
			_q = q.value
			self.assertTrue(q == ground_truth)
			
			#run again, to make sure we are actually 
			#calculating new angle axis and not relying 
			#on it from previous test:
			q = Quaternion(_q)
			_ = q.angle
			check(q)
			
			q = Quaternion(_q)
			_ = q.axis
			check(q)
			
			q = Quaternion(_q)
			_,__ = q.angle_axis
			check(q)
		test(0, Vector3(1,0,0), Quaternion(0, 0, 0, 1))
		test(math.pi, Vector3(1,0,0), Quaternion(1, 0, 0, 0))
		test(math.pi, Vector3(0,1,0), Quaternion(0, 1, 0, 0))
		test(math.pi, Vector3(0,0,1), Quaternion(0, 0, 1, 0))
		
		_707 = (0.7071070192004544 + 0.7071065431725605)/2
		test(math.pi/2, Vector3(1,0,0), Quaternion(_707, 0, 0, _707))
		test(math.pi/2, Vector3(0,1,0), Quaternion(0, _707, 0, _707))
		test(math.pi/2, Vector3(0,0,1), Quaternion(0, 0, _707, _707))
		
		test(-math.pi/2, Vector3(1,0,0), Quaternion(-_707, 0, 0, _707))
		test(-math.pi/2, Vector3(0,1,0), Quaternion(0, -_707, 0, _707))
		test(-math.pi/2, Vector3(0,0,1), Quaternion(0, 0, -_707, _707))
		
		_408 = 0.40824842788125626
		test(math.pi/2, Vector3(1,1,1).normalized, Quaternion(_408, _408, _408, _707))
		test(-math.pi/2, Vector3(-1,1,1).normalized, Quaternion(_408, -_408, -_408, _707))
		
	def test05_multiply(self):
		'''Quaternion multiply.'''
		def mul(q1:Quaternion, q2:Quaternion):
				#https://www.euclideanspace.com/maths/algebra/realNormedAlgebra/quaternions/code/index.htm
				x =  q1.x * q2.w + q1.y * q2.z - q1.z * q2.y + q1.w * q2.x
				y = -q1.x * q2.z + q1.y * q2.w + q1.z * q2.x + q1.w * q2.y
				z =  q1.x * q2.y - q1.y * q2.x + q1.z * q2.w + q1.w * q2.z
				w = -q1.x * q2.x - q1.y * q2.y - q1.z * q2.z + q1.w * q2.w
				return x,y,z,w
				
		def test(q1:Quaternion, q2:Quaternion):
			self.assertTrue( q1*q2 == Quaternion(mul(q1,q2)))
			self.assertTrue( q2*q1 == Quaternion(mul(q2,q1)))
			if q1 != Quaternion.identity and q2 != Quaternion.identity:
				self.assertTrue( q1*q2 != q2*q1)
		
		test(
			Quaternion.from_angle_axis(math.pi/2, Vector3(1,0,0)),
			Quaternion.from_angle_axis(math.pi/2, Vector3(0,1,0))
		)
		
		test(
			Quaternion.from_angle_axis(math.pi/2, Vector3(.3,7,2).normalized),
			Quaternion.from_angle_axis(math.pi/2, Vector3(4,2,-9).normalized)
		)
		
	def test06_identity(self):
		'''
		Ensures Quaternion.identity is an 
		identity, per Quaternion.multiply.
		'''
		q = Quaternion.from_angle_axis(math.pi/2, Vector3(3,-7,2).normalized)
		self.assertTrue(q*Quaternion.identity == q)
		self.assertTrue(Quaternion.identity*q == q)
		
	def test07_inverse(self):
		'''Checks Quaternion.inverse.'''
		def test(q:Quaternion):
			self.assertTrue(q.inverse * q == Quaternion.identity)
			self.assertTrue(q * q.inverse == Quaternion.identity)
			
		test( Quaternion.from_angle_axis(math.pi/2, Vector3(3,-7,2).normalized) )
		test( Quaternion.from_angle_axis(math.pi/2, Vector3(2,1,-6).normalized) )
		test( Quaternion.from_angle_axis(math.pi/2, Vector3(1,0,0)) )
		test( Quaternion.from_angle_axis(0, Vector3(1,0,0)) )
		test( Quaternion.from_angle_axis(-math.pi, Vector3(0,0,1)) )
		
	def test08_euler(self):
		'''
		Checks creation of Quaternion by euler 
		angles and that it can get them.
		'''
		self.assertTrue(False)
	def test09_rotation_matrix(self):
		'''Tests quaternion from to rotation matrix.'''
		self.assertTrue(False)
if __name__ == 'main':
	unittest.main()