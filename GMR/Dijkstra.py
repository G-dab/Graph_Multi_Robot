import numpy as np

from utils import *

def Dijkstra(adjmatrix, graph_type='undirected'):
    if graph_type == 'undirected':
        # determine whether the graph is undirected
        if not np.allclose(adjmatrix, adjmatrix.T):
            raise ValueError('The graph is not undirected!')
    # determine whether the graph is connected
    if not is_connected(adjmatrix):
        raise ValueError('The graph is not connected!')
    
    # Dijkstra algorithm
    n = adjmatrix.shape[0]
    visited = [False] * n
    dist = [float('inf')] * n
    dist[0] = 0
    for i in range(n):
        min_dist = float('inf')
        for j in range(n):
            if not visited[j] and dist[j] < min_dist:
                min_dist = dist[j]
                u = j
        visited[u] = True
        for v in range(n):
            if not visited[v] and dist[u] + adjmatrix[u, v] < dist[v]:
                dist[v] = dist[u] + adjmatrix[u, v]
    return dist