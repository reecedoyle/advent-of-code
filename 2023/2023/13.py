# Point of Incidence

file_path = "data/13.txt"

def parse_input():
    with open(file_path, "r") as file:
        lines = file.readlines()
    lines = [line.rstrip('\n') for line in lines]
    sublists = [[]]
    for line in lines:
        if line == "":
            sublists.append([])
        else:
            sublists[-1].append(line)
    return sublists

def check_horizontally_mirrored(plane, i):
    if i < 1 or i >= len(plane):
        return False
    a = i - 1
    b = i
    while a >= 0 and b < len(plane):
        if plane[a] != plane[b]:
            return False
        a -= 1
        b += 1
    return True

def find_horizontal_mirror(plane):
    for i in range(1, len(plane)):
        if check_horizontally_mirrored(plane, i):
            return i
    return 0

def get_smudges_required(line, other_line):
    smudges = []
    for i in range(len(line)):
        if line[i] != other_line[i]:
            smudges.append(i)
    return smudges

def check_horizontally_mirrored_with_smudge(plane, i):
    if i < 1 or i >= len(plane):
        return False
    a = i - 1
    b = i
    smudged = None
    while a >= 0 and b < len(plane):
        if plane[a] != plane[b]:
            if smudged is not None: # already smudged, no more allowed
                return False
            required_smudges = get_smudges_required(plane[a], plane[b])
            if len(required_smudges) > 1:
                return False
            smudged = (a, required_smudges[0])
        a -= 1
        b += 1
    if smudged is None:
        return False
    print(smudged)
    return True

def find_horizontal_mirror_with_smudge(plane):
    for i in range(1, len(plane)):
        if check_horizontally_mirrored_with_smudge(plane, i):
            return i
    return 0

def transpose(plane):
    return list([''.join(l) for l in map(list, zip(*plane))])
    
def part1():
    input = parse_input()
    h = 0
    v = 0
    for plane in input:
        hi = find_horizontal_mirror(plane)
        if hi == 0:
            vi = find_horizontal_mirror(transpose(plane))
            print("vi", vi)
            v += vi
        else:
            h += hi
            print("hi", hi)
    print((100*h) + v)
    
def part2():
    input = parse_input()
    h = 0
    v = 0
    for plane in input:
        hi = find_horizontal_mirror_with_smudge(plane)
        if hi == 0:
            vi = find_horizontal_mirror_with_smudge(transpose(plane))
            print("vi", vi)
            v += vi
        else:
            h += hi
            print("hi", hi)
    print((100*h) + v)

if __name__ == "__main__":
    #part1()
    part2()
