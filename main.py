from Classes.MetroCoordinator import MetroCoordinator
from Classes.Point import Point
from Classes.Renderer import Renderer
from Classes.Vertex import Vertex, VertexType

from random import sample

GRID_SIZE: tuple[int, int] = (100, 100)
CELL_SIZE: int = 50

if __name__ in "__main__":
    grid = set([ Vertex(VertexType.STATION, Point(x, y)) for x in range(100) for y in range(100) ])
    stations = sample(list(grid), 100)
    
    coordinator = MetroCoordinator(stations)
    renderer = Renderer(GRID_SIZE=GRID_SIZE, CELL_SIZE=CELL_SIZE)
    
    clusters: list[list[Vertex]] = coordinator._get_clusters(stations, 6)
    for (index, cluster) in enumerate(clusters):
        edges = coordinator._prims_mst(cluster)
    
        renderer.draw_graph(stations, edges, filename=f"cluster_{index}_mst.svg")
    
    