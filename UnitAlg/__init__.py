from .Vector3 import Vector3
from .Quaternion import Quaternion
from .Ray import Ray
from .Transform import Transform
from .Plane import Plane

epsilon:float
def _get_epsilon_scoped_import():
	import numpy as np
	epsilon = np.finfo(float).eps*4
_get_epsilon_scoped_import()