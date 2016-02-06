from PIL import Image, ImageDraw
import random
from math import sqrt

WIDTH=1000
HEIGHT=1000
COLOURS=[
    (255, 127, 39),
    (34, 177, 76),
    (0, 162, 232),
    (163, 73, 164),
    (255, 242, 0),
    (63, 72, 204),
]

def generate_points(n=100):
    return [(int(random.random()*WIDTH), int(random.random()*HEIGHT)) for i in range(n)]

def draw_point(draw, point, size, fill):
    draw.rectangle((point[0]-size, point[1]-size, point[0]+size, point[1]+size),
                       fill=fill)

def p_distance(v1, v2):
    x = v1[0] - v2[0]
    y = v1[1] - v2[1]

    return sqrt(x**2 + y**2)
