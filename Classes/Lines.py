import os
import sys
from typing import TYPE_CHECKING

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Edge import Edge

if TYPE_CHECKING:
    from Vertex import Vertex

# the edges and vertices (that are not stations !!) between two stations
class Segment:
    def __init__(self, edges: list[Edge], vertices: list['Vertex']) -> None:
        self.edges: list[Edge] = edges
        self.vertices: list['Vertex'] = vertices

# a metro line with stations and segments
class Line:
    def __init__(self, stations: list['Vertex']) -> None:
        self.stations: list['Vertex'] = stations
        self.segments: list[Segment] = []