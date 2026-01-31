from Classes.MetroCoordinator import MetroCoordinator
from Classes.Point import Point
from Classes.Renderer import Renderer
from Classes.Vertex import Vertex, VertexType

from random import sample

GRID_SIZE: tuple[int, int] = (100, 100)
CELL_SIZE: int = 16

def get_predefined_stations_placements() -> list[Vertex]:
    return [
        Vertex(VertexType.STATION, Point(0, 0)),
        Vertex(VertexType.STATION, Point(2, 3)),
        
        Vertex(VertexType.STATION, Point(10, 4)),
        Vertex(VertexType.STATION, Point(12, 1)),
    ]

def get_random_station_placements(count: int) -> list[Vertex]:
    grid = set([ 
        Vertex(VertexType.STATION, Point(x, y)) for x in range(GRID_SIZE[0]) for y in range(GRID_SIZE[1]) 
    ])
    return sample(list(grid), count)

if __name__ in "__main__":
    stations = get_random_station_placements(100)
    # stations = get_predefined_stations_placements()
    
    coordinator = MetroCoordinator(stations)
    renderer = Renderer(GRID_SIZE=GRID_SIZE, CELL_SIZE=CELL_SIZE)
    
    coordinator.populate_lines()
    renderer.draw_metro(coordinator.lines, filename="cluster_mst.svg")
    
    