from enum import Enum, auto

class Direction(Enum):
    # bi-directional
    NORTH_SOUTH_BI = auto()
    WEST_EAST_BI = auto()
    
    NORTH_WEST_BI = auto()
    NORTH_EAST_BI = auto()
    
    # one-way
    NORTH_SOUTH = auto()
    SOUTH_NORTH = auto()
    WEST_EAST = auto()
    EAST_WEST = auto()
    
    NORTH_WEST = auto()
    WEST_NORTH = auto()
    NORTH_EAST = auto()
    EAST_NORTH = auto()