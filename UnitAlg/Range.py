class Range():
	def __init__(self, min:float, max:float) -> None:
		self.min = min
		self.max = max
		self.range = max - min
	
	@classmethod
	def from_point(cls, point:float) -> 'Range':
		return cls(point, point)
		
	@classmethod
	def from_center_delta(cls, center:float, delta:float) -> 'Range':
		return cls(center - delta, center + delta)
	
	def overlaps(self, other:'Range') -> bool:
		return self.min <= other.max and self.max >= other.min
	
	def overlapping(self, other:'Range') -> 'Range':
		"""
		Returns the overlapping range between this and the other range,
		unless the ranges do not overlap, in which case it returns a range
		still contained within this range but closest to the other range.
		"""
		if self.min > other.max:
			return Range.from_point(self.min)
		elif self.max < other.min:
			return Range.from_point(self.max)
		return Range(max(self.min, other.min), min(self.max, other.max))
	
	def clamp(self, value:float) -> float:
		return max(min(value, self.max), self.min)
	
	def __mul__(self, value:float) -> 'Range':
		return Range(self.min * value, self.max * value)
	def __rmul__(self, value:float) -> 'Range':
		return self * value
	def __truediv__(self, value:float) -> 'Range':
		return Range(self.min / value, self.max / value)
		
	def __contains__(self, value:float) -> bool:
		return self.min <= value <= self.max
	
	def __str__(self) -> str:
		return str.format('(min:{0} max:{1})',self.min,self.max)
	