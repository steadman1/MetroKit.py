import os
import sys
from math import sin, ceil
from random import sample, choice

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Edge import Edge
from Vertex import Vertex
from Lines import Line, Segment
from Point import Point
from MagnetismPathfinder import MagnetismPathfinder

# create stations given (or not given) location
# ^ use PCA or MDS to place points given a similarity vector
# create lines given stations locations
# create Segments between stations with edges, corners, etc.
# handle segment magnitism: creation, modification (anchor point updates)
# 
class MetroCoordinator:
    # populate stations based on 
    def __init__(
        self, 
        stations: list[Vertex], 
        GRID_SIZE: tuple[int, int],
        LINE_COUNT: int = 6
    ) -> None:
        self.stations: list[Vertex] = stations
        self.lines: list[Line] = []
        
        self.GRID_SIZE = GRID_SIZE
        self.LINE_COUNT = LINE_COUNT
    
    @classmethod
    def from_lines(
        cls, 
        stations: list[Vertex], 
        lines: list[Line],
        GRID_SIZE: tuple[int, int],
        LINE_COUNT: int
    ):
        coordinator = cls(stations, GRID_SIZE, LINE_COUNT)
        coordinator.lines = lines
        return coordinator
    
    # generate clusters using k-mean 
    def _get_clusters(self, vertices: list[Vertex], cluster_count: int, iterations: int = 10) -> list[list[Vertex]]:
        if not vertices or cluster_count <= 0:
            return []
        if cluster_count >= len(vertices):
            return [[v] for v in vertices]
    
        centroids = [v.location for v in sample(vertices, cluster_count)]
        
        clusters: list[list[Vertex]] = [[] for _ in range(cluster_count)]
    
        for _ in range(iterations):
            clusters = [[] for _ in range(cluster_count)]
    
            for vertex in vertices:
                best_centroid_idx = 0
                min_cost = float('inf')
                
                for i, centroid_loc in enumerate(centroids):
                    cost = self._edge_cost(vertex.location, centroid_loc)
                    if cost < min_cost:
                        min_cost = cost
                        best_centroid_idx = i
                
                clusters[best_centroid_idx].append(vertex)
    
            for i in range(cluster_count):
                if not clusters[i]:
                    centroids[i] = choice(vertices).location
                    continue
                
                avg_x = sum(v.location.x for v in clusters[i]) / len(clusters[i])
                avg_y = sum(v.location.y for v in clusters[i]) / len(clusters[i])
                centroids[i] = Point(avg_x, avg_y)
    
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
                segment = Segment.from_stations(vertices[parent[u]], vertices[u])
                mst_segments.append(segment)
    
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
    
    def populate_lines(self, magnetism: float):           
        clusters: list[list[Vertex]] = self._get_clusters(self.stations, self.LINE_COUNT)
        
        global_edges: list[Edge] = []
        lines: list[Line] = []
        # build min. spanning tree for each cluster
        for cluster in clusters:
            line = Line(cluster)
            mst = self._prims_mst(cluster)
            
            for segment_template in mst:
                p_start = segment_template.edges[0].start
                p_end = segment_template.edges[-1].end

                # 1. Calculate Path
                pathfinder = MagnetismPathfinder(global_edges, self.GRID_SIZE)
                path_points = pathfinder.find_path(p_start, p_end, magnetism)
                
                # 2. Process Path into Graph Primitives
                new_edges, new_corners = MagnetismPathfinder.process_path_into_segment_data(path_points)
                
                # 3. Add to Global Environment (so next lines stick to these)
                global_edges.extend(new_edges)

                # 4. Create the Segment
                # We pass the edges and the explicitly created corner vertices.
                # We set split_edge=False because we have manually defined the geometry.
                
                # Note: Segment expects a list of edges. If your Segment class is strictly 
                # one edge (as per original code), you may need to add multiple Segments.
                # However, assuming we modified Segment to hold a chain of edges:
                
                # Case A: Segment supports multiple edges (Recommended Refactor)
                # new_segment = Segment(new_edges, vertices=new_corners, split_edge=False)
                # line.add_segment(new_segment)

                # Case B: One Segment per Edge (Strict adherence to original Segment class)
                # This is safer if you haven't refactored Segment yet.
                # We treat the path as a chain of segments.
                for i, edge in enumerate(new_edges):
                    # Find if this edge connects to a corner we just created
                    # The start of this edge might be a corner from the previous iteration
                    start_v = next((c for c in new_corners if c.location == edge.start), None)
                    end_v = next((c for c in new_corners if c.location == edge.end), None)
                    
                    verts = []
                    if start_v: verts.append(start_v)
                    if end_v: verts.append(end_v)
                    
                    # We pass the specific edge and its associated corners
                    seg = Segment(edge, vertices=verts, split_edge=False)
                    line.add_segment(seg)
            
            lines.append(line)
        
        self.lines = lines
            
        # connect lines together
        # todo: ensure graph becomes fully connected, currently its not guarenteed
        # for line in self.lines:
        #     if not line.stations:
        #         continue
                
        #     start = line.stations[0]
        #     end = self._get_closest_unconnected_station(start)
        #     line.add_segment(Segment.from_stations(start, end))
            
        # determine most efficient graph based on total weight of graph
        # check for large edge lengths
        return