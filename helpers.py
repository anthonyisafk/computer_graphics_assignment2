import numpy as np

def get_ccs_unit_vectors(c_org: np.ndarray, c_lookat: np.ndarray, c_up: np.ndarray):
	"""Calculates the camera unit vectors depending on where the camera is located,
	where it points and which way is 'up'.

	:param c_org: camera coordinates
	:param c_lookat: the point we have set at the center of the photograph.
	:param c_up: 'up vector'
	"""
	c_to_center = c_lookat - c_org
	z_c = c_to_center / np.linalg.norm(c_to_center)
	t =  c_up - np.dot(c_up, z_c) * z_c
	y_c = t / np.linalg.norm(t)
	x_c = np.cross(y_c, z_c)

	return x_c, y_c, z_c


def find_out_of_bounds_vertices(verts_rast, img_h, img_w):
	negative = np.argwhere(verts_rast < 0)[:, 0]
	height = np.argwhere(verts_rast[:, 0] > img_w - 1)[:, 0]
	width = np.argwhere(verts_rast[:, 1] > img_h - 1)[:, 0]
	return np.union1d(np.union1d(height, width), negative)


def get_in_bounds_vertices_and_faces(rejects, verts_rast, faces, vcolors):
	verts_in = np.delete(verts_rast, rejects, 0)