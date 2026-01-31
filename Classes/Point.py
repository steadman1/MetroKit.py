class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y