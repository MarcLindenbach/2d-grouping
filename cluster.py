from PIL import Image, ImageDraw
import random
from math import sqrt

WIDTH=1000
HEIGHT=1000
BORDER=25
POINT_SIZE=4
POINT_COLOR=(237,28,36)

def generate_points(n=100):
    return [(int(random.random()*WIDTH) + BORDER, int(random.random()*HEIGHT) + BORDER) for i in range(n)]

def create_image():
    img = Image.new('RGB', (WIDTH + BORDER*2, HEIGHT+ BORDER*2), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    return img, draw

def draw_point(draw, point, fill, size=POINT_SIZE):
    draw.rectangle((point[0]-size, point[1]-size, point[0]+size, point[1]+size),
                       fill=fill)

def p_distance(v1, v2):
    x = v1[0] - v2[0]
    y = v1[1] - v2[1]

    return sqrt(x**2 + y**2)
