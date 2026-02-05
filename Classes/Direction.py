from enum import Enum, auto
from tkinter.constants import TRUE

class Direction(Enum):
    UNKNOWN = auto()
    
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
    
    def is_cardinal(self):
        match self.value:
         case Direction.NORTH_WEST_BI.value | \
                Direction.NORTH_EAST_BI.value | \
                Direction.NORTH_WEST.value | \
                Direction.NORTH_EAST.value | \
                Direction.WEST_NORTH.value | \
                Direction.EAST_NORTH.value | \
                Direction.UNKNOWN:
            return False 
        
        return True
             