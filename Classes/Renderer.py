import os
from pathlib import Path
import sys
import svgwrite
import math

absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(absolute_path)

from Edge import Edge
from Lines import Line
from Point import *
from Vertex import Vertex, VertexType

SVG_OUTPUT_PATH = Path.cwd().joinpath("svgs")

COLORS = [
    "#fdce07", # yellow
    "#ef392f", # red
    "#0ab255", # green
    "#c3499b", # purple
    "#2752a4", # blue
    "#f47d20", # orange
    "#a9642a", # brown
    "#a7abae", # light grey
    "#858588", # dark grey
]

# create grid
# draw vertices
# draw edges
# draw anchor points (show a nub to drag?)
# draw arcs/bevels on corners
class Renderer:
    def __init__(self, GRID_SIZE: tuple[int, int], CELL_SIZE: int) -> None:
        os.makedirs(SVG_OUTPUT_PATH, exist_ok=True) 
        
        self.GRID_SIZE: tuple[int, int] = GRID_SIZE
        self.CELL_SIZE: int = CELL_SIZE
        self.PADDING: int = 50
    
    def _get_color(self, index: int) -> str:
        if index < len(COLORS):
            return COLORS[index]
            
        return "#000000"
    
    def _get_cell_pos(self, x: int, y: int) -> tuple[float, float]:
        return (x * self.CELL_SIZE / 2 + self.PADDING, y * self.CELL_SIZE / 2 + self.PADDING)
    
    def _draw_rounded_corner(self, drawing: svgwrite.Drawing, p0: tuple, p1: tuple, radius: float, sweep_flag: int, color: str = 'red'):
        """Renders the SVG arc based on pre-calculated tangent points and flags."""
        rel_x = p1[0] - p0[0]
        rel_y = p1[1] - p0[1]
    
        # SVG Arc path: Move to p0, then draw arc to p1
        path_data = f"M {p0[0]},{p0[1]} a {radius},{radius} 0 0,{sweep_flag} {rel_x},{rel_y}"
        
        drawing.add(drawing.path(
            d=path_data,
            fill="none",
            stroke=color,
            stroke_width=5,
        ))
    
    def draw_corner(self, drawing: svgwrite.Drawing, vertex: Vertex, color: str):
        """Calculates vertex-specific geometry and delegates drawing to _draw_rounded_corner."""
        if len(vertex.edges) < 2:
            return
    
        center_coords = self._get_cell_pos(vertex.location.x, vertex.location.y)
        radius = vertex.get_radius() / 2 * self.CELL_SIZE
    
        # 1. Calculate unit vectors for the two incident edges
        unit_vectors = []
        for edge in vertex.edges:
            # Identify the neighbor to determine direction
            neighbor = edge.start if (edge.end.x == vertex.location.x and 
                                     edge.end.y == vertex.location.y) else edge.end
            n_coords = self._get_cell_pos(neighbor.x, neighbor.y)
            
            dx, dy = n_coords[0] - center_coords[0], n_coords[1] - center_coords[1]
            mag = math.sqrt(dx**2 + dy**2)
            
            if mag > 0:
                unit_vectors.append((dx / mag, dy / mag))
    
        if len(unit_vectors) < 2:
            return
    
        # 2. Derive tangent points p0 and p1 at 'radius' distance from center
        v1, v2 = unit_vectors[0], unit_vectors[1]
        p0 = (center_coords[0] + v1[0] * radius, center_coords[1] + v1[1] * radius)
        p1 = (center_coords[0] + v2[0] * radius, center_coords[1] + v2[1] * radius)
    
        # 3. Determine sweep flag via cross product
        cross_product = v1[0] * v2[1] - v1[1] * v2[0]
        sweep_flag = 0 if cross_product > 0 else 1
    
        # 4. Delegate to drawing helper
        self._draw_rounded_corner(drawing, p0, p1, radius, sweep_flag, color)
    
    def draw_station(self, drawing: svgwrite.Drawing, position: tuple[int | float, int | float]):
        drawing.add(
            drawing.circle(
                center=position, 
                r=5, 
                fill="white",
                stroke="black",
                stroke_width=2, 
            )
        )
    
    def draw_metro(self, lines: list[Line], filename: str = "graph.svg"):
        # Initialize the drawing context
        dwg = svgwrite.Drawing(
            SVG_OUTPUT_PATH / filename, 
            profile='tiny'
        )
    
        # draw all edges for all stations
        for index, line in enumerate(lines):
            hex_color = self._get_color(index)
            # 1. Draw Edges first so they appear behind vertices
            for segment in line.segments:
                for corner in segment.vertices:
                    self.draw_corner(dwg, corner, hex_color)
                    
                for edge in segment.get_trimmed_edges():
                    
                    start_coords = self._get_cell_pos(edge.start.x, edge.start.y)
                    end_coords = self._get_cell_pos(edge.end.x, edge.end.y)
                    
                    dwg.add(dwg.line(
                        start=start_coords,
                        end=end_coords,
                        stroke=hex_color,
                        stroke_width=5
                    ))
            
        # draw all stations for all lines
        for index, line in enumerate(lines):
            hex_color = self._get_color(index)
            # 2. Draw Vertices
            for vertex in line.stations:
                pos = self._get_cell_pos(vertex.location.x, vertex.location.y)
                self.draw_station(dwg, pos)
        
        dwg.save()