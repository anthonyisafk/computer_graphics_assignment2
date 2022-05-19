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
from camera import *
import numpy as np
import render

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
	img_w = 512 # image weight and height in pixels
	img_h = 512
	cam_w = 15 # canvas weight and height in inches
	cam_h = 15
	background = np.array([1.0, 1.0, 1.0])

	# TODO: Capture snapshots between each step.
	# 0) Original state.
	# 1) Offset by t_1.
	verts3d = transform_affine(verts3d, None, None, t_1)

	# 2) Rotate by phi around axis u
	verts3d = transform_affine(verts3d, phi, u, None)

	# 3) Offset by t_2
	verts3d = transform_affine(verts3d, None, None, t_2)



