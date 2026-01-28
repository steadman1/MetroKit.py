import os
import sys

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Line import Line
from Point import Point

class Vertex:
    def __init__(self, location: Point) -> None:
        self.lines: list[Line] = []
        self.location: Point = location
    
    def add_line(self, line: Line):
        pass

# visible vertex
class Station(Vertex):
    pass

# invisible vertex at corners or created by gestures
class Anchor(Vertex):
    pass