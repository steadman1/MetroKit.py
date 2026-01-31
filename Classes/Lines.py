import os
import sys
from typing import TYPE_CHECKING

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Edge import Edge
from Point import Point
from Direction import Direction

if TYPE_CHECKING:
    from Vertex import Vertex

# the edges and vertices (that are not stations !!) between two stations
class Segment:
    def __init__(self, edge: Edge) -> None:
        self.edges: list[Edge] = self.split_edge(edge)
    
    def split_edge(self, edge: Edge) -> list[Edge]:
        if edge.direction.value != Direction.UNKNOWN.value:
            return [edge]

        first = Edge(
            Point(edge.start.x, edge.start.y),
            Point(edge.start.x, edge.end.y)
        )
        second = Edge(
            Point(edge.start.x, edge.end.y),
            Point(edge.end.x, edge.end.y)
        )
        return [first, second]
        

# a metro line with stations and segments
class Line:
    def __init__(self, stations: list['Vertex']) -> None:
        self.stations: list['Vertex'] = stations
        self.segments: list[Segment] = []
        
    def add_segment(self, segment: Segment):
        self.segments.append(segment)