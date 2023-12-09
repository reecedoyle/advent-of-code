# Mirage Maintenance

file_path = "data/09.txt"

def parse_input():
    with open(file_path, "r") as file:
        lines = file.readlines()
    lines = [line.rstrip('\n').split() for line in lines]
    return [[(int(elem)) for elem in line] for line in lines]

def get_differences(sequence):
    differences = []
    for i in range(len(sequence) - 1):
        diff = sequence[i+1] - sequence[i]
        differences.append(diff)
    return differences

def get_next_in_sequence(sequence):
    total = sequence[-1]
    diffs = get_differences(sequence)
    while not all(diff == 0 for diff in diffs):
        total += diffs[-1]
        diffs = get_differences(diffs)
    return total

def get_previous_in_sequence(sequence):
    total = sequence[0]
    diffs = get_differences(sequence)
    sign = 1
    while not all(diff == 0 for diff in diffs):
        sign = sign * -1
        total += diffs[0] * sign
        diffs = get_differences(diffs)
    return total

def part1():
    input = parse_input()
    total = 0
    for line in input:
        total += get_next_in_sequence(line)
    print(total)

def part2():
    input = parse_input()
    total = 0
    for line in input:
        total += get_previous_in_sequence(line)
    print(total)

if __name__ == "__main__":
    #part1()
    part2()