import numpy as np
import cv2 as cv

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


def get_full_image_dimensions(img_w, img_h, max_w, max_h, M, N):
	crop = np.array([0, 0])
	full_img_w = max(img_w, max_w + 1)
	full_img_h = max(img_h, max_h + 1)
	if M > img_w / 2:
		crop[0] = M - img_w / 2
		if full_img_w == img_w:
			full_img_w = M + img_w / 2
	if N > img_h / 2:
		crop[1] = N - img_h / 2
		if full_img_h == img_h:
			full_img_h = N + img_h / 2

	return crop, full_img_w, full_img_h


def crop_image(img, crop, img_w, img_h):
	cropped_img = np.zeros((img_w, img_h, 3))
	for i in range(img_w):
		x = i + crop[0]
		for j in range(img_h):
			cropped_img[i][j] = img[x][j + crop[1]]
	cv.imshow(f"Cropped image", cropped_img)
	cv.waitKey(0)
	cv.destroyAllWindows()

	return cropped_img