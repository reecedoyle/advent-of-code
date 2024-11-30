# Day 8: Haunted Wasteland

import re
from itertools import cycle

file_path = "data/08.txt"


def parse_input():
    with open(file_path, "r") as file:
        lines = file.readlines()
    lines = [line.rstrip('\n') for line in lines]
    nodes = {}
    for line in lines[2:]:
        match = re.match(r'(.{3}) \= \((.{3})\, (.{3})\)', line)
        if match:
            nodes[match.group(1)] = {'L': match.group(2), 'R': match.group(3)}
        else:
            print(f"Error couldn't match {line}")
    return (lines[0], nodes)

def part1():
    directions, nodes = parse_input()
    directions = cycle(directions)
    current_node = 'AAA'
    step_count = 0
    while(current_node != 'ZZZ'):
        step_count += 1
        direction = next(directions)
        current_node = nodes[current_node][direction]
    print(step_count)

def part2():
    directions, nodes = parse_input()
    directions = cycle(directions)
    # get all nodes that start end with A
    current_nodes = [node for node in nodes.keys() if node[-1] == 'A']
    print(current_nodes)
    step_count = 0
    while(not all(node[-1] == 'Z' for node in current_nodes)):
        step_count += 1
        direction = next(directions)
        for i in range(len(current_nodes)):
            current_nodes[i] = nodes[current_nodes[i]][direction]
            print(step_count)
    print(step_count)

if __name__ == "__main__":
    # part1()
    part2()