import os
import sys
from math import floor
from enum import Enum, auto
from typing import TYPE_CHECKING

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Point import Point

if TYPE_CHECKING:
    from Edge import Edge
    from Lines import Line, Segment

class VertexType(Enum):
    STATION = auto() # a visible vertex on the grid
    ANCHOR = auto() # an invisible vertex on the grid (created from gestures)
    CORNER = auto() # a vertex on the grid where incoming lines 

class Vertex:
    def __init__(self, type: VertexType, location: Point, edges: list['Edge'] = []) -> None:
        self.type: VertexType = type
        self.edges: list['Edge'] = edges
        self.location: Point = location
        
        # check if there's more than just incoming and outgoing lines, might want the ability to have more than 2 at some point but not rn
        if len(self.edges) > 2:
            raise Exception("Vertices should not have more than 2 associated lines.")
    
    def __str__(self) -> str:
        return f"{self.type.name}: ({self.location.x}, {self.location.y})"
    
    def add_edge(self, edge: 'Edge'):
        self.edges.append(edge)
    
    def remove_edge(self, edge: 'Edge'):
        self.edges.remove(edge)
    
    def get_radius(self) -> int:
        edge_lengths: list[float] = list( map( lambda x: x.get_length(), self.edges ) )
        return min(
            floor( min( edge_lengths ) ),
            4
        )