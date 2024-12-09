from collections import defaultdict
from dataclasses import dataclass
import sys
from typing import List
from common.utils import run, read_lines


def get_checksum(start: int, length: int, value: int):
    return sum([i * value for i in range(start, start + length)])


def get_file_id(index: int):
    return index // 2


def solution_09_A(filename: str) -> int:
    lines = read_lines(filename)
    line = list(map(int, lines[0]))
    checksum = 0
    i = 0
    sparse_i = 0
    j = len(line) - 1 # make sure it's not a gap (not odd)
    if j % 2 == 1:
        j -= 1
    while i <= j:
        if i % 2 == 0: # not a gap
            checksum += get_checksum(sparse_i, line[i], get_file_id(i))
            sparse_i += line[i]
            i += 1
        else:
            diff = line[j] - line[i] # fill the gap
            if diff > 0:
                checksum += get_checksum(sparse_i, line[i], get_file_id(j))
                line[j] = diff # reduce to remainder
                sparse_i += line[i]
                i += 1 # move on
            elif diff < 0:
                checksum += get_checksum(sparse_i, line[j], get_file_id(j))
                line[i] = diff * -1 # set to remainder
                sparse_i += line[j]
                j -= 2 # move to next
            else:
                checksum += get_checksum(sparse_i, line[i], get_file_id(j))
                sparse_i += line[i]
                i += 1
                j -= 2
    return checksum


@dataclass
class Gap:
    index: int
    size: int
    filled: List[int]

    def remainder(self):
        return self.size - len(self.filled)


def solution_09_B(filename: str) -> int:
    lines = read_lines(filename)
    line = list(map(int, lines[0]))
    gaps = [Gap(i, x, list()) for i, x in enumerate(line) if i % 2 == 1]
    i = 0
    j = len(line) - 1 # make sure it's not a gap (not odd)
    checksum = 0
    if j % 2 == 1:
        j -= 1
    while j >= 0:
        for gap in gaps:
            if gap.index >= j:
                break
            if gap.remainder() <= 0:
                continue
            diff = gap.remainder() - line[j]
            if diff < 0: # doesn't fit
                continue
            else:
                gap.filled.extend([get_file_id(j)] * line[j])
                gaps.append(Gap(j, line[j], list()))
                break
        j -= 2 # go to next block
    gaps_dict = {gap.index : gap for gap in gaps}
    sparse_i = 0
    for i in range(0, len(line)):
        if i in gaps_dict:
            for fill in gaps_dict[i].filled:
                checksum += fill * sparse_i
                sparse_i += 1
            sparse_i += gaps_dict[i].remainder()
        else:
            checksum += get_checksum(sparse_i, line[i], get_file_id(i))
            sparse_i += line[i]
    return checksum


def test_solution_09_A():
    assert solution_09_A("./09/test_input.txt") == 1928  # Replace with expected output for the test case


# def test_final_solution_09_A():
#    assert solution_09_A('./09/input.txt') == 0 # Replace with solution when known


def test_solution_09_B():
    assert solution_09_B("./09/test_input.txt") == 2858  # Replace with expected output for the test case


# def test_final_solution_09_B():
#    assert solution_09_B('./09/input.txt') == 0 # Replace with solution when known


def test_get_checksum():
    assert get_checksum(0, 3, 2) == 0*2 + 1*2 + 2*2
    assert get_checksum(4, 3, 7) == 4*7 + 5*7 + 6*7


def test_get_file_id():
    assert get_file_id(0) == 0
    assert get_file_id(3) == 1
    assert get_file_id(5) == 2

if __name__ == "__main__":
    run("09", sys.argv[1], solution_09_A, solution_09_B)
