# If You Give A Seed A Fertilizer

file_path = "data/05.txt"

class Mapper:
    def __init__(self, mappings):
        self.mappings = mappings

    def map(self, seed):
        for mapping in self.mappings:
            dest, source, length = mapping
            if seed >= source and seed < source + length:
                return dest + (seed - source)
        return seed

def parse_input():
    with open(file_path, "r") as file:
        lines = file.readlines()
    lines = [line.rstrip('\n') for line in lines]  # Strip newlines from lines
    # parse seeds
    line = lines[0]
    seeds = [int(seed) for seed in line.split(':')[1].strip().split()]
    all_mappings = []
    current_mapping = []
    for line in lines[2:]:
        if len(line) == 0:
            continue
        if not line[0].isdigit():
            if len(current_mapping) > 0:
                all_mappings.append(current_mapping)
                current_mapping = []
            continue # Don't bother with mapping names, rely on ordering instead
        values = tuple([int(value) for value in line.split()])
        current_mapping.append(values)
    all_mappings.append(current_mapping)
    return seeds, all_mappings

def get_ranged_seeds(seeds):
    for i in range(0, len(seeds), 2):
        for j in range(seeds[i+1]):
            yield seeds[i] + j

def part1():
    input = parse_input()
    mappers = [Mapper(mappings) for mappings in input[1]]
    output = input[0]
    for mapper in mappers:
        for i in range(len(output)):
            output[i] = mapper.map(output[i])
    print(sorted(output))

def part2():
    input = parse_input()
    seeds = input[0]
    seeds = list(get_ranged_seeds(seeds))
    print(len(seeds))
    mappers = [Mapper(mappings) for mappings in input[1]]
    output = input[0]
    for mapper in mappers:
        for i in range(len(output)):
            output[i] = mapper.map(output[i])
    print(sorted(output))

if __name__ == "__main__":
    part2()

        