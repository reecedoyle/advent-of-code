from collections import defaultdict
import sys
from common.utils import read_lines, run
from common.grid import Cell, grid_from_lines, Direction


DIRECTIONS = {
    "^": Direction.NORTH,
    "v": Direction.SOUTH,
    ">": Direction.EAST,
    "<": Direction.WEST
}


ROTATE = {
    "^": ">",
    "v": "<",
    ">": "v",
    "<": "^"
}


def solution_06_A(filename: str) -> int:
    lines = read_lines(filename)
    grid = grid_from_lines(lines)
    current = grid.find("^")
    obstacle = "#"
    while True:
        direction = current.val
        next = current.nav(DIRECTIONS[direction])
        if next is None: # out of bounds
            current.set_val("X") # mark as visited
            break
        if next.val == obstacle: # blocked, rotate, go again
            current.val = ROTATE[direction]
            continue
        current.set_val("X") # mark as visited
        current = next # move
        current.set_val(direction) # continue in the same direction
    return sum([row.count("X") for row in grid.val_rows()])


def detect_cycle(current: Cell) -> bool:
    direction = current.val
    prev_directions = defaultdict(set)
    while current is not None:
        if direction in prev_directions[current.point]:
            return True
        prev_directions[current.point].add(direction)
        next = current.nav(DIRECTIONS[direction])
        if next is not None and next.val == "#":
            direction = ROTATE[direction]
        else:
            current = next # move
    return False


def solution_06_B(filename: str) -> int:
    lines = read_lines(filename)
    grid = grid_from_lines(lines)
    current = grid.find("^")
    obstacle = "#"
    tested_blocks = {current.point} # can't place obstacle on start position
    count = 0
    while True:
        direction = current.val
        next = current.nav(DIRECTIONS[direction])
        if next is None: # out of bounds
            break
        if next.val == obstacle: # blocked, rotate, go again
            current.set_val(ROTATE[direction])
            continue
        adjacent = current.nav(DIRECTIONS[ROTATE[direction]])
        if adjacent is not None and next.point not in tested_blocks:
            tested_blocks.add(next.point)
            next_val = next.val
            next.set_val(obstacle) # place obstacle to test for loop
            if detect_cycle(current):
                count += 1
            next.set_val(next_val) # remove placed obstacle
        current = next # move
        current.set_val(direction) # continue in the same direction
    return count # remove start point


def test_solution_06_A():
    assert solution_06_A("./06/test_input.txt") == 41  # Replace with expected output for the test case


# def test_final_solution_06_A():
#    assert solution_06_A('./06/input.txt') == 0 # Replace with solution when known


def test_solution_06_B():
    assert solution_06_B("./06/test_input.txt") == 6  # Replace with expected output for the test case


# def test_final_solution_06_B():
#    assert solution_06_B('./06/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("06", sys.argv[1], solution_06_A, solution_06_B)
