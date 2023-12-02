from functools import reduce
import operator

file_path = "data/02.txt"

def parse_line(line):
    game_str, all_rounds = line.split(":")
    game_num = int(game_str.split(" ")[1])
    rounds = all_rounds.split(";")
    round_counts = []
    for round in rounds:
        counts = {}
        round = round.strip()
        colour_strings = round.split(",")
        for colour_string in colour_strings:
            colour_string = colour_string.strip()
            count, colour = colour_string.split(" ")
            counts[colour] = int(count)
        round_counts.append(counts)
    return game_num, round_counts

def parse_input():
    game_data = {}
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            game, data = parse_line(line)
            game_data[game] = data
    return game_data
            
    

def part1():
    game_data = parse_input()
    limits = {
        "red": 12,
        "green": 13,
        "blue": 14
    }
    legal_games = set()
    for game, data in game_data.items():
        bad_game = False
        for round in data:
            for colour, count in round.items():
                if count > limits[colour]:
                    bad_game = True
                    break
            if bad_game:
                break
        if not bad_game:
            legal_games.add(game)

    print(legal_games)
    print(sum(legal_games))


def part2():
    game_data = parse_input()
    powers = []
    for game, data in game_data.items():
        colour_maxs = {}
        for round in data:
            for colour, count in round.items():
                if colour not in colour_maxs:
                    colour_maxs[colour] = count
                else:
                    colour_maxs[colour] = max(colour_maxs[colour], count)
        powers.append(reduce(operator.mul, colour_maxs.values()))
    print(sum(powers))

if __name__ == "__main__":
    part2()

