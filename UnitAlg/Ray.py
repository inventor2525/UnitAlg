from UnitAlg.Vector3 import Vector3

class Ray():
	def __init__(self, origin:Vector3, direction:Vector3) -> None:
		self.origin = origin
		self.direction = direction