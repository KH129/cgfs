import numpy as np
import math
import cv2
import matplotlib.pyplot as plt

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
BACKGROUND_COLOR = [255, 255, 255]

class Sphere: #note that the order of color is BRG for opencv
	def __init__ (self, center, radius, color):
		self.center = center
		self.radius = radius
		self.color = color

viewport_size = 1
projection_plane_d = 1
O = [0, 0, 0]

sphere1 = Sphere([0, -1, 3], 1, [255, 0, 0])
sphere2 = Sphere([2, 0, 4], 1, [0, 0, 255])
shpere3 = Sphere([-2, 0, 4], 1, [0, 255, 0])

spheres = [sphere1, sphere2, shpere3]

def canvas2viewport (x, y):
	return (x * viewport_size / CANVAS_WIDTH, y * viewport_size / CANVAS_HEIGHT, projection_plane_d)


def intersectRaySphere (origin, direction, sphere):
	r = sphere.radius
	CO = np.subtract(origin, sphere.center)

	a = np.dot(direction, direction)
	b = 2 * np.dot(CO, direction)
	c = np.dot(CO, CO) - r * r

	discriminant = b * b - 4 * a * c
	if discriminant < 0:
		return (math.inf, math.inf)


	t1 = (-b + math.sqrt(discriminant)) / (2 * a)
	t2 = (-b - math.sqrt(discriminant)) / (2 * a)

	return (t1, t2)


def putPixel(img, x, y, color):
    x = CANVAS_WIDTH/2 + x
    y = CANVAS_HEIGHT/2 - y
    if (x< 0 or x >= CANVAS_WIDTH or y < 0 or y >= CANVAS_HEIGHT):
        return
    cv2.line(img, (int(x), int(y)), (int(x), int(y)), (color[0], color[1], color[2]))


def traceRay (origin, direction, t_min, t_max):
	closest_t = math.inf
	closest_sphere = None
	for sphere in spheres:
		t1, t2 = intersectRaySphere(origin, direction, sphere)
		if t1 >= t_min and t1 <= t_max and t1 < closest_t:
			closest_t = t1
			closest_sphere = sphere
		if t2 >= t_min and t2 <= t_max and t2 < closest_t:
			closest_t = t2
			closest_sphere = sphere

	if closest_sphere == None:
		return BACKGROUND_COLOR
	return closest_sphere.color


def main ():
	img = np.zeros((CANVAS_WIDTH, CANVAS_HEIGHT, 3), dtype = np.uint8)

	for x in range(-CANVAS_WIDTH//2, CANVAS_WIDTH//2 + 1):
		for y in range(-CANVAS_HEIGHT//2, CANVAS_HEIGHT//2 + 1):
			direction = canvas2viewport(x, y)
			color = traceRay(O, direction, 1, math.inf)
			putPixel(img, x, y, color)
	plt.imshow(img)
	plt.show()


main()
# if __name__ == '__main__':
# 	main()