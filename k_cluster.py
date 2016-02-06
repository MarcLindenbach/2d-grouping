from cluster import *

# Line colours
COLOURS=[
    (255, 127, 39),
    (34, 177, 76),
    (0, 162, 232),
    (163, 73, 164),
    (255, 242, 0),
    (63, 72, 204),
]

def k_cluster(points, k=6, distance=p_distance, file_name='k-iteration-%d.jpeg'):
    render_k(points, file_name=file_name % 0)
    clusters = generate_points(n=k)
    
    last_matches = None
    for iter in range(1, 100):
        print('iteration %d...' % iter)
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

        render_k(points, clusters=clusters, best_matches=best_matches, file_name=file_name % iter)

        for i in range(len(clusters)):
            avgs = [0.0, 0.0]
            for j in range(len(best_matches[i])):
                avgs[0] += points[best_matches[i][j]][0]
                avgs[1] += points[best_matches[i][j]][1]
            avgs[0] /= len(best_matches[i])
            avgs[1] /= len(best_matches[i])
            clusters[i] = avgs

def render_k(points, clusters=None, best_matches=None, file_name='cluster.jpeg'):
    img, draw = create_image()

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