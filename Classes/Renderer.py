import os
import sys
import svgwrite

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Edge import Edge
from Lines import *
from Point import *
from Vertex import *


class Renderer:
    def __init__(self, GRID_SIZE: tuple[int, int], CELL_SIZE: int) -> None:
        self.GRID_SIZE: tuple[int, int] = GRID_SIZE
        self.CELL_SIZE: int = CELL_SIZE