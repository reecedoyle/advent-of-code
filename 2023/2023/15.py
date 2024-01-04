# Lens Library

import re
from collections import OrderedDict

file_path = "data/15.txt"

class Step:
    def __init__(self, string):
        match = re.match(r'([^\-\=]+)([\-\=])(\d*)', string)
        self.label = match.group(1)
        self.operator = match.group(2)
        if len(match.group(3)) > 0:
            self.value = int(match.group(3))

    def hash(self):
        hash = 0
        for char in self.label:
            hash = ((hash + ord(char)) * 17) % 256
        return hash
    
class Box:
    def __init__(self):
        self.lenses = OrderedDict()

    def add_lens(self, label, value):
        self.lenses[label] = value

    def remove_lens(self, label):
        if label in self.lenses:
            del self.lenses[label]

    def focusing_power(self):
        total = 0
        for i, lens in enumerate(self.lenses.values()):
            total += (i+1) * lens
        return total

class Boxes:
    def __init__(self):
        self.boxes = {}

    def apply_step(self, step):
        hash = step.hash()
        if hash not in self.boxes:
            self.boxes[hash] = Box()
        box = self.boxes[hash]
        if step.operator == '-':
            box.remove_lens(step.label)
        elif step.operator == '=':
            box.add_lens(step.label, step.value)

    def total_focusing_power(self):
        total = 0
        for i, box in self.boxes.items():
            total += (i+1) * box.focusing_power()
        return total

def parse_input():
    with open(file_path, "r") as file:
        lines = file.read()
    return lines.rstrip('\n').split(',')

def part1():
    input = parse_input()
    sum = 0
    for step in input:
        hash = 0
        for char in step:
            hash = ((hash + ord(char)) * 17) % 256
        sum += hash
    print(sum)

def part2():
    input = parse_input()
    steps = [Step(step) for step in input]
    boxes = Boxes()
    for step in steps:
        boxes.apply_step(step)
    print(boxes.total_focusing_power())

if __name__ == "__main__":
    #part1()
    part2()