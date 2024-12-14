import sys
from typing import Tuple
from common.utils import run
import numpy as np
import re


def parse(filename: str):
    button_re = r"Button .: X\+(\d+), Y\+(\d+)"
    prize_re = r"Prize: X\=(\d+), Y\=(\d+)"
    machines = list()
    with open(filename, 'r') as file:
        while True:
            a_line = file.readline()
            b_line = file.readline()
            p_line = file.readline()
            a_match = list(map(int, re.match(button_re, a_line).groups()))
            b_match = list(map(int, re.match(button_re, b_line).groups()))
            p_match = list(map(int, re.match(prize_re, p_line).groups()))
            machines.append(((a_match[0], a_match[1]), (b_match[0], b_match[1]), (p_match[0], p_match[1])))
            if file.readline() == '':
                break
    return machines


def machine_to_matrix(machine: Tuple[Tuple[int,int],Tuple[int,int],Tuple[int,int]]):
    matrix = np.array([[machine[0][0], machine[1][0]], [machine[0][1], machine[1][1]]])
    result = np.array([machine[2][0], machine[2][1]])
    return matrix, result


def cramer2x2(a, b):
    print(a)
    print(b)
    assert a.shape == (2, 2)
    assert b.size == 2
    d = np.linalg.det(a)
    dx = np.linalg.det(np.column_stack([b, a[:, 1]]))
    dy = np.linalg.det(np.column_stack([a[:, 0], b]))
    return np.array([dx/d, dy/d])


def solution_13_A(filename: str) -> int:
    machines = parse(filename)
    total = 0
    for machine in machines:
        matrix, result = machine_to_matrix(machine)
        solution = np.rint(cramer2x2(matrix, result))
        if (np.matmul(matrix, solution) == result).all():
            total += (3 * solution[0]) + solution[1]
    return total


def solution_13_B(filename: str) -> int:
    np.set_printoptions(suppress=True, formatter={'float_kind':'{:f}'.format})
    additive = 10000000000000
    machines = parse(filename)
    total = 0
    for machine in machines:
        matrix, result = machine_to_matrix(machine)
        result = result + additive
        solution = np.rint(cramer2x2(matrix, result))
        expected = np.rint(np.matmul(matrix, solution))
        if (expected == result).all():
            total += (3 * solution[0]) + solution[1]
    return int(total)


def test_solution_13_A():
    assert solution_13_A("./13/test_input.txt") == 480  # Replace with expected output for the test case


# def test_final_solution_13_A():
#    assert solution_13_A('./13/input.txt') == 0 # Replace with solution when known


def test_solution_13_B():
    assert solution_13_B("./13/test_input.txt") == 875318608908  # Replace with expected output for the test case


# def test_final_solution_13_B():
#    assert solution_13_B('./13/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("13", sys.argv[1], solution_13_A, solution_13_B)
