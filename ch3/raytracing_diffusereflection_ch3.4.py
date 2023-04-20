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

class Light:
	AMBIENT = 0
	POINT = 1
	DIRECTIONAL = 2

	def __init__ (self, typeL, intensity, position):
		self.typeL = typeL
		self.intensity = intensity
		self.position = position # store direction in position in case of directional light

viewport_size = 1
projection_plane_d = 1
O = [0, 0, 0]

sphere1 = Sphere([0, -1, 3], 1, [255, 0, 0])
sphere2 = Sphere([2, 0, 4], 1, [0, 0, 255])
sphere3 = Sphere([-2, 0, 4], 1, [0, 255, 0])
sphere4 = Sphere([0, -5001, 0], 5000, [255, 255, 0])
spheres = [sphere1, sphere2, sphere3, sphere4]

light1 = Light(Light.AMBIENT, 0.2, None)
light2 = Light(Light.POINT, 0.6, [2, 1, 0])
light3 = Light(Light.DIRECTIONAL, 0.2, [1, 4, 4])
lights = [light1, light2, light3]


def putPixel(img, x, y, color):
    x = CANVAS_WIDTH/2 + x
    y = CANVAS_HEIGHT/2 - y
    if (x< 0 or x >= CANVAS_WIDTH or y < 0 or y >= CANVAS_HEIGHT):
        return
    cv2.line(img, (int(x), int(y)), (int(x), int(y)), (color[0], color[1], color[2]))

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

	point = np.add(O, np.dot(closest_t, direction))
	normal = np.subtract(point, closest_sphere.center)
	normal = normal / np.linalg.norm(normal)
	return np.dot(closest_sphere.color, computeLighting(point, normal))

def computeLighting (point, normal):
	total_intensity = 0.0
	
	for light in lights:
		if light.typeL == Light.AMBIENT:
			total_intensity += light.intensity
		else:
			if light.typeL == Light.POINT:
				vec_light = np.subtract(light.position, point)
			else:
				vec_light = light.position

			n_dot_l = np.dot(normal, vec_light)
			if n_dot_l > 0:
				total_intensity += light.intensity * n_dot_l / (np.linalg.norm(normal) * np.linalg.norm(vec_light))

	return total_intensity

def main ():
	img = np.zeros((CANVAS_WIDTH, CANVAS_HEIGHT, 3), dtype = np.uint8)
	x = -CANVAS_WIDTH / 2
	y = -CANVAS_HEIGHT / 2
	for i in range(CANVAS_WIDTH):
		for j in range(CANVAS_HEIGHT):
			direction = canvas2viewport(x, y)
			color = traceRay(O, direction, 1, math.inf)
			putPixel(img, x, y, color)
			y += 1
		y = -CANVAS_HEIGHT / 2
		x += 1
	plt.imshow(img)
	plt.show()

if __name__ == '__main__':
	main()