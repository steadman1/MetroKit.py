import os
import sys
import svgwrite
from typing import TYPE_CHECKING

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

if TYPE_CHECKING:
    from Edge import Edge
    from Lines import *
    from Point import *
    from Vertex import *

# create grid
# drawing vertices
# draw edges
# draw anchor points (show a nub to drag?)
# draw arcs/bevels on corners
class Renderer:
    def __init__(self, GRID_SIZE: tuple[int, int], CELL_SIZE: int) -> None:
        self.GRID_SIZE: tuple[int, int] = GRID_SIZE
        self.CELL_SIZE: int = CELL_SIZE