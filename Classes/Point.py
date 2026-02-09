class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        
    def __eq__(self, other) -> bool:
            if not isinstance(other, Point):
                return NotImplemented
            return self.x == other.x and self.y == other.y
        
    def __lt__(self, other) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        # Lexicographical comparison:
        # 1. Compare X
        if self.x != other.x:
            return self.x < other.x
        # 2. If X is equal, compare Y
        return self.y < other.y