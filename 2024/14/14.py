import sys
from typing import List, Set
from common.utils import run
from common.grid import Point
from collections import namedtuple
import re

Robot = namedtuple('Robot', 'x y dx dy')


def parse(filename: str):
    robots = list()
    regex = r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)"
    with open(filename, 'r') as file:
        while (line := file.readline().strip()) != '':
            groups = re.match(regex, line).groups()
            robots.append(Robot(int(groups[0]), int(groups[1]), int(groups[2]), int(groups[3])))
    return robots


def move_robot(robot: Robot, iterations: int, width: int, height: int):
    final_x = (robot.x + (robot.dx * iterations)) % width
    final_y = (robot.y + (robot.dy * iterations)) % height
    return Robot(final_x, final_y, robot.dx, robot.dy)


def solution_14_A(filename: str, width: int, height: int) -> int:
    robots = parse(filename)
    iterations = 100
    width_mid = (width - 1) / 2
    height_mid = (height - 1) / 2
    q1, q2, q3, q4 = 0, 0, 0, 0
    for robot in robots:
        final_x = (robot.x + (robot.dx * iterations)) % width
        final_y = (robot.y + (robot.dy * iterations)) % height
        if final_x < width_mid and final_y < height_mid:
            q1 += 1
        elif final_x > width_mid and final_y < height_mid:
            q2 += 1
        elif final_x < width_mid and final_y > height_mid:
            q3 += 1
        elif final_x > width_mid and final_y > height_mid:
            q4 += 1
    return q1 * q2 * q3 * q4


def robot_points(robots: List[Robot]) -> Set[Point]:
    return {Point(r.x, r.y) for r in robots}


def might_be_tree(robots: List[Robot], width: int, height: int) -> bool:
    points = robot_points(robots)
    continous_rows = list()
    h_marg = int(height * 0.2)
    w_marg = int(width * 0.2)
    for j in range(h_marg, height - h_marg):
        max_continuous = 0
        continuous = 0
        for i in range(w_marg, width - w_marg):
            if Point(i, j) in points:
                continuous += 1
                if continuous > max_continuous:
                    max_continuous = continuous
            else:
                continuous = 0
        continous_rows.append(max_continuous)
    return len([r for r in continous_rows if r > 5]) > 5


def print_robots(robots: List[Robot], width: int, height: int):
    points = robot_points(robots)
    for j in range(0, height):
        row = ""
        for i in range(0, width):
            row += "#" if Point(i, j) in points else "."
        print(row)


def solution_14_B(filename: str, width: int, height: int) -> int:
    robots = parse(filename)
    iteration = 0
    while not might_be_tree(robots, width, height):
        iteration += 1
        robots = [move_robot(r, 1, width, height) for r in robots]
    print_robots(robots, width, height)
    return iteration


def test_solution_14_A():
    assert solution_14_A("./14/test_input.txt", 11, 7) == 12  # Replace with expected output for the test case


# def test_final_solution_14_A():
#    assert solution_14_A('./14/input.txt') == 0 # Replace with solution when known


def test_solution_14_B():
    assert solution_14_B("./14/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_14_B():
#    assert solution_14_B('./14/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("14", sys.argv[1], lambda f: solution_14_A(f, 101, 103), lambda f: solution_14_B(f, 101, 103))
