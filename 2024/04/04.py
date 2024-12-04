import sys
from common.utils import run, read_lines
from common.grid import grid_from_lines, Cell, Direction


def check_word(cell: Cell, word: str, direction: Direction=None) -> int:
    if len(word) == 0:
        return 0
    if cell.val != word[0]:
        return 0
    if len(word) == 1:
        return True
    word_count = 0
    if direction is None:
        for d in Direction:
            next_cell = cell.nav(d)
            if next_cell is not None:
                if check_word(next_cell, word[1:], d):
                    word_count += 1
        return word_count # no valid direction
    else:
        next_cell = cell.nav(direction)
        if next_cell is not None:
            return check_word(next_cell, word[1:], direction)


def solution_04_A(filename: str) -> int:
    lines = read_lines(filename)
    grid = grid_from_lines(lines)
    count = 0
    for cell in grid:
        count += check_word(cell, 'XMAS')
    return count


def is_x_mas(cell: Cell) -> bool:
    if cell.val != 'A':
        return False
    nw = cell.nav_val(Direction.NORTHWEST)
    ne = cell.nav_val(Direction.NORTHEAST)
    sw = cell.nav_val(Direction.SOUTHWEST)
    se = cell.nav_val(Direction.SOUTHEAST)
    upwards = (nw == 'M' and se == 'S') or (nw == 'S' and se == 'M')
    downwards = (ne == 'M' and sw == 'S') or (ne == 'S' and sw == 'M')
    return upwards and downwards


def solution_04_B(filename: str) -> int:
    lines = read_lines(filename)
    grid = grid_from_lines(lines)
    count = 0
    for cell in grid:
        if is_x_mas(cell):
            count += 1
    return count


def test_solution_04_A():
    assert solution_04_A("./04/test_input.txt") == 18  # Replace with expected output for the test case


# def test_final_solution_04_A():
#    assert solution_04_A('./04/input.txt') == 0 # Replace with solution when known


def test_solution_04_B():
    assert solution_04_B("./04/test_input.txt") == 9  # Replace with expected output for the test case


# def test_final_solution_04_B():
#    assert solution_04_B('./04/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("04", sys.argv[1], solution_04_A, solution_04_B)
