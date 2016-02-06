from h_cluster import *
from k_cluster import *

points = generate_points(n=50)
print('Running hierarchical clustering...')
h_cluster(points)
print('Running k-means clustering...')
k_cluster(points)
print('Done')