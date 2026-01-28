import os
import sys

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Line import Line
from Point import Point

class Station:
    def __init__(self, location: Point) -> None:
        self.lines = []
        self.location = location
    
    def add_line(self, line: Line):
        pass