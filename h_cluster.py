from cluster import *

COLORS = {
    'new-cluster': (0, 255, 0),
    'old-cluster': (0, 0, 255),
    'point': POINT_COLOR
}

class BiCluster():
    def __init__(self, pos, first=None, second=None, is_branch=False):
        self.pos = pos
        self.first = first
        self.second = second
        self.is_branch = is_branch

def h_cluster(points, distance=p_distance, file_name='h-iteration-%d.jpeg'):
    clusters = [BiCluster(point) for point in points]
    iter = 0
    render_h(clusters, None, file_name=file_name % iter)

    while len(clusters) > 1:
        iter += 1
        print("iteration %d..." % iter)

        closest_pair = (0, 1)
        closest_distance = distance(clusters[0].pos, clusters[1].pos)

        for i in range(len(clusters)):
            for j in range(i+1, len(clusters)):
                d = distance(clusters[i].pos, clusters[j].pos)
                if d < closest_distance:
                    closest_pair = (i, j)
                    closest_distance = d

        avg_pos = [(clusters[closest_pair[0]].pos[0] + clusters[closest_pair[1]].pos[0]) / 2,
                   (clusters[closest_pair[0]].pos[1] + clusters[closest_pair[1]].pos[1]) / 2]

        new_cluster = BiCluster(avg_pos,
                                first=clusters[closest_pair[0]],
                                second=clusters[closest_pair[1]],
                                is_branch=True)

        del clusters[closest_pair[1]]
        del clusters[closest_pair[0]]
        clusters.append(new_cluster)
        render_h(clusters, new_cluster, file_name=file_name % iter)

    return clusters[0]

def render_h(clusters, new_cluster, file_name='cluster.jpeg'):
    img, draw = create_image()

    for cluster in clusters:
        draw_cluster(draw, cluster)

    if new_cluster:
        draw_cluster(draw, new_cluster, fill=COLORS['new-cluster'])

    img.save(file_name)

def draw_cluster(draw, cluster, fill=None):
    if cluster.is_branch:
        if not fill: fill = COLORS['old-cluster']
        draw_cluster(draw, cluster.first, fill)
        draw_cluster(draw, cluster.second, fill)
        draw_boundary(draw, cluster, fill)
    else:
        if not fill: fill = COLORS['point']
        draw_point(draw, cluster.pos, fill)

def draw_boundary(draw, cluster, fill, offset=6):
    points = get_points(cluster)
    xmin = min([point[0] for point in points]) - offset
    xmax = max([point[0] for point in points]) + offset
    ymin = min([point[1] for point in points]) - offset
    ymax = max([point[1] for point in points]) + offset

    draw.line((xmin, ymin, xmax, ymin), fill)
    draw.line((xmin, ymax, xmax, ymax), fill)
    draw.line((xmax, ymin, xmax, ymax), fill)
    draw.line((xmin, ymin, xmin, ymax), fill)

def get_points(cluster):
    if cluster.is_branch:
        return get_points(cluster.first) + get_points(cluster.second)
    else:
        return [cluster.pos]
