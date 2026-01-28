import os
import sys

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Point import Point

class Line:
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end