# Hot Springs

from itertools import combinations, zip_longest
from operator import add

file_path = "data/12.txt"

def parse_input():
    with open(file_path, "r") as file:
        lines = file.readlines()
    lines = [line.rstrip('\n') for line in lines]
    for line in lines:
        row, damaged = line.split()
        yield row, [int(d) for d in damaged.split(',')]

def convert_to_blocks(row):
    return [b for b in row.split('.') if b]

def convert_nums_to_block(nums):
    #print(nums)
    block = ""
    empty = True
    for num in nums:
        if empty:
            block += '.' * num
        else:
            block += '#' * num
        empty = not empty
    return block

def partitions(n, k):
    for c in combinations(range(n+k-1), k-1):
        yield [b-a-1 for a, b in zip((-1,)+c, c+(n+k-1,))]

def get_possible_blocks(total_length, springs):
    #print("get_possible_blocks", total_length, springs)
    possible_gaps = len(springs) + 1
    occupied_space = sum(springs) + (len(springs) - 1)
    free_space = total_length - occupied_space
    space_combos = list(partitions(free_space, possible_gaps))
    possible_blocks = []
    for partition in space_combos:
        combined = [partition[0]]
        for i in range(1, len(partition) + len(springs) - 1):
            if i % 2 == 0:
                combined.append(partition[i//2] + 1) # must have one empty space between springs
            else:
                combined.append(springs[i//2])
        combined.append(partition[-1])
        possible_blocks.append(combined)
    return [convert_nums_to_block(block) for block in possible_blocks]

def get_valid(block, potential_blocks):
    result = []
    for candidate in potential_blocks:
        if len(block) != len(candidate):
            continue
        valid = True
        for i in range(len(block)):
            if candidate[i] == '#' and block[i] == '.':
                valid = False
                #print("is invalid", block, candidate)
            if block[i] == '#' and candidate[i] == '.':
                valid = False
                #print("is invalid", block, candidate)
        if valid:
            #print("is valid", block, candidate)
            result.append(candidate)
    return result

def determine_block_options(block, damaged):
    # for a block, return the number of ways the springs can fit, per number of springs
    # so that we know a) the number of possibilities and b) the number of springs to keep using for the next block
    # return {springs_used: options}
    #print("determine_block_options", block, damaged)
    max_num_springs = 0
    sum = 0
    for springs in damaged:
        if springs <= len(block) - sum:
            max_num_springs += 1
            sum += springs + 1 # for the gap between
        else:
            break
    options = {}
    for n in range(1, max_num_springs + 1):
        #print("n:", n)
        potential_blocks = get_possible_blocks(len(block), damaged[:n])
        valids = get_valid(block, potential_blocks)
        #print("potential_blocks for", n, "->", potential_blocks)
        #print("valid count vs", block, "->", valid_count)
        options[n] = valids
    #print("Options for", block, damaged, options)
    return options

def can_be_empty(blocks):
    for block in blocks:
        if '#' in block:
            return False
    return True

def determine_possibilities(blocks, damaged, prev_blocks=[]):
    #print("Determining:", blocks, damaged, prev_blocks)
    if len(blocks) == 1: # base case, only one block
        spring_options = determine_block_options(blocks[0], damaged)
        valid_options = [options for springs, options in spring_options.items() if springs == len(damaged)]
        base_sum = sum([len(option) for option in valid_options])
        #for option in valid_options:
            #print('.'.join(prev_blocks + option))
        #print("base_sum", base_sum, spring_options)
        return base_sum
    if len(damaged) == 0:
        if can_be_empty(blocks):
            return 1
        else:
            return 0
    if len(blocks[0]) < damaged[0]: # if the next size spring can't fit in this block, move on to the next one
        #print("Next spring can't fit", blocks[0], damaged)
        if '#' not in blocks[0]:
            return determine_possibilities(blocks[1:], damaged, prev_blocks + ['.']*len(blocks[0]))
        else:
            return 0
    # the case where it does fit + multiply this by recursive call for remaining blocks
    spring_options = determine_block_options(blocks[0], damaged)
    #print(spring_options)
    total = 0
    for springs_used, options in spring_options.items():
        if len(options) != 0:
            if springs_used == len(damaged):
                if can_be_empty(blocks[1:]): # if we're done, check no further springs required
                    #for option in options:
                        #print(prev_blocks + [option])
                    total += len(options)
            else:
                for option in options:
                    total += determine_possibilities(blocks[1:], damaged[springs_used:], prev_blocks + [option])
    # Also the case where we use no springs for this block (only if we don't have to)
    if '#' not in blocks[0]:
        total += determine_possibilities(blocks[1:], damaged, prev_blocks)
    #print("total", total)
    return total

def part1():
    input = list(parse_input())
    results = []
    for row, damaged in input:
        print("Starting row", row, damaged)
        blocks = convert_to_blocks(row)
        options = determine_possibilities(blocks, damaged)
        print("options for row:", row, damaged, "->", options)
        results.append(options)
    print(list(enumerate(results)))
    print(results)
    print(sum(results))

def part2():
    input = list(parse_input())
    results = []
    for row, damaged in input:
        print("Starting row", row, damaged)
        blocks = convert_to_blocks(row)
        options = determine_possibilities(blocks, damaged)
        print("options for row:", row, damaged, "->", options)
        results.append(options)
    print(list(enumerate(results)))
    print(results)
    print(sum(results))

if __name__ == "__main__":
    #print(list(get_possible_blocks(10, [4,3])))
    part1()
    #part2()