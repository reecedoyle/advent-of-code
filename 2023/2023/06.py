# Wait For It

import math

# Your toy boat has a starting speed of zero millimeters per millisecond.
# For each whole millisecond you spend at the beginning of the race holding down the button,
# the boat's speed increases by one millimeter per millisecond.

# x = time held
# y = distance travelled
# t = total time available
# d = target distance

# y = x * (t - x)
# y = tx - x^2
# d < y
# d < tx - x^2
# x^2 - tx + d < 0
# Find the roots of the quadratic equation & all points between them are the "winning" times
# (x - t/2)^2 - (t/2)^2 + d < 0
# x = (t +- sqrt(t^2 - 4d)) / 2

from collections import namedtuple

Race = namedtuple("Race", "time distance")

file_path = "data/06.txt"

def parse_input():
    with open(file_path, "r") as file:
        lines = file.readlines()
    lines = [line.rstrip('\n').split() for line in lines]  # Strip newlines from lines
    for i in range(1, len(lines[0])):
        yield Race(int(lines[0][i]), int(lines[1][i]))

def get_race_ways(race):
    discriminant = (race.time ** 2) - (4 * race.distance)
    discriminant_root = math.sqrt(discriminant)
    lower_root = (race.time - discriminant_root)/2
    upper_root = (race.time + discriminant_root)/2
    ceil_lower_root = math.ceil(lower_root)
    if ceil_lower_root == lower_root: # must be higher than the root
        ceil_lower_root += 1
    floor_upper_root = math.floor(upper_root)
    if floor_upper_root == upper_root: # must be lower than the root
        floor_upper_root -= 1
    ways = (floor_upper_root - ceil_lower_root) + 1
    val_before = ceil_lower_root - 1
    val_after = floor_upper_root + 1
    return ways

def part1():
    product = 1
    for race in parse_input():
        ways = get_race_ways(race)
        product = product * ways
    print(product)

def part2():
    time = ""
    distance = ""
    for race in parse_input():
        time += f"{race.time}"
        distance += f"{race.distance}"
    race = Race(int(time), int(distance))
    ways = get_race_ways(race)
    print(ways)

if __name__ == "__main__":
    part2()