import cv2
import numpy as np
from math import acos
from math import sqrt
from math import pi


def length(v):
    return sqrt(v[0] ** 2 + v[1] ** 2)


def dot_product(v, w):
    return v[0] * w[0] + v[1] * w[1]


def determinant(v, w):
    return v[0] * w[1] - v[1] * w[0]


def inner_angle(v, w):
    cosx = dot_product(v, w) / (length(v) * length(w))
    rad = acos(cosx)  # in radians
    return rad * 180 / pi  # returns degrees


def angle_clockwise(A, B):
    inner = inner_angle(A, B)
    det = determinant(A, B)
    if det < 0:  # this is a property of the det. If the det < 0 then B is clockwise of A
        return inner
    else:  # if the det > 0 then A is immediately clockwise of B
        return 360 - inner


img = cv2.imread("proce0.jpg", 3)
#                    x, y , w , h
deteccion = [1114.8406982421875, 258.3362731933594, 397.4610900878906, 446.6963195800781]


height = np.size(img, 0)
width = np.size(img, 1)
print "h: " , height
print "w: " , width

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))


w1 = int(deteccion[2] / 2)
h1 = int(deteccion[3] / 2)
x1 = int(deteccion[0])
y1 = int(deteccion[1])

cv2.circle(img, (x1, y1), 5, (255, 255, 120))

cv2.circle(img, ((width / 2), (height/ 2)), 5, (0, 255, 255))

print("anglebetween: ",360 -angle_between((x1, y1),((width/2), (height))))

print("Clockwise:",angle_clockwise((x1, y1), ((width / 2), (height))))

cv2.rectangle(img, ((x1-w1),(y1-h1)), (x1+w1,(y1+h1)), (0, 255, 0), 2)
cv2.line(img,(x1,y1), ((width / 2), (height/ 2)), (255, 255, 0), 2)
cv2.imshow("Tesis", img)
tecla = cv2.waitKey(0)

