from camera import *
import numpy as np
import math

def transform_affine(cp: np.ndarray, theta, u: np.ndarray, t: np.ndarray):
	"""
	:param cp: the initial point
	:param theta: the angle of rotation
	:param u: the axis the rotation takes place around
	:param t: the offset after the rotation, given as a vector
	:return: the resulting point cq
	"""
	R = np.zeros((3, 3)) # matrix placeholder for the Rodrigues formula
	cq = cp

	if u is not None and theta is not None:
		R1 = (1 - math.cos(theta)) * np.array([
			[u[0] ** 2, u[0] * u[1], u[0] * u[2]],
			[u[1] * u[0], u[1] ** 2, u[1] * u[2]],
			[u[2] * u[0], u[2] * u[1], u[2] ** 2]
		])
		R2 = math.cos(theta) * np.eye(3)
		R3 = math.sin(theta) * np.array([
			[0, -1 * u[2], u[1]],
			[u[2], 0, -1 * u[0]],
			[-1 * u[1], u[0], 0]
		])
		R = R1 + R2 + R3
		cq = R.dot(cp.T).T

	if t is not None:
		for i in range(len(cq)):
			cq[i] += t

	return cq


def system_transform(cp, R, c0):
	"""Change from one coordinate system to another.

	:param cp: initial point in the original coordinate system
	:param R: the rotation matrix
	:param c0: the new point of reference (i.e. start of the axes)
	:return: the resulting point after the rotation using the new coordinate system
	"""
	RT = np.transpose(R)
	dp = RT.dot(cp)
	return dp - c0


def project_cam(f, cv, cx, cy, cz, p):
	"""Finds the projection of a point.
	Uses the WCS (World Coordinate System) coordinates and turns them into
	CCS (Camera Coordinate System) coordinates.

	:param f: focal distance
	:param cv: coordinates of the camera
	:param cx: WCS coordinates of the CCS x unit vector
	:param cy: WCS coordinates of the CCS y unit vector
	:param cz: WCS coordinates of the CCS z unit vector
	:param p: the point [3 x 1], or matrix of points, [3 x N]
	:return: the 2D projections of the points and the respective depths
	"""
	R = np.stack((cx, cy, cz), axis=1) # rotation matrix based on the new unit vectors
	n = len(p)
	verts2d = np.zeros((n, 2))
	depths = np.zeros(n)
	for i in range(n):
		p_ccs = system_transform(p[i], R, cv)
		verts2d[i] = (f / p_ccs[2]) * p_ccs[0:2]
		depths[i] = p_ccs[2]
	return verts2d, depths


def project_cam_lookat(f, c_org, c_lookat, c_up, verts3d):
	cx, cy, cz = get_ccs_unit_vectors(c_org, c_lookat, c_up)
	return project_cam(f, c_org, cx, cy, cz, verts3d)