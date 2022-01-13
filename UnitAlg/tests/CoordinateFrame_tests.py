import math
import unittest
from UnitAlg import *
from UnitAlg.BaseVector import BaseVector
from UnitAlg.CoordinateFrame import *

class Vector3Tests(unittest.TestCase):
	def test00_frame_setting(self):
		self.assertTrue(Vector3.right == Vector3(1,0,0))
		self.assertTrue(Vector3.forward == Vector3(0,1,0))
		self.assertTrue(Vector3.up == Vector3(0,0,1))
		self.assertTrue(Vector3.left == Vector3(-1,0,0))
		self.assertTrue(Vector3.back == Vector3(0,-1,0))
		self.assertTrue(Vector3.down == Vector3(0,0,-1))
		
		BaseVector.coordinate_frame = CoordinateFrame.Unity
		self.assertTrue(Vector3.right == Vector3(1,0,0))
		self.assertTrue(Vector3.up == Vector3(0,1,0))
		self.assertTrue(Vector3.forward == Vector3(0,0,1))
		self.assertTrue(Vector3.left == Vector3(-1,0,0))
		self.assertTrue(Vector3.down == Vector3(0,-1,0))
		self.assertTrue(Vector3.back == Vector3(0,0,-1))
		
		BaseVector.coordinate_frame = CoordinateFrame.ROS
		self.assertTrue(Vector3.right == Vector3(0,-1,0))
		self.assertTrue(Vector3.forward == Vector3(1,0,0))
		self.assertTrue(Vector3.up == Vector3(0,0,1))
		self.assertTrue(Vector3.left == Vector3(0,1,0))
		self.assertTrue(Vector3.back == Vector3(-1,0,0))
		self.assertTrue(Vector3.down == Vector3(0,0,-1))

if __name__ == 'main':
	unittest.main()