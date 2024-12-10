import sys
from common.utils import read_lines, run
from common.grid import grid_from_lines
from common.grid import Direction, Point, Cell


def get_reachable(cell, cache):
    if cell.point in cache:
        return cache[cell.point]
    if cell.val == '9':
        cache[cell.point] = {cell.point}
        return {cell.point}
    next_val = str(int(cell.val) + 1)
    reachable = set()
    if cell.nav_val(Direction.NORTH) == next_val:
        reachable |=  get_reachable(cell.nav(Direction.NORTH), cache)
    if cell.nav_val(Direction.SOUTH) == next_val:
        reachable |=  get_reachable(cell.nav(Direction.SOUTH), cache)
    if cell.nav_val(Direction.EAST) == next_val:
        reachable |=  get_reachable(cell.nav(Direction.EAST), cache)
    if cell.nav_val(Direction.WEST) == next_val:
        reachable |=  get_reachable(cell.nav(Direction.WEST), cache)
    cache[cell.point] = reachable
    return reachable


def solution_10_A(filename: str) -> int:
    lines = read_lines(filename)
    grid = grid_from_lines(lines)
    cache = dict()
    total = 0
    for cell in grid:
        if cell.val != '0':
            continue
        reachable = get_reachable(cell, cache)
        total += len(reachable)
    return total


def get_rating(cell, cache):
    if cell.point in cache:
        return cache[cell.point]
    if cell.val == '9':
        cache[cell.point] = 1
        return 1
    next_val = str(int(cell.val) + 1)
    total = 0
    if cell.nav_val(Direction.NORTH) == next_val:
        total +=  get_rating(cell.nav(Direction.NORTH), cache)
    if cell.nav_val(Direction.SOUTH) == next_val:
        total +=  get_rating(cell.nav(Direction.SOUTH), cache)
    if cell.nav_val(Direction.EAST) == next_val:
        total +=  get_rating(cell.nav(Direction.EAST), cache)
    if cell.nav_val(Direction.WEST) == next_val:
        total +=  get_rating(cell.nav(Direction.WEST), cache)
    cache[cell.point] = total
    return total


def solution_10_B(filename: str) -> int:
    lines = read_lines(filename)
    grid = grid_from_lines(lines)
    cache = dict()
    total = 0
    for cell in grid:
        if cell.val != '0':
            continue
        rating = get_rating(cell, cache)
        total += rating
    return total


def test_solution_10_A():
    assert solution_10_A("./10/test_input.txt") == 36  # Replace with expected output for the test case


# def test_final_solution_10_A():
#    assert solution_10_A('./10/input.txt') == 0 # Replace with solution when known


def test_solution_10_B():
    assert solution_10_B("./10/test_input.txt") == 81  # Replace with expected output for the test case


# def test_final_solution_10_B():
#    assert solution_10_B('./10/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("10", sys.argv[1], solution_10_A, solution_10_B)
