import os
from pathlib import Path
import sys
import svgwrite

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Edge import Edge
from Lines import *
from Point import *
from Vertex import Vertex, VertexType

SVG_OUTPUT_PATH = Path.cwd().joinpath("svgs")

# create grid
# draw vertices
# draw edges
# draw anchor points (show a nub to drag?)
# draw arcs/bevels on corners
class Renderer:
    def __init__(self, GRID_SIZE: tuple[int, int], CELL_SIZE: int) -> None:
        self.GRID_SIZE: tuple[int, int] = GRID_SIZE
        self.CELL_SIZE: int = CELL_SIZE
    
    def draw_graph(self, v: list[Vertex], e: list[Edge], filename: str = "graph.svg"):
        # Initialize the drawing context
        dwg = svgwrite.Drawing(
            SVG_OUTPUT_PATH / filename, 
            profile='tiny'
        )
    
        # 1. Draw Edges first so they appear behind vertices
        for edge in e:
            start_coords = (edge.start.x, edge.start.y)
            end_coords = (edge.end.x, edge.end.y)
            
            dwg.add(dwg.line(
                start=start_coords,
                end=end_coords,
                stroke=svgwrite.rgb(0, 0, 0, '%'),
                stroke_width=2
            ))
    
        # 2. Draw Vertices
        for vertex in v:
            pos = (vertex.location.x, vertex.location.y)
            
            match vertex.type.value:
                case VertexType.STATION.value:
                    dwg.add(dwg.circle(center=pos, r=2, fill='red'))
                case VertexType.CORNER.value:
                    dwg.add(dwg.circle(center=pos, r=2, fill='gray'))
                case VertexType.ANCHOR.value:
                    dwg.add(dwg.circle(center=pos, r=2, fill='none', stroke='blue', stroke_dasharray='2,2'))
    
        dwg.save()