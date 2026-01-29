from Classes.MetroCoordinator import MetroCoordinator
from Classes.Renderer import Renderer

GRID_SIZE: tuple[int, int] = (100, 100)
CELL_SIZE: int = 50

if __name__ in "__main__":
    coordinator = MetroCoordinator()
    renderer = Renderer(GRID_SIZE=GRID_SIZE, CELL_SIZE=CELL_SIZE)
    
    