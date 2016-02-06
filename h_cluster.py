from cluster import *

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