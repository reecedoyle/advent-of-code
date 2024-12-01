from collections import defaultdict
import sys
from common.utils import run


def solution_01_A(filename: str) -> int:
    with open(filename, "r") as file:
        data = file.readlines()
        left = list()
        right = list()
        for line in data:
            (left_side, right_side) = line.split()
            left.append(left_side)
            right.append(right_side)
    left.sort()
    right.sort()
    sum = 0
    for i in range(len(left)):
        sum += abs((int(left[i]) - int(right[i])))
    return sum


def solution_01_B(filename: str) -> int:
    with open(filename, "r") as file:
        data = file.readlines()
        left = list()
        right_count = defaultdict(lambda: 0)
        for line in data:
            (left_side, right_side) = [int(x) for x in line.split()]
            left.append(left_side)
            right_count[right_side] += 1
    sum = 0
    for num in left:
        sum += num * right_count[num]
    return sum


def test_solution_01_A():
    assert solution_01_A("./01/test_input.txt") == 11


# def test_final_solution_01_A():
#    assert solution_01_A('./01/input.txt') == 1223326 # Replace with solution when known


def test_solution_01_B():
    assert solution_01_B("./01/test_input.txt") == 31


# def test_final_solution_01_B():
#    assert solution_01_B('./01/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("01", sys.argv[1], solution_01_A, solution_01_B)
