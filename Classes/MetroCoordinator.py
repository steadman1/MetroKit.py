import os
import sys
from math import sin, ceil
from random import choice

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Edge import Edge
from Vertex import Vertex
from Lines import Line, Segment
from Point import Point
   
MIN_LINE_COUNT = 1
MAX_LINE_COUNT = 8

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
    def _edge_cost(self, start: Point, end: Point) -> float:
        edge = Edge(start, end)
        distance = edge.get_length()
        four_gonality = abs( sin(4 * edge.get_angle_rad()) )
        
        # prioritize lines that have angle 0/180deg, 45/135/225/315deg, 90/270deg
        return distance * (1 + four_gonality)
    
    # calc min spanning tree for given vertex set
    def _prims_mst(self, vertices: list[Vertex]) -> list[Segment]:
        vertex_count = len(vertices)
        if vertex_count == 0:
            return []
    
        min_dist = [float('inf')] * vertex_count
        parent = [-1] * vertex_count
        in_mst = [False] * vertex_count
    
        min_dist[0] = 0
        mst_segments = []
    
        for _ in range(vertex_count):
            u = -1
            for i in range(vertex_count):
                if not in_mst[i] and (u == -1 or min_dist[i] < min_dist[u]):
                    u = i
    
            if min_dist[u] == float('inf'):
                break
    
            in_mst[u] = True
            if parent[u] != -1:
                segments = Segment.from_stations(vertices[parent[u]], vertices[u])
                mst_segments.append(segments)
    
            for v in range(vertex_count):
                if not in_mst[v]:
                    dist = self._edge_cost(vertices[u].location, vertices[v].location)
                    if dist < min_dist[v]:
                        min_dist[v] = dist
                        parent[v] = u
    
        return mst_segments
    
    def _calculate_lines_efficiency(self, lines: list[Line]) -> float:
        result = 0
        
        for line in lines:
            for segment in line.segments:
                result += self._edge_cost(
                    segment.edges[0].start, segment.edges[0].end
                )
        
        return result
        
    def _are_stations_connected(self, v1: Vertex, v2: Vertex) -> bool:
        for line in self.lines:
            if v1 in line.stations and v2 in line.stations:
                return True
        
        return False
    
    def _get_closest_unconnected_station(self, vertex: Vertex) -> Vertex:
        if not self.stations:
            raise ValueError("No stations available in MetroCoordinator.")

        closest_station = self.stations[0]
        min_cost = float('inf')

        for station in self.stations:
            # guard against same station
            if station.location == vertex.location or self._are_stations_connected(station, vertex):
                continue
                
            current_cost = self._edge_cost(vertex.location, station.location)
            
            if current_cost < min_cost:
                min_cost = current_cost
                closest_station = station

        return closest_station
    
    def populate_lines(self):            
        best_efficiency = float('inf')
        # iteratively determine best line count based on some efficiency score
        for line_count in range(MIN_LINE_COUNT, min(MAX_LINE_COUNT + 1, len(self.stations) + 1)):
            # cluster stations (where each cluster is a metro line)
            clusters: list[list[Vertex]] = self._get_clusters(self.stations, line_count)
            
            lines: list[Line] = []
            # build min. spanning tree for each cluster
            for cluster in clusters:
                line = Line(cluster)
                mst = self._prims_mst(cluster)
                for segment in mst:
                    line.add_segment(segment)
                
                lines.append(line)
            
            current_efficiency = self._calculate_lines_efficiency(lines)
            if current_efficiency < best_efficiency:
                best_efficiency = current_efficiency
                self.lines = lines
            
        # calculate weight of adjacencies based on distance, angle of vertices, etc.
        # 
        # connect lines together
        # todo: ensure graph becomes fully connected, currently its not guarenteed
        for line in self.lines:
            if not line.stations:
                continue
                
            start = line.stations[0]
            end = self._get_closest_unconnected_station(start)
            line.add_segment(Segment.from_stations(start, end))
            
        # determine most efficient graph based on total weight of graph
        # check for large edge lengths
        return