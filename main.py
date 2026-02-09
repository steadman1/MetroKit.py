from Classes.MetroCoordinator import MetroCoordinator
from Classes.Point import Point
from Classes.Renderer import Renderer
from Classes.Vertex import Vertex, VertexType
from Classes.Lines import Line, Segment

from random import seed, sample

GRID_SIZE: tuple[int, int] = (16, 16)
CELL_SIZE: int = 60
LINE_COUNT: int = 3

def get_predefined_stations_placements() -> list[Vertex]:
    return [
        Vertex(VertexType.STATION, Point(0, 0)),
        Vertex(VertexType.STATION, Point(2, 3)),
        
        Vertex(VertexType.STATION, Point(10, 4)),
        Vertex(VertexType.STATION, Point(12, 1)),
        
        Vertex(VertexType.STATION, Point(16, 10)),
        Vertex(VertexType.STATION, Point(4, 12)),
    ]

def get_random_station_placements(count: int, use_seed: bool = True) -> list[Vertex]:
    grid = [ 
        Vertex(VertexType.STATION, Point(x, y)) 
        for x in range(GRID_SIZE[0]) 
        for y in range(GRID_SIZE[1]) 
    ]
    
    if use_seed:
        seed(0)
    return sample(list(grid), count)

if __name__ in "__main__":
    stations = get_random_station_placements(24)
    # stations = get_predefined_stations_placements()
    
    coordinator = MetroCoordinator(stations, GRID_SIZE=GRID_SIZE, LINE_COUNT=LINE_COUNT)
    renderer = Renderer(GRID_SIZE=GRID_SIZE, CELL_SIZE=CELL_SIZE)
    
    coordinator.populate_lines(0)
    renderer.draw_metro(coordinator.lines, filename="cluster_mst.svg")
    
    coordinator.populate_lines(1)
    renderer.draw_metro(coordinator.lines, filename="cluster_mst_magnetic.svg")
    
    