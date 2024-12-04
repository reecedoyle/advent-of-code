from dataclasses import dataclass
from enum import Enum
from typing import List


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4
    NORTHEAST = 5
    SOUTHEAST = 6
    SOUTHWEST = 7
    NORTHWEST = 8


@dataclass
class Point:
    x: int
    y: int

    def __str__(self):
        return f"({self.x},{self.y})"


def min_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


@dataclass
class Cell:
    grid: "Grid"
    point: Point
    val: str

    def __str__(self):
        return self.val
    
    def nav(self, direction: Direction):
        switch = {
            Direction.NORTH: lambda c : c.move(0, -1),
            Direction.EAST: lambda c : c.move(1, 0),
            Direction.SOUTH: lambda c : c.move(0, 1),
            Direction.WEST: lambda c : c.move(-1, 0),
            Direction.NORTHEAST: lambda c : c.move(1, -1),
            Direction.SOUTHEAST: lambda c : c.move(1, 1),
            Direction.SOUTHWEST: lambda c : c.move(-1, 1),
            Direction.NORTHWEST: lambda c : c.move(-1, -1)
        }
        return switch[direction](self)
    
    def nav_val(self, direction: Direction):
        cell = self.nav(direction)
        if cell is not None:
            return cell.val
        return None
    
    def move(self, dx, dy):
        return self.grid.loc(self.point.x + dx, self.point.y + dy)


class Grid:
    def __init__(self, vals: list[list[str]]):
        # copy so we don't end up with a ref to some other list
        self.vals = list([list(row) for row in vals])

    def width(self):
        return len(self.vals[0]) if len(self.vals) > 0 else 0

    def height(self):
        return len(self.vals)

    def val_rows(self):
        return list([list(row) for row in self.vals])

    def val_cols(self):
        grid_width = self.width()
        if grid_width > 0:
            cols = []
            for i in range(0, grid_width):
                cols.append([row[i] for row in self.val_rows()])
            return cols
        else:
            return []
        
    def loc(self, x, y):
        if x >= self.width() or y >= self.height() or x < 0 or y < 0:
            return None
        return Cell(self, Point(x, y), self.vals[y][x])

    def __iter__(self):
        for y, row in enumerate(self.vals):
            for x, val in enumerate(row):
                yield Cell(self, Point(x, y), val)

    def __str__(self):
        return "\n".join(["".join(row) for row in self.vals])


def grid_from_lines(lines: list[str]) -> Grid:
    vals = []
    for line in lines:
        vals.append(list(line.strip()))
    return Grid(vals)
