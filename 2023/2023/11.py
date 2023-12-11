# Cosmic Expansion

from collections import namedtuple

Point = namedtuple("Point", "x y")

file_path = "data/11.txt"

def parse_input():
    with open(file_path, "r") as file:
        lines = file.readlines()
    lines = [line.rstrip('\n') for line in lines]
    return lines

def get_rows_and_cols_emptiness(input):
    populated_rows = set()
    populated_cols = set()
    for i in range(len(input)):
        for j in range(len(input[i])):
            if input[i][j] == "#":
                populated_rows.add(i)
                populated_cols.add(j)
    rows = {i: i in populated_rows for i in range(len(input))}
    cols = {i: i in populated_cols for i in range(len(input[0]))}
    return rows, cols

def get_distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def calculate_galaxy_distances(emptiness_multiplier):
    input = parse_input()
    # identify empty rows and cols
    row_is_populated, col_is_populated = get_rows_and_cols_emptiness(input)
    # keep track of galaxies and find distances while iterating
    # could be more efficient by grabbing galaxies previously but who cares
    galaxies = []
    total = 0
    empty_row_count = 0
    for i in range(len(input)):
        empty_col_count = 0
        if not row_is_populated[i]:
            empty_row_count += (emptiness_multiplier - 1)
            continue # nothing to do here
        for j in range(len(input[i])):
            if not col_is_populated[j]:
                empty_col_count += (emptiness_multiplier - 1)
                continue # nothing to do here
            if input[i][j] == "#":
                galaxy = Point(i + empty_row_count, j + empty_col_count)
                for other_galaxy in galaxies:
                    total += get_distance(galaxy, other_galaxy)
                galaxies.append(galaxy)
    return total

def part1():
    total = calculate_galaxy_distances(2)
    print(total)

def part2():
    total = calculate_galaxy_distances(1000000)
    print(total)

if __name__ == "__main__":
    #part1()
    part2()