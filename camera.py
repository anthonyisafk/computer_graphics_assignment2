import numpy as np

def get_ccs_unit_vectors(c_org: np.ndarray, c_lookat: np.ndarray, c_up: np.ndarray):
	"""Calculates the camera unit vectors depending on where the camera is located,
	where it points and which way is 'up'.

	:param c_org: camera coordinates
	:param c_lookat: the point exactly opposite from the camera
	:param c_up: 'up vector'
	"""
	c_to_center = c_lookat - c_org
	z_c = c_to_center / np.linalg.norm(c_to_center)
	t =  c_up - np.dot(c_up, z_c) * z_c
	y_c = t / np.linalg.norm(t)
	x_c = np.cross(y_c, z_c)

	return x_c, y_c, z_c