from Direction import Direction
from Point import Point

# a single edge between two vertices
class Edge:
    def __init__(self, start: Point, end: Point) -> None:
        if start.y == end.y:
            self.direction = Direction.NORTH_SOUTH_BI
        elif start.x == end.x:
            self.direction = Direction.WEST_EAST_BI
        elif (end.x - start.x) == (end.y - start.y):
            self.direction = Direction.NORTH_WEST_BI
        elif (end.x - start.x) == -(end.y - start.y):
            self.direction = Direction.NORTH_EAST_BI
        else:
            raise Exception("Invalid edge start, end pair")