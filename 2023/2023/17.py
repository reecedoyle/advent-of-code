# Clumsy Crucible

# need to keep track of cost per direciton and times travelled in direction

from collections import namedtuple
from enum import Flag
from dataclasses import dataclass
from heapq import heapify, heappush, heappop

Point = namedtuple("Point", "x y")

MIN_CONSECUTIVE_STEPS = 4
MAX_CONSECUTIVE_STEPS = 10

class Direction(Flag):
    UP = 1
    DOWN = 2
    LEFT = 4
    RIGHT = 8

OPPOSITE_DIRECTION = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT
}

class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.target = Point(self.rows - 1, self.cols - 1)
        self.average_cost = sum([sum(line) for line in grid]) / float(self.rows * self.cols)

    def __delitem__(self, key):
        self.grid.__delitem__(key)

    def __getitem__(self, key):
        return self.grid.__getitem__(key)

    def __setitem__(self, key, value):
        self.grid.__setitem__(key, value)

@dataclass(frozen=True, order=True)
class NodeVisit:
    point: Point
    direction: Direction
    consecutive_steps: int

    def neighbours(self, grid):
        nodes = []
        for direction in Direction:
            if is_opposite_direction(self.direction, direction):
                continue
            if self.direction == direction:
                if self.consecutive_steps < MAX_CONSECUTIVE_STEPS:
                    nodes.append(NodeVisit(travel(self.point, direction), direction, self.consecutive_steps + 1))
            elif self.consecutive_steps >= MIN_CONSECUTIVE_STEPS:
                nodes.append(NodeVisit(travel(self.point, direction), direction, 1))
        return [node for node in nodes if node.point.x >= 0 and node.point.x < grid.rows \
                and node.point.y >= 0 and node.point.y < grid.cols]

class CostCache:
    def __init__(self, grid):
        self.target = grid.target
        self.cache = [[{d:[float('inf')] * MAX_CONSECUTIVE_STEPS for d in Direction} for _ in range(grid.cols)] for _ in range(grid.rows)]

    def get(self, node):
        # could get min value of all with more steps too?
        return self.cache[node.point.x][node.point.y][node.direction][node.consecutive_steps-1]
    
    def set(self, node, value):
        if value < self.get(node):
            self.cache[node.point.x][node.point.y][node.direction][node.consecutive_steps-1] = value
            return True
        return False

    def get_min_target_cost(self):
        target_costs = self.cache[self.target.x][self.target.y]
        return min([c for _, costs in target_costs.items() for c in costs])

    def get_min_target_node(self):
        target_costs = self.cache[self.target.x][self.target.y]
        min_cost = float('inf')
        min_node = None
        for direction, costs in target_costs.items():
            for i in range(len(costs)):
                if costs[i] < min_cost:
                    min_cost = costs[i]
                    min_node = NodeVisit(self.target, direction, i + 1)
        return min_node

file_path = "data/17.txt"

def parse_input():
    with open(file_path, "r") as file:
        lines = file.readlines()
    return [[int(char) for char in line.rstrip('\n')] for line in lines]

def is_opposite_direction(d1, d2):
    combined = (d1 | d2).value
    return combined == 3 or combined == 12

def travel(point, direction):
    return {
        Direction.UP: Point(point.x - 1, point.y),
        Direction.DOWN: Point(point.x + 1, point.y),
        Direction.LEFT: Point(point.x, point.y - 1),
        Direction.RIGHT: Point(point.x, point.y + 1)
    }[direction]

def estimated_cost(node, costs, grid):
    # idk why a* fucks this up, but it does. so commented out the heuristic.
    entry_cost = costs.get(node)
    #distance_to_target = abs(node.point.x - grid.target.x) + abs(node.point.y - grid.target.y)
    return entry_cost# + distance_to_target * grid.average_cost

# heap/priority queue is better but fuck it
def pop_lowest_cost_node(nodes, costs, grid):
    lowest_cost = float("inf")
    lowest_cost_node = None
    for node in nodes:
        cost = estimated_cost(node, costs, grid)
        if cost < lowest_cost:
            lowest_cost = cost
            lowest_cost_node = node
    nodes.remove(lowest_cost_node)
    return lowest_cost_node

def find_cheapest_path():
    entropy = 0
    input = parse_input()
    grid = Grid(input)
    starting_nodes = [NodeVisit(Point(0, 1), Direction.RIGHT, 1), NodeVisit(Point(1, 0), Direction.DOWN, 1)]
    costs = CostCache(grid)
    prev = {n: None for n in starting_nodes}
    to_visit = []
    heapify(starting_nodes)
    for starting_node in starting_nodes:
        cost = grid[starting_node.point.x][starting_node.point.y]
        costs.set(starting_node, cost)
        heappush(to_visit, (cost, entropy, starting_node))
        entropy += 1
    while len(to_visit) > 0:
        _, _, node = heappop(to_visit)
        current_cost = costs.get(node)
        print("to visit", len(to_visit), "Current cost", current_cost, "Entropy", entropy)
        if current_cost >= costs.get_min_target_cost():
            break
        neighbours = node.neighbours(grid)
        #print("neighbours", len(neighbours))
        for n in neighbours:
            cost_of_entry = grid[n.point.x][n.point.y]
            total_cost = cost_of_entry + current_cost
            if costs.set(n, total_cost):
                prev[n] = node
            heappush(to_visit, (total_cost, entropy, n))
            entropy += 1
        #if len(visited) > 5:
            #break
    print(costs.get_min_target_cost())
    node = costs.get_min_target_node()
    while node is not None:
        print(node, costs.get(node), grid[node.point.x][node.point.y])
        node = prev[node]

def part1():
    MIN_CONSECUTIVE_STEPS = 0
    MAX_CONSECUTIVE_STEPS = 3
    find_cheapest_path()

def part2():
    MIN_CONSECUTIVE_STEPS = 4
    MAX_CONSECUTIVE_STEPS = 10
    find_cheapest_path()
    
if __name__ == "__main__":
    #part1()
    part2()