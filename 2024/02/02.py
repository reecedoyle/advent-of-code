import sys
from typing import List
from common.utils import run


def get_sign(x):
    return (x > 0) - (x < 0) 


def remove_level(levels: List[int], index: int) -> List[int]:
    new_levels = levels.copy()
    new_levels.pop(index)
    return new_levels


def is_safe_report(levels: List[int], problem_dampener: bool = False) -> bool:
    max_diff = 3
    min_diff = 1
    diff = levels[1] - levels[0]
    sign = get_sign(diff)
    if abs(diff) > max_diff or abs(diff) < min_diff:
        if problem_dampener:
            return any([is_safe_report(remove_level(levels, j)) for j in (0, 1)])
        else:
            return False
    for i in range(2, len(levels)):
        diff = levels[i] - levels[i-1]
        if sign != get_sign(diff):
            if problem_dampener:
                # comparing diff to first diff, so try removing first element too
                remove_options = (i-1, i, 0) if i == 2 else (i-1, i)
                return any([is_safe_report(remove_level(levels, j)) for j in remove_options])
            else:
                return False
        if abs(diff) > max_diff or abs(diff) < min_diff:
            if problem_dampener:
                return any([is_safe_report(remove_level(levels, j)) for j in (i-1, i)])
            else:
                return False
    return True


def solution_02_A(filename: str) -> int:
    with open(filename, 'r') as file:
        lines = file.readlines()
    return sum(is_safe_report([int(x) for x in line.split()]) for line in lines)


def solution_02_B(filename: str) -> int:
    with open(filename, 'r') as file:
        lines = file.readlines()
    return sum(is_safe_report([int(x) for x in line.split()], True) for line in lines)


def test_solution_02_A():
    assert solution_02_A("./02/test_input.txt") == 2  # Replace with expected output for the test case


# def test_final_solution_02_A():
#    assert solution_02_A('./02/input.txt') == 0 # Replace with solution when known


def test_solution_02_B():
    assert solution_02_B("./02/test_input.txt") == 4  # Replace with expected output for the test case


# def test_final_solution_02_B():
#    assert solution_02_B('./02/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("02", sys.argv[1], solution_02_A, solution_02_B)
