import os
import sys
from math import sin, ceil
from random import choice
import heapq
from typing import TYPE_CHECKING

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Edge import Edge
from Vertex import Vertex
from Lines import Line, Segment
   
MIN_LINE_COUNT = 2
MAX_LINE_COUNT = 2

# create stations given (or not given) location
# ^ use PCA or MDS to place points given a similarity vector
# create lines given stations locations
# create Segments between stations with edges, corners, etc.
# handle segment magnitism: creation, modification (anchor point updates)
# 
class MetroCoordinator:
    # populate stations based on 
    def __init__(self, stations: list[Vertex]) -> None:
        self.stations: list[Vertex] = stations
        self.lines: list[Line] = []
    
    # randomly selecting vertices to generate clusters
    # TODO: change to k-mean clustering or another algo (?)
    def _get_clusters(self, vertices: list[Vertex], cluster_count: int) -> list[list[Vertex]]:
        max_capacity = ceil(len(vertices) / cluster_count)
        clusters: list[list[Vertex]] = [ [] for _ in range(cluster_count) ]
        
        for vertex in vertices:
            cluster_index_choices = [
                x for x in range(cluster_count) 
                if len(clusters[x]) < max_capacity
            ]
            cluster_index = choice(cluster_index_choices)
            clusters[cluster_index].append(vertex)
            
        return clusters
        
    # define costs for each line
    def _edge_cost(self, start: Vertex, end: Vertex) -> float:
        edge = Edge(start.location, end.location)
        distance = edge.get_length()
        four_gonality = abs( sin(4 * edge.get_angle_rad()) )
        
        # prioritize lines that have angle 0/180deg, 45/135/225/315deg, 90/270deg
        return distance * (1 + four_gonality)
    
    # calc min spanning tree for given vertex set
    def _prims_mst(self, vertices: list[Vertex]) -> list[Edge]:
        vertex_count = len(vertices)
        if vertex_count == 0:
            return []
    
        min_dist = [float('inf')] * vertex_count
        parent = [-1] * vertex_count
        in_mst = [False] * vertex_count
    
        min_dist[0] = 0
        mst_edges = []
    
        for _ in range(vertex_count):
            u = -1
            for i in range(vertex_count):
                if not in_mst[i] and (u == -1 or min_dist[i] < min_dist[u]):
                    u = i
    
            if min_dist[u] == float('inf'):
                break
    
            in_mst[u] = True
            if parent[u] != -1:
                edge = Edge(vertices[parent[u]].location, vertices[u].location)
                mst_edges.append(edge)
    
            for v in range(vertex_count):
                if not in_mst[v]:
                    dist = self._edge_cost(vertices[u], vertices[v])
                    if dist < min_dist[v]:
                        min_dist[v] = dist
                        parent[v] = u
    
        return mst_edges
        
    def populate_lines(self):            
        # iteratively determine best line count based on some efficiency score
        for line_count in range(MIN_LINE_COUNT, MAX_LINE_COUNT + 1):
            # cluster stations (where each cluster is a metro line)
            clusters: list[list[Vertex]] = self._get_clusters(self.stations, line_count)
            
            # build min. spanning tree for each cluster
            print([ list((str(vertex) for vertex in cluster)) for cluster in clusters])
            for cluster in clusters:
                mst = self._prims_mst(cluster)
                print([ str(edge) for edge in mst])
            
            # calculate weight of adjacencies based on distance, angle of vertices, etc.
            pass 
            
        # determine most efficient graph based on total weight of graph
        # check for large edge lengths
        return