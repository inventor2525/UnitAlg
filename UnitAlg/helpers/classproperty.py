from typing import Callable, Iterator, TypeVar, Generic

_T = TypeVar("_T", covariant=True)
class classproperty(Generic[_T]):
	def __init__(self, f:Callable[[],_T]):
		self.f = f
	def __get__(self, obj, owner) -> _T:
		return self.f()

def all_true(bools:Iterator[bool]) -> bool:
	'''
	Checks if all in iterator are true.
	'''
	for b in bools:
		if not b:
			return False
	return True