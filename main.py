import svgwrite

from Classes.Line import Line
from Classes.Point import Point
from Classes.Station import Station

GRID_SIZE: tuple[int, int] = (100, 100)
CELL_SIZE: int = 50

if __name__ in "__main__":
    dwg = svgwrite.Drawing("test.svg", size=('100px', '100px'), profile='tiny')
    
    dwg.add(dwg.rect(insert=(20, 20), size=(60, 20), fill='blue'))

    dwg.save()
    
    x = Line(Point(1, 1), Point(1, 1))