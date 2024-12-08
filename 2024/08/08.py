import sys
from typing import List, Tuple
from itertools import product
from fractions import Fraction
from common.utils import run, read_lines
from common.grid import Grid, Point, grid_from_lines


def get_antinodes(a: Point, b: Point) -> List[Point]:
    dx = a.x - b.x
    dy = a.y - b.y
    if dx == 0 and dy == 0:
        return list() # same point
    return [Point(a.x + dx, a.y + dy), Point(b.x - dx, b.y - dy)]


def get_line(a: Point, b: Point) -> Tuple[Fraction, int]:
    dx = a.x - b.x
    dy = a.y - b.y
    m = Fraction(dy, dx)
    c = a.y - m * a.x
    return m, c


def is_on_line(p: Point, m: Fraction, c: int) -> bool:
    return p.y == m * p.x + c


def group_by_freq(grid: Grid) -> dict[str, set[Point]]:
    freq_antennae = dict()
    for cell in grid:
        if cell.val == '.':
            continue
        if cell.val not in freq_antennae:
            freq_antennae[cell.val] = {cell.point}
        else:
            freq_antennae[cell.val].add(cell.point)
    return freq_antennae


def solution_08_A(filename: str) -> int:
    lines = read_lines(filename)
    grid = grid_from_lines(lines)
    freq_antennae = group_by_freq(grid)
    antinodes = set()
    for antennae in freq_antennae.values():
        if len(antennae) < 2:
            continue
        for a, b in product(antennae, repeat=2):
            ans = [p for p in get_antinodes(a, b) if grid.in_bounds(p)]
            antinodes.update(ans)
    return len(antinodes)

def solution_08_B(filename: str) -> int:
    lines = read_lines(filename)
    grid = grid_from_lines(lines)
    freq_antennae = group_by_freq(grid)
    lines = set()
    for antennae in freq_antennae.values():
        if len(antennae) < 2:
            continue
        for a, b in product(antennae, repeat=2):
            if a == b:
                continue
            lines.add(get_line(a, b))
    count = 0
    for cell in grid:
        if cell.val != '.':
            count += 1 # it's an antenna
            continue
        for m, c in lines:
            if is_on_line(cell.point, m, c):
                count += 1
                break
    return count


def test_solution_08_A():
    assert solution_08_A("./08/test_input.txt") == 14  # Replace with expected output for the test case


# def test_final_solution_08_A():
#    assert solution_08_A('./08/input.txt') == 0 # Replace with solution when known


def test_solution_08_B():
    assert solution_08_B("./08/test_input.txt") == 34  # Replace with expected output for the test case


# def test_final_solution_08_B():
#    assert solution_08_B('./08/input.txt') == 0 # Replace with solution when known

def test_get_line():
    assert get_line(Point(0, 0), Point(1, 1)) == (1, 0)
    assert get_line(Point(1, 1), Point(0, 0)) == (1, 0)
    assert get_line(Point(0, 1), Point(1, 2)) == (1, 1)
    assert get_line(Point(1, 0), Point(2, 1)) == (1, -1)
    assert get_line(Point(0, 0), Point(1, 2)) == (2, 0)
    assert get_line(Point(0, 0), Point(1, 3)) == (3, 0)
    assert get_line(Point(0, 0), Point(2, 1)) == (0.5, 0)
    assert get_line(Point(0, 0), Point(3, 1)) == (Fraction(1, 3), 0)
    assert get_line(Point(0, 0), Point(9, 3)) == (Fraction(1, 3), 0)
    assert get_line(Point(0, 6), Point(9, 9)) == (Fraction(1, 3), 6)

if __name__ == "__main__":
    run("08", sys.argv[1], solution_08_A, solution_08_B)
