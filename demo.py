"""
@author: Antonios Antoniou
@email: aantonii@ece.auth.gr
******************************
@brief: Reads the hw2.npy file to get info about the 3D coordinates of the vertices of the triangles
		an image has been split into. Uses the info about the location of the camera, its center
		and the up vector to match the 3D points to their 2D projections on a photograph.
		Then 'render' (of the 1st assignment) is called to capture a snapshot of the result
		during certain steps of the procedure.
******************************
2022 Aristotle University Thessaloniki - Computer Graphics
"""

from util import *
import numpy as np


if __name__ == "__main__":
	data = np.load("hw2/hw2.npy", allow_pickle=True)[()]
	verts3d = data['verts3d']
	vcolors = data['vcolors']
	faces = data['faces']
	c_org = data['c_org']
	c_lookat = data['c_lookat']
	c_up = data['c_up']
	t_1 = data['t_1']
	t_2 = data['t_2']
	u = data['u']
	phi = data['phi']

	f = 70 # focal distance
	img_w = 512 # image width and height in pixels
	img_h = 512
	cam_w = 15 # canvas width and height in inches
	cam_h = 15
	background = np.array([1.0, 1.0, 1.0])

	# 0) Original state.
	print("Original state...\n")
	render_object(verts3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up)

	# 1) Offset by t_1.
	print(f"Offsetting by {t_1.tolist()}...\n")
	verts3d = transform_affine(verts3d, None, None, t_1)
	render_object(verts3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up)

	# 2) Rotate by phi around axis u
	print(f"Rotating by {phi} radians around axis {u.tolist()}...\n")
	verts3d = transform_affine(verts3d, phi, u, None)
	render_object(verts3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up)

	# 3) Offset by t_2
	print(f"Offsetting by {t_2.tolist()}...")
	verts3d = transform_affine(verts3d, None, None, t_2)
	render_object(verts3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up)