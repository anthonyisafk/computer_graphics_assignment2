"""
@author: Antonios Antoniou
@email: aantonii@ece.auth.gr
******************************
@brief:
@instructions:
******************************
2022 Aristotle University Thessaloniki - Computer Graphics
"""

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
	R = np.zeros((3, 3))
	cq = cp

	if u is not None:
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
		cq = R.dot(cp)

	if t is not None:
		for i in range(len(cq[0])):
			cq[:, i] += t

	return cq, R


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

if __name__ == "__main__":
	cp = np.array([
		[-0.5, 1.2, 2, 2.2, 3.2, 4.5],
	 	[2, 2, 2, 2.2, 3.2, 4.5],
		[2, 3, 2, 2.2, 3.2, 4.5]
	])
	cq, R = transform_affine(cp, math.pi / 4, np.array([1, 2, 1]), np.array([1, 2, 3]))

	vq = system_transform(cq[:, 1], R, np.array([1, 0.5, 0.5]))
	print(f"vq = {vq}")