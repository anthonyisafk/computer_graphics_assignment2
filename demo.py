"""
@author: Antonios Antoniou
@email: aantonii@ece.auth.gr
@version: Python 3.7.9
******************************
@brief: Reads the hw2.npy file to get info about the 3D coordinates of the vertices of the triangles
		an image has been split into. Uses the info about the location of the camera, its center
		and the up vector to match the 3D points to their 2D projections on a photograph.
		Then 'render' (of the 1st assignment) is called to capture a snapshot of the result
		during certain steps of the procedure.
@notes: `render` function borrowed from Anestis Kaimakamidis - 9627.
******************************
2022 Aristotle University Thessaloniki - Computer Graphics
"""

from util import *
import numpy as np
import cv2 as cv


if __name__ == "__main__":
	data = np.load("hw2.npy", allow_pickle=True)[()]
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

	# 0) Original state.
	print("Initial state...")
	img0 = render_object(verts3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up)
	save_image(img0, img_w, img_h, "0.jpg")

	# 1) Offset by t_1.
	print(f"\nOffsetting by {t_1.tolist()}...")
	verts3d = transform_affine(verts3d, None, None, t_1)
	img1 = render_object(verts3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up)
	save_image(img1, img_w, img_h, "1.jpg")


	# 2) Rotate by phi around axis u
	print(f"\nRotating by {phi} radians around axis {u.tolist()}...")
	verts3d = transform_affine(verts3d, phi, u, None)
	img2 = render_object(verts3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up)
	save_image(img2, img_w, img_h, "2.jpg")

	# 3) Offset by t_2
	print(f"\nOffsetting by {t_2.tolist()}...")
	verts3d = transform_affine(verts3d, None, None, t_2)
	img3 = render_object(verts3d, faces, vcolors, img_h, img_w, cam_h, cam_w, f, c_org, c_lookat, c_up)
	save_image(img3, img_w, img_h, "3.jpg")