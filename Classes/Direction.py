from enum import Enum, auto

class Direction(Enum):
    NS = auto() # North, South (vertical bi-directional)
    WE = auto() # West, East (horizontal ...)
    NW = auto() # North, West (diagonal ...)
    NE = auto() # ...
    
    