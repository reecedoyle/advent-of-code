# Parabolic Reflector Dish

from functools import lru_cache
import numpy as np

file_path = "data/14.txt"

def parse_input():
    with open(file_path, "r") as file:
        lines = file.readlines()
    return [line.rstrip('\n') for line in lines]

def part1():
    input = parse_input()
    row_score = len(input)
    col_scores = [row_score] * len(input[0])
    print(col_scores)
    total_score = 0
    line_num = 0
    for line in input:
        line_num += 1
        for i in range(len(line)):
            if line[i] == '#':
                col_scores[i] = row_score - 1
            if line[i] == 'O':
                print(line_num, i, col_scores[i])
                total_score += col_scores[i]
                col_scores[i] -= 1
        row_score -= 1
    print(total_score)

def roll_line_left(array):
    boulder_count = 0
    count = 0
    line = ""
    for element in array:
        if element == 'O':
            boulder_count += 1
            count += 1
        elif element == '#':
            line += "O" * boulder_count + "." * (count - boulder_count) + '#'
            count = 0
            boulder_count = 0
        else:
            count += 1
    line += "O" * boulder_count + "." * (count - boulder_count)
    return np.array([x for x in line])

def roll_line(line, direction):
    if direction in ('W', 'N'):
        return roll_line_left(line)
    if direction in ('E','S'):
        return roll_line_left(line[::-1])[::-1]
    
def roll_rows(grid, direction):
    return np.array([roll_line(row, direction) for row in grid])

def roll_cols(grid, direction):
    return np.array([roll_line(col, direction) for col in grid.T]).T
    
def roll_grid(grid, direction):
    if direction in ('N','S'):
        cols = roll_cols(grid, direction)
        return cols
    else:
        rows = roll_rows(grid, direction)
        return rows
    
def cycle_grid(grid):
    for direction in ('N', 'W', 'S', 'E'):
        grid = roll_grid(grid, direction)
    return grid

def compute_grid_id(a):
    b = ''
    (rows, cols) = a.shape
    for i in range(0,rows):
        for j in range(0,cols):
            b+=str(a[i,j])
    return b

def print_grid(grid):
    for row in grid:
        print(''.join(row))

def calculate_load(grid):
    load = 0
    for i in range(0, grid.shape[0]):
        load += np.sum(grid[-i-1] == 'O') * (i + 1)
    return load

def part2():
    input = parse_input()
    grid = np.array([[x for x in line] for line in input])
    starting_grid_id = compute_grid_id(grid)
    seen_grids = {starting_grid_id:0}
    for i in range(1000000000):
        grid = cycle_grid(grid)
        grid_id = compute_grid_id(grid)
        if grid_id in seen_grids:
            print(i)
            break
        seen_grids[grid_id] = i + 1
    cycles_before_loop = seen_grids[grid_id]
    loop_size = i + 1 - cycles_before_loop
    cycles_after_loop = (1000000000 - cycles_before_loop) % loop_size

    ## prove it
    grid_before = grid
    for i in range(loop_size):
        grid = cycle_grid(grid)
    print((grid_before == grid).all())

    for i in range(cycles_after_loop):
        grid = cycle_grid(grid)
    print(cycles_before_loop, loop_size, cycles_after_loop)
    print(calculate_load(grid))

if __name__ == "__main__":
    #part1()
    part2()