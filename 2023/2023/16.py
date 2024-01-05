# The Floor Will Be Lava

from enum import Flag, Enum
from dataclasses import dataclass

# Indicate whether a cell is energised and which direction the energy travelled to
class Direction(Flag):
    NONE = 0
    UP = 1
    DOWN = 2
    LEFT = 4
    RIGHT = 8

@dataclass
class Beam:
    direction: Direction
    x: int
    y: int

    def move(self, grid):
        if self.x < 0 or self.x >= len(grid) or self.y < 0 or self.y >= len(grid[0]):
            return []
        if grid[self.x][self.y] == '.':
            return [next_location(self.x, self.y, self.direction)]
        if grid[self.x][self.y] == '/':
            if self.direction == Direction.UP:
                return [next_location(self.x, self.y, Direction.RIGHT)]
            if self.direction == Direction.DOWN:
                return [next_location(self.x, self.y, Direction.LEFT)]
            if self.direction == Direction.LEFT:
                return [next_location(self.x, self.y, Direction.DOWN)]
            if self.direction == Direction.RIGHT:
                return [next_location(self.x, self.y, Direction.UP)]
        if grid[self.x][self.y] == '\\':
            if self.direction == Direction.UP:
                return [next_location(self.x, self.y, Direction.LEFT)]
            if self.direction == Direction.DOWN:
                return [next_location(self.x, self.y, Direction.RIGHT)]
            if self.direction == Direction.LEFT:
                return [next_location(self.x, self.y, Direction.UP)]
            if self.direction == Direction.RIGHT:
                return [next_location(self.x, self.y, Direction.DOWN)]
        if grid[self.x][self.y] == '-':
            if self.direction in (Direction.UP, Direction.DOWN):
                return [next_location(self.x, self.y, Direction.LEFT), next_location(self.x, self.y, Direction.RIGHT)]
            return [next_location(self.x, self.y, self.direction)]
        if grid[self.x][self.y] == '|':
            if self.direction in (Direction.LEFT, Direction.RIGHT):
                return [next_location(self.x, self.y, Direction.UP), next_location(self.x, self.y, Direction.DOWN)]
            return [next_location(self.x, self.y, self.direction)]


file_path = "data/16.txt"

def parse_input():
    with open(file_path, "r") as file:
        lines = file.readlines()
    return [line.rstrip('\n') for line in lines]

def next_location(x, y, direction):
    return {
        Direction.UP: Beam(direction, x - 1, y),
        Direction.DOWN: Beam(direction, x + 1, y),
        Direction.LEFT: Beam(direction, x, y - 1),
        Direction.RIGHT: Beam(direction, x, y + 1)
    }[direction]

def count_energised(grid_states):
    count = 0
    for i in range(len(grid_states)):
        for j in range(len(grid_states[i])):
            if grid_states[i][j] != Direction.NONE:
                count += 1
    return count

def shine_beam(grid, x, y, direction):
    print("Shining beam", x, y, direction)
    energy_states = [[Direction.NONE] * len(grid[0]) for i in range(len(grid))]
    beams = [Beam(direction, x, y)]
    while len(beams) > 0:
        for beam in beams:
            energy_states[beam.x][beam.y] = energy_states[beam.x][beam.y] | beam.direction
        beams = [next_beam for beam in beams for next_beam in beam.move(grid)]
        # Remove out-of-range beams
        beams = [beam for beam in beams if beam.x >= 0 and beam.x < len(grid) and beam.y >= 0 and beam.y < len(grid[0])]
        # remove beams that have already passed through in the same direction
        beams = [beam for beam in beams if energy_states[beam.x][beam.y] & beam.direction == Direction.NONE]
    energised_count = count_energised(energy_states)
    return energised_count

def part1():
    grid = parse_input()
    print(shine_beam(grid, 0, 0, Direction.RIGHT))

def part2():
    grid = parse_input()
    max_energised = 0
    for x in range(len(grid)):
        energised = shine_beam(grid, x, 0, Direction.RIGHT)
        if energised > max_energised:
            max_energised = energised
        energised = shine_beam(grid, x, len(grid[x])-1, Direction.LEFT)
        if energised > max_energised:
            max_energised = energised
    for y in range(len(grid[0])):
        energised = shine_beam(grid, 0, y, Direction.DOWN)
        if energised > max_energised:
            max_energised = energised
        energised = shine_beam(grid, len(grid)-1, y, Direction.UP)
        if energised > max_energised:
            max_energised = energised
    print(max_energised)

if __name__ == "__main__":
    #part1()
    part2()