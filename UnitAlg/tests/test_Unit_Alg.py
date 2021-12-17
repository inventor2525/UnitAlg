import math
import unittest
from UnitAlg import *

class UnitAlgTests(unittest.TestCase):	
	def test01_non_rotation_test(self):
		vec = Vector3(0,0,1)
		print("\n",vec, type(vec))
		rot = Quaternion(0,0,0.7,0.7)
		rotated_vec = rot * vec
		self.assertEqual(rotated_vec, Vector3(0,0,1))
		
	def test02_rotation_test(self):
		vec = Vector3(1,0,0)
		print("\n",vec, type(vec))
		rt22 = math.sqrt(2)/2
		rot = Quaternion(0,0,rt22,rt22)
		rotated_vec = rot * vec
		print(rotated_vec)
		self.assertTrue((rotated_vec - Vector3(0,1,0)).magnitude() < 0.001)
		
if __name__ == 'main':
	vec = Vector3.forward
	print(vec, type(vec))
	unittest.main()
		