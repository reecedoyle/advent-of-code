import sys
from common.utils import run, read_lines
import re


def solution_03_A(filename: str) -> int:
    lines = read_lines(filename)
    sum = 0
    for line in lines:
        matches = re.findall(r"mul\((\d{1,3})\,(\d{1,3})\)", line)
        for match in matches:
            sum += int(match[0]) * int(match[1])
    return sum


def solution_03_B(filename: str) -> int:
    lines = read_lines(filename)
    sum = 0
    active = True
    for line in lines:
        matches = re.findall(r"mul\((\d{1,3})\,(\d{1,3})\)|(do\(\))|(don\'t)", line)
        for a, b, do, dont in matches:
            if len(do) > 0:
                active = True
            if len(dont) > 0:
                active = False
            if not active:
                continue
            if len(a) > 0 and len(b) > 0:
                sum += int(a) * int(b)
    return sum


def test_solution_03_A():
    assert solution_03_A("./03/test_input.txt") == 161


# def test_final_solution_03_A():
#    assert solution_03_A('./03/input.txt') == 0 # Replace with solution when known


def test_solution_03_B():
    assert solution_03_B("./03/test_input2.txt") == 48


# def test_final_solution_03_B():
#    assert solution_03_B('./03/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("03", sys.argv[1], solution_03_A, solution_03_B)
