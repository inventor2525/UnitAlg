from typing import Iterator

class classproperty():
	def __init__(self, f):
		self.f = f
	def __get__(self, obj, owner):
		return self.f()

def all_true(bools:Iterator[bool]):
	'''
	Checks if all in iterator are true.
	'''
	for b in bools:
		if not b:
			return False
	return True