from collections import defaultdict
import math
import sys
from typing import List, Set, Tuple
from common.utils import read_lines, run


def read_input(filename: str) -> Tuple[List[str], List[str]]:
    rules = []
    updates = []
    current = rules
    lines = read_lines(filename)
    for line in lines:
        if line == "\n":
            current = updates
        else:
            current.append(line.strip())
    return rules, updates


def backwards_dict(rules: List[Tuple[int, int]]) -> dict[int, set[int]]:
    rule_dict = {}
    for first, second in rules:
        if second in rule_dict:
            rule_dict[second] |= {first}
        else:
            rule_dict[second] = {first}
    return rule_dict


def forwards_dict(rules: List[Tuple[int, int]]) -> dict[int, set[int]]:
    rule_dict = {}
    for first, second in rules:
        if first in rule_dict:
            rule_dict[first] |= {second}
        else:
            rule_dict[first] = {second}
    return rule_dict


def parse_rules(rules: List[str]) -> List[Tuple[int, int]]:
    rule_list = []
    for rule in rules:
        parts = [int(x) for x in rule.split("|")]
        rule_list.append((parts[0], parts[1]))
    return rule_list


def order(pages: Set[int], rules: List[Tuple[int, int]]) -> List[int]:
    relevant_rules = [r for r in rules if r[0] in pages and r[1] in pages]
    rules_adj = defaultdict(set, forwards_dict(relevant_rules))
    paths_in = defaultdict(int)
    ordered_pages = list()
    for v in rules_adj.values():
        for e in v:
            paths_in[e] += 1
    while len(ordered_pages) < len(pages):
        for page in pages:
            if paths_in[page] == 0:
                paths_in[page] -= 1 # so we don't revisit
                ordered_pages.append(page)
                for e in rules_adj[page]:
                    paths_in[e] -= 1
    return ordered_pages


def solution_05_A(filename: str) -> int:
    input = read_input(filename)
    parsed_rules = parse_rules(input[0])
    rules = backwards_dict(parsed_rules) # latter page points to earlier page
    sum = 0
    for update in input[1]:
        unwanted_pages = set() # if we see these, pages are out of order
        pages = [int(p) for p in update.split(",")]
        valid = True
        for page in pages:
            if page in unwanted_pages:
                valid = False
                break
            if page in rules:
                unwanted_pages |= rules[page]
        if valid:
            sum += pages[len(pages)//2]
    return sum

def solution_05_B(filename: str) -> int:
    input = read_input(filename)
    parsed_rules = parse_rules(input[0])
    rules = backwards_dict(parsed_rules) # latter page points to earlier page
    sum = 0
    for update in input[1]:
        unwanted_pages = set() # if we see these, pages are out of order
        pages = [int(p) for p in update.split(",")]
        for page in pages:
            if page in unwanted_pages:
                ordered = order(pages, parsed_rules)
                sum += ordered[len(ordered)//2]
                break
            if page in rules:
                unwanted_pages |= rules[page]
    return sum


def test_solution_05_A():
    assert solution_05_A("./05/test_input.txt") == 143  # Replace with expected output for the test case


# def test_final_solution_05_A():
#    assert solution_05_A('./05/input.txt') == 0 # Replace with solution when known


def test_solution_05_B():
    assert solution_05_B("./05/test_input.txt") == 123  # Replace with expected output for the test case


# def test_final_solution_05_B():
#    assert solution_05_B('./05/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("05", sys.argv[1], solution_05_A, solution_05_B)
