from typing import Any, Type, TypeVar

class Convertable():
	to_conversions = {}
	from_conversions = {}
	
	T = TypeVar("T", bound='Convertable')
	@classmethod
	def _from(cls:Type[T], original:Any) -> T:
		try:
			conversion = cls.from_conversions[type(original)]
			return conversion(original)
		except:
			raise KeyError("Invalid type passed or you need to supply a from conversion function for this type!", type(original))
	
	K = TypeVar("K")
	def to(self, other:Type[K]) -> K:
		try:
			conversion = self.to_conversions[other]
			return conversion(self)
		except:
			raise KeyError("You need to supply a conversion function for this type!", other)
			