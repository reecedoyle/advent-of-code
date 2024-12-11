from collections import Counter, defaultdict
import sys
from typing import Dict, List, Set
from common.utils import run, read_lines


def blink(stone: int) -> List[int]:
    if stone == 0:
        return [1]
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        mid = len(stone_str) // 2
        return [int(stone_str[:mid]), int(stone_str[mid:])]
    return [stone * 2024]


def repeat_blink(stones: Set[int], repetitions: int):
    counts = {s: 1 for s in stones}
    for i in range(0, repetitions):
        print(f"repetition {i}")
        next_counts = defaultdict(int)
        for stone, count in counts.items():
            for next_stone in blink(stone):
                next_counts[next_stone] += count
        counts = next_counts
    return sum(counts.values())


def solution_11_A(filename: str) -> int:
    line = read_lines(filename)[0]
    stones = list(map(int, line.split()))
    return repeat_blink(set(stones), 25)


def solution_11_B(filename: str) -> int:
    line = read_lines(filename)[0]
    stones = list(map(int, line.split()))
    return repeat_blink(set(stones), 75)


def test_solution_11_A():
    assert solution_11_A("./11/test_input.txt") == 55312  # Replace with expected output for the test case


# def test_final_solution_11_A():
#    assert solution_11_A('./11/input.txt') == 0 # Replace with solution when known


def test_solution_11_B():
    assert solution_11_B("./11/test_input.txt") == 0  # Replace with expected output for the test case


# def test_final_solution_11_B():
#    assert solution_11_B('./11/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("11", sys.argv[1], solution_11_A, solution_11_B)
