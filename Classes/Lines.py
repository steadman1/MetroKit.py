import os
import sys
import math
from tabnanny import verbose
from typing import Optional

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Edge import Edge
from Point import Point
from Direction import Direction
from Vertex import Vertex, VertexType

# the edges and vertices (that are not stations !!) between two stations
class Segment:
    def __init__(self, edge: Edge, vertices: list[Vertex], split_edge: bool = True) -> None:
        self.vertices: list[Vertex] = vertices
        
        corner, edges = self.split_edge(edge)
        self.edges: list[Edge] = edges
        if corner:
            self.vertices += [corner]
    
    @classmethod
    def from_stations(cls, s1: Vertex, s2: Vertex):
        edge = Edge(s1.location, s2.location)
        return cls(edge, [s1, s2])
    
    def get_vertices(self, type: VertexType) -> list[Vertex]:
        return list( filter( lambda x: x.type.value == type.value, self.vertices ) )
    
    def split_edge(self, edge: Edge) -> tuple[Optional[Vertex], list[Edge]]:
        if edge.direction.value != Direction.UNKNOWN.value:
            return (None, [edge])

        # randomize if the split edge becomes a top left or bottom right anchor
        edges = [
            Edge(
                Point(edge.start.x, edge.start.y),
                Point(edge.start.x, edge.end.y)
            ),
            Edge(
                Point(edge.start.x, edge.end.y),
                Point(edge.end.x, edge.end.y)
            )
        ]
        corner = Vertex(
            VertexType.CORNER,
            Point(edge.start.x, edge.end.y),
            edges=edges
        )
        return (corner, edges)
    
    def get_trimmed_edges(self) -> list[Edge]:
        if not self.vertices:
            return self.edges
            
        trimmed_edges: list[Edge] = []
        
        for edge in self.edges:
            corners = self.get_vertices(VertexType.CORNER)
            # Determine the radius to trim at the start
            # Find if there's a vertex at the start point
            start_vertex = next((v for v in corners if v.location == edge.start), None)
            r_start = start_vertex.get_radius() if start_vertex else 0
            
            # Determine the radius to trim at the end
            # Find if there's a vertex at the end point
            end_vertex = next((v for v in corners if v.location == edge.end), None)
            r_end = end_vertex.get_radius() if end_vertex else 0
            
            # Calculate the unit vector for the edge direction
            dx = edge.end.x - edge.start.x
            dy = edge.end.y - edge.start.y
            length = math.sqrt(dx**2 + dy**2)
            
            if length == 0:
                continue
                
            ux, uy = dx / length, dy / length
            
            # Calculate new points
            # Shift start point forward by r_start
            new_start = Point(
                edge.start.x + ux * r_start,
                edge.start.y + uy * r_start
            )
            # Shift end point backward by r_end
            new_end = Point(
                edge.end.x - ux * r_end,
                edge.end.y - uy * r_end
            )
            
            trimmed_edges.append(Edge(new_start, new_end))
            
        return trimmed_edges

# a metro line with stations and segments
class Line:
    def __init__(self, stations: list['Vertex']) -> None:
        self.stations: list['Vertex'] = stations
        self.segments: list[Segment] = []
        
    def add_segment(self, segment: Segment):
        self.segments.append(segment)
        for vertex in segment.vertices:
            if vertex.type.value == VertexType.STATION.value and vertex not in self.stations:
                self.stations.append(vertex)
                