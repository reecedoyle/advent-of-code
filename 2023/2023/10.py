# Pipe Maze

from enum import Enum
from dataclasses import dataclass, replace
from typing import List
from typing_extensions import Self
from termcolor import colored

Direction = Enum('Direction', ['NORTH', 'SOUTH', 'EAST', 'WEST'])

@dataclass
class Tile:
    row: int
    col: int
    value: str
    tiles: List[List[Self]]
    on_path: bool = False
    in_loop: bool = False

    def is_start(self):
        return self.value == 'S'
    
    def get_adj(self, direction):
        if direction == Direction.NORTH:
            return self.tiles[self.row - 1][self.col]
        elif direction == Direction.SOUTH:
            return self.tiles[self.row + 1][self.col]
        elif direction == Direction.EAST:
            return self.tiles[self.row][self.col + 1]
        elif direction == Direction.WEST:
            return self.tiles[self.row][self.col - 1]
        
    def set_on_path(self):
        self.tiles[self.row][self.col] = replace(self, on_path=True)
        
    def set_in_loop(self):
        self.tiles[self.row][self.col] = replace(self, in_loop=True)
        
    def __repr__(self):
        if self.is_start():
            return colored(self.value, "green")
        elif self.on_path:
            return colored(self.value, "red")
        elif self.in_loop:
            return colored(self.value, "blue")
        else:
            return self.value

west_connected = set(["-", "J", "7", "S"])
east_connected = set(["-", "L", "F", "S"])
north_connected = set(["|", "J", "L", "S"])
south_connected = set(["|", "F", "7", "S"])

connections = {
    Direction.NORTH: north_connected,
    Direction.SOUTH: south_connected,
    Direction.EAST: east_connected,
    Direction.WEST: west_connected
}

opposite_direction = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST
}

file_path = "data/10.txt"

def parse_input():
    with open(file_path, "r") as file:
        lines = file.readlines()
    lines = [line.rstrip('\n') for line in lines]
    tiles = []
    for i in range(len(lines)):
        tile_row = []
        for j in range(len(lines[i])):
            tile_row.append(Tile(i, j, lines[i][j], tiles))
        tiles.append(tile_row)
    return tiles

def find_start(tiles):
    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            if tiles[i][j].is_start():
                return tiles[i][j]

def is_connected(tile1, tile2):
    is_eastward = tile1.col == tile2.col - 1 and \
        tile1.value in east_connected and tile2.value in west_connected
    is_westward = tile1.col == tile2.col + 1 and \
        tile1.value in west_connected and tile2.value in east_connected
    is_northward = tile1.row == tile2.row + 1 and \
        tile1.value in north_connected and tile2.value in south_connected
    is_southward = tile1.row == tile2.row - 1 and \
        tile1.value in south_connected and tile2.value in north_connected
    return ((is_eastward or is_westward) and tile1.row == tile2.row) \
        or ((is_northward or is_southward) and tile1.col == tile2.col)

def can_go(direction, current_tile, prev_direction):
    # This currently ignores the bounds of the grid, we assume this is impossible
    return (prev_direction is None or direction != opposite_direction[prev_direction]) and \
        current_tile.value in connections[direction]

def get_next(current_tile, prev_direction):
    for direction in Direction:
        if can_go(direction, current_tile, prev_direction):
            adj_tile = current_tile.get_adj(direction)
            if is_connected(current_tile, adj_tile):
                return (adj_tile, direction)

def part1():
    tiles = parse_input()
    tile = find_start(tiles)
    steps = 0
    prev_direction = None
    while True:
        steps += 1
        (tile, prev_direction) = get_next(tile, prev_direction)
        if tile.is_start():
            break
    print(steps//2)

def part2():
    tiles = parse_input()
    tile = find_start(tiles)
    prev_direction = None
    while True:
        tile.set_on_path()
        (tile, prev_direction) = get_next(tile, prev_direction)
        if tile.is_start():
            break
    # Now mark as inside or outside
    count = 0
    for i in range(len(tiles)):
        inside_loop = False
        direction_entered_from = None
        for j in range(len(tiles[i])):
            # must treat pipes as tiny lines, so symbols handled differently? count continous pipes!
            if tiles[i][j].on_path:
                # pipe just entered this row
                if tiles[i][j].value == "L":
                    direction_entered_from = Direction.NORTH
                if tiles[i][j].value == "F":
                    direction_entered_from = Direction.SOUTH
                # change loop state if pipe passed through this row
                if tiles[i][j].value == "J" or tiles[i][j].is_start(): # hack
                    if direction_entered_from == Direction.SOUTH:
                        inside_loop = not inside_loop
                    direction_entered_from = None
                if tiles[i][j].value == "7":
                    if direction_entered_from == Direction.NORTH:
                        inside_loop = not inside_loop
                    direction_entered_from = None
                if tiles[i][j].value == "|":
                    inside_loop = not inside_loop
            if not tiles[i][j].on_path:
                if inside_loop:
                    tiles[i][j].set_in_loop()
                    count += 1

    for line in tiles:
        print("".join([str(tile) for tile in line]))

    print(count)

if __name__ == "__main__":
    #part1()
    part2()