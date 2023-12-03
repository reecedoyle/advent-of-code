# Gear Ratios

file_path = "data/03.txt"

def parse_input():
    with open(file_path, "r") as file:
        lines = file.readlines()
    lines = [line.rstrip('\n') for line in lines]  # Strip newlines from lines
    data = [[0 for j in range(len(lines[i]))] for i in range(len(lines))]
    for i in range(0, len(lines)):
        number_string = ""
        for j in range(0, len(lines[i])):
            if not lines[i][j].isdigit():
                if len(number_string) > 0:
                    num = int(number_string)
                    for n in range(0, len(number_string)):
                        data[i][j-n-1] = num
                    number_string = ""
                data[i][j] = lines[i][j]
                continue
            number_string += lines[i][j]
            if j == len(lines[i]) - 1:
                num = int(number_string)
                for n in range(0, len(number_string)):
                    data[i][j-n] = num
    return data
    

def is_symbol(character):
    return not character.isalpha() and not character.isdigit() and character != '.'

def extract_parts_from_line(before, line, after):
    prev_col_has_symbol = False
    current_number = 0
    num_is_adjacent_to_symbol = False
    for i in range(0, len(line)):
        is_symbol_above = (before is not None and is_symbol(before[i]))
        is_symbol_below = (after is not None and is_symbol(after[i]))
        is_adjacent_to_symbol = is_symbol_above or is_symbol_below or prev_col_has_symbol
        current_col_has_symbol = is_symbol(line[i]) or is_symbol_above or is_symbol_below
        if line[i].isdigit():
            num_is_adjacent_to_symbol = num_is_adjacent_to_symbol or is_adjacent_to_symbol
            current_number *= 10
            current_number += int(line[i])
            if is_adjacent_to_symbol:
                if i == len(line) - 1:
                    yield current_number
                continue # Already confirmed this number so keep going
        elif current_number != 0: # We have just finished a number
            if num_is_adjacent_to_symbol or current_col_has_symbol:
                yield current_number
            current_number = 0
            num_is_adjacent_to_symbol = False
        prev_col_has_symbol = current_col_has_symbol

def get_parts_for_gear(gear, data):
    x, y = gear
    parts = []
    if y > 0: # check left
        if isinstance(data[x][y-1], int):
            parts.append(data[x][y-1])
    if y < len(data[x]) - 1: # check right
        if isinstance(data[x][y+1], int):
            parts.append(data[x][y+1])
    if x > 0:
        top_left = y > 0 and isinstance(data[x-1][y-1], int)
        top = isinstance(data[x-1][y], int)
        top_right = y < len(data[x]) - 1 and isinstance(data[x-1][y+1], int)
        if top_left and not top:
            parts.append(data[x-1][y-1])
        if top:
            parts.append(data[x-1][y])
        if top_right and not top:
            parts.append(data[x-1][y+1])
    if x < len(data) - 1:
        bottom_left = y > 0 and isinstance(data[x+1][y-1], int)
        bottom = isinstance(data[x+1][y], int)
        bottom_right = y < len(data[x]) - 1 and isinstance(data[x+1][y+1], int)
        if bottom_left and not bottom:
            parts.append(data[x+1][y-1])
        if bottom:
            parts.append(data[x+1][y])
        if bottom_right and not bottom:
            parts.append(data[x+1][y+1])
    return parts

def part1():
    with open(file_path, "r") as file:
        lines = file.readlines()
    lines = [line.rstrip('\n') for line in lines]  # Strip newlines from lines
    total = 0
    for i in range(0, len(lines)):
        if i == 0:
            before = None
        else:
            before = lines[i-1]
        if i == len(lines) - 1:
            after = None
        else:
            after = lines[i+1]
        parts = list(extract_parts_from_line(before, lines[i], after))
        total += sum(parts)
        print(lines[i])
        print(parts)
    print(total)

def part2():
    data = parse_input()
    gears = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == '*':
                gears.append((i, j))
    gear_parts = {gear: get_parts_for_gear(gear, data) for gear in gears}
    ratios = [parts[0] * parts[1] for gear, parts in gear_parts.items() if len(parts) == 2]
    print(sum(ratios))
        

if __name__ == "__main__":
    part2()
