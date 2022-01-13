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
		
	def test01_frame_conversion(self):
		t = Transform.conversion_from_to(CoordinateFrame.Normal_Math, CoordinateFrame.Unity)
		self.assertTrue(t*Vector3(1,0,0) == Vector3(1,0,0))
		self.assertTrue(t*Vector3(0,1,0) == Vector3(0,0,1))
		self.assertTrue(t*Vector3(0,0,1) == Vector3(0,1,0))
		t = Transform.conversion_from_to(CoordinateFrame.Unity, CoordinateFrame.Normal_Math)
		self.assertTrue(t*Vector3(1,0,0) == Vector3(1,0,0))
		self.assertTrue(t*Vector3(0,1,0) == Vector3(0,0,1))
		self.assertTrue(t*Vector3(0,0,1) == Vector3(0,1,0))
		
		t = Transform.conversion_from_to(CoordinateFrame.Normal_Math, CoordinateFrame.ROS)
		self.assertTrue(t*Vector3(1,0,0) == Vector3(0,-1,0))
		self.assertTrue(t*Vector3(0,1,0) == Vector3(1,0,0))
		self.assertTrue(t*Vector3(0,0,1) == Vector3(0,0,1))
		t = Transform.conversion_from_to(CoordinateFrame.ROS, CoordinateFrame.Normal_Math)
		self.assertTrue(t*Vector3(1,0,0) == Vector3(0,1,0))
		self.assertTrue(t*Vector3(0,1,0) == Vector3(-1,0,0))
		self.assertTrue(t*Vector3(0,0,1) == Vector3(0,0,1))
		
		t = Transform.conversion_from_to(CoordinateFrame.Unity, CoordinateFrame.ROS)
		self.assertTrue(t*Vector3(1,0,0) == Vector3(0,-1,0))
		self.assertTrue(t*Vector3(0,1,0) == Vector3(0,0,1))
		self.assertTrue(t*Vector3(0,0,1) == Vector3(1,0,0))
		t = Transform.conversion_from_to(CoordinateFrame.ROS, CoordinateFrame.Unity)
		self.assertTrue(t*Vector3(1,0,0) == Vector3(0,0,1))
		self.assertTrue(t*Vector3(0,1,0) == Vector3(-1,0,0))
		self.assertTrue(t*Vector3(0,0,1) == Vector3(0,1,0))
		
		t = Transform.conversion_from_to(CoordinateFrame.OpenCV, CoordinateFrame.ROS)
		self.assertTrue(t*Vector3(1,0,0) == Vector3(0,-1,0))
		self.assertTrue(t*Vector3(0,1,0) == Vector3(0,0,-1))
		self.assertTrue(t*Vector3(0,0,1) == Vector3(1,0,0))
		t = Transform.conversion_from_to(CoordinateFrame.ROS, CoordinateFrame.OpenCV)
		self.assertTrue(t*Vector3(1,0,0) == Vector3(0,0,1))
		self.assertTrue(t*Vector3(0,1,0) == Vector3(-1,0,0))
		self.assertTrue(t*Vector3(0,0,1) == Vector3(0,-1,0))

if __name__ == 'main':
	unittest.main()