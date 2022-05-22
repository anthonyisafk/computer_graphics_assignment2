from helpers import *
from render.util import render
import numpy as np
import math

def transform_affine(cp, theta, u, t):
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


def rasterize(verts2d, img_h, img_w, cam_h, cam_w):
	"""Matches the 2D camera projections to pixels on the canvas."""
	scale = np.array([img_w / cam_w, img_h / cam_h]) # factors by which we scale down the x and y coordinates
	verts_scaled = np.round(verts2d * scale)

	# Incorporate the elements that are out of bounds (in negative indices)
	# They will be cropped out using render_object().
	max_w = abs(min(verts_scaled[:, 0]))
	max_h = abs(min(verts_scaled[:, 1]))
	M = max_w if max_w > img_w / 2 else img_w / 2
	N = max_h if max_h > img_h / 2 else img_h / 2
	offset = np.array([M, N]) # offset the photo to bring the bottom left coordinates to (0,0)
	verts_rast_offset = transform_affine(verts_scaled, None, None, offset)
	return verts_rast_offset, M, N


def render_object(verts3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up):
	verts2d, depths = project_cam_lookat(f, c_org, c_lookat, c_up, verts3d)
	verts_rast, M, N = rasterize(verts2d, img_h, img_w, cam_h, cam_w)
	max_w = max(verts_rast[:, 0])
	max_h = max(verts_rast[:, 1])
	crop, full_img_w, full_img_h = get_full_image_dimensions(img_w, img_h, max_w, max_h, M, N)
	img = render(verts_rast, faces, vcolors, depths, "gouraud", int(full_img_w), int(full_img_h))

	if np.any(crop > 0):
		print(f"Cropping...")
		return crop_image(img, crop, img_w, img_h)
	return img