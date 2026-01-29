import os
import sys
from math import sin
from typing import TYPE_CHECKING

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Edge import Edge

if TYPE_CHECKING:
    from Vertex import Vertex
    from Lines import Line, Segment
   
MIN_LINE_COUNT = 1
MAX_LINE_COUNT = 10

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
        
    def populate_lines():
        # define costs for each line
        def edge_cost(start: Vertex, end: Vertex) -> float:
            edge = Edge(start.location, end.location)
            distance = edge.get_length()
            four_gonality = abs( sin(4 * edge.get_angle_rad()) )
            
            # prioritize lines that have angle 0/180deg, 45/135/225/315deg, 90/270deg
            return distance * (1 + four_gonality)
           
        # iteratively determine best line count based on some efficiency score
        for line_count in range(MIN_LINE_COUNT, MAX_LINE_COUNT + 1):
            # cluster stations using k-mean (where each cluster is a metro line)
            # build min. spanning tree for each cluster
            # calculate weight of adjacencies based on distance, angle of vertices, etc.
            pass 
            
        # determine most efficient graph based on total weight of graph
        # check for large edge lengths
        
        pass
    
    def build_line(self) -> Line:
        return Line([])