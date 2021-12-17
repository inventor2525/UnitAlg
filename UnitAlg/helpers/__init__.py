from .classproperty import classproperty, all_true
from itertools import chain

epsilon:float=0
def _get_epsilon_scoped_import():
	import numpy as np
	epsilon = np.finfo(float).eps*4
_get_epsilon_scoped_import()