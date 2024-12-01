import sys
from common.utils import run


def solution_DD_A(filename: str) -> int:
    return 0


def solution_DD_B(filename: str) -> int:
    return 0


def test_solution_DD_A():
    assert solution_DD_A("./DD/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_DD_A():
#    assert solution_DD_A('./DD/input.txt') == 0 # Replace with solution when known


def test_solution_DD_B():
    assert solution_DD_B("./DD/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_DD_B():
#    assert solution_DD_B('./DD/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("DD", sys.argv[1], solution_DD_A, solution_DD_B)
