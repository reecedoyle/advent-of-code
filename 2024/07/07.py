import sys
from typing import List, Tuple
from common.utils import run, read_lines


def parse_input(lines: List[str]) -> List[Tuple[int, List[int]]]:
    result = list()
    for line in lines:
        parts = line.split()
        result.append((int(parts[0].strip(':')), list(map(int, parts[1:]))))
    return result


def int_concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def is_equation(total: int, numbers: List[int], acc: int = None, allow_concat=False) -> bool:
    if acc is None:
        return is_equation(total, numbers[1:], numbers[0], allow_concat)
    if len(numbers) == 0:
        return acc == total
    if acc > total:
        return False # there are no negative numbers of 0s in the input so quit early
    sum = is_equation(total, numbers[1:], acc + numbers[0], allow_concat)
    mul = is_equation(total, numbers[1:], acc * numbers[0], allow_concat)
    if allow_concat:
        concat = is_equation(total, numbers[1:], int_concat(acc, numbers[0]), allow_concat)
        return sum or mul or concat
    return sum or mul


def solution_07_A(filename: str) -> int:
    lines = read_lines(filename)
    data = parse_input(lines)
    sum = 0
    for total, numbers in data:
        if is_equation(total, numbers):
            sum += total
    return sum


def solution_07_B(filename: str) -> int:
    lines = read_lines(filename)
    data = parse_input(lines)
    sum = 0
    for total, numbers in data:
        if is_equation(total, numbers, allow_concat=True):
            sum += total
    return sum


def test_solution_07_A():
    assert solution_07_A("./07/test_input.txt") == 3749  # Replace with expected output for the test case


# def test_final_solution_07_A():
#    assert solution_07_A('./07/input.txt') == 0 # Replace with solution when known


def test_solution_07_B():
    assert solution_07_B("./07/test_input.txt") == 11387  # Replace with expected output for the test case


# def test_final_solution_07_B():
#    assert solution_07_B('./07/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("07", sys.argv[1], solution_07_A, solution_07_B)
