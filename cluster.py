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

def render_k(points, clusters=None, best_matches=None, file_name='cluster.jpeg'):
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    if best_matches:
        for i in range(len(best_matches)):
            for j in range(len(best_matches[i])):
                x1 = points[best_matches[i][j]][0]
                y1 = points[best_matches[i][j]][1]
                x2 = clusters[i][0]
                y2 = clusters[i][1]
                draw.line((x1, y1, x2, y2), fill=COLOURS[i])

    if clusters:
        for i in range(len(clusters)):
            draw_point(draw, clusters[i], 8, COLOURS[i])

    for point in points:
        draw_point(draw, point, 4, (237,28,36))

    img.save(file_name)

def draw_point(draw, point, size, fill):
    draw.rectangle((point[0]-size, point[1]-size, point[0]+size, point[1]+size),
                       fill=fill)

def p_distance(v1, v2):
    x = v1[0] - v2[0]
    y = v1[1] - v2[1]

    return sqrt(x**2 + y**2)

def k_cluster(points, k=5, distance=p_distance):
    "K-Means Clustering of 2D Data"
    render_k(points, file_name='iteration-0.jpeg')
    clusters = generate_points(n=k)
    last_matches = None
    for iter in range(1, 100):
        print('iteration %d' % iter)
        best_matches = [[] for i in range(k)]
        for i in range(len(points)):
            point = points[i]
            best_match = 0
            for j in range(k):
                d = distance(clusters[j], point)
                if d < distance(clusters[best_match], point): best_match = j
            best_matches[best_match].append(i)

        if last_matches == best_matches: break
        last_matches = best_matches

        render_k(points, clusters=clusters, best_matches=best_matches, file_name='iteration-%d.jpeg' % iter)

        for i in range(len(clusters)):
            avgs = [0.0, 0.0]
            for j in range(len(best_matches[i])):
                avgs[0] += points[best_matches[i][j]][0]
                avgs[1] += points[best_matches[i][j]][1]
            avgs[0] /= len(best_matches[i])
            avgs[1] /= len(best_matches[i])
            clusters[i] = avgs


class BiCluster():
    def __init__(self, pos, first=None, second=None, is_branch=False):
        self.pos = pos
        self.first = first
        self.second = second
        self.is_branch = is_branch

def h_cluster(points, distance=p_distance):
    clusters = [BiCluster(point) for point in points]
    iter = 0
    render_h(clusters, None, file_name='iteration-%d.jpeg' % iter)
    
    while len(clusters) > 1:
        closest_pair = (0, 1)
        closest_distance = distance(clusters[0].pos, clusters[1].pos)
        iter += 1
        
        for i in range(len(clusters)):
            for j in range(i+1, len(clusters)):
                d = distance(clusters[i].pos, clusters[j].pos)
                if d < closest_distance:
                    closest_pair = (i, j)
                    closest_distance = d
        
        new_pos = [(clusters[closest_pair[0]].pos[0] + clusters[closest_pair[1]].pos[0]) / 2,
                   (clusters[closest_pair[0]].pos[1] + clusters[closest_pair[1]].pos[1]) / 2]
        print(clusters[closest_pair[0]].pos, clusters[closest_pair[1]].pos, new_pos)
        new_cluster = BiCluster(new_pos, 
                                first=clusters[closest_pair[0]], 
                                second=clusters[closest_pair[1]],
                                is_branch=True)
        
        del clusters[closest_pair[1]]
        del clusters[closest_pair[0]]
        clusters.append(new_cluster)
        render_h(clusters, new_cluster, file_name='iteration-%d.jpeg' % iter)
    
def render_h(clusters, new_cluster, file_name='cluster.jpeg'):
    img = Image.new('RGB', (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    for cluster in clusters:
        draw_cluster(draw, cluster)
    
    if new_cluster:
        draw_cluster(draw, new_cluster, fill=(0, 255, 0))
        
    img.save(file_name)
    
def draw_cluster(draw, cluster, fill=None):
    if cluster.is_branch:
        if not fill: fill = (0, 0, 255)
        draw_cluster(draw, cluster.first, fill)
        draw_cluster(draw, cluster.second, fill)
    else:
        if not fill: fill = (237 ,28 ,36)
        draw_point(draw, cluster.pos, 4, fill) 
   
def demo():
    points = generate_points()
    k_cluster(points)