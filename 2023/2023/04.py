# Scratchcards

file_path = "data/04.txt"

def parse_input():
    with open(file_path, "r") as file:
        lines = file.readlines()
    lines = [line.rstrip('\n') for line in lines]  # Strip newlines from lines
    return [parse_line(line) for line in lines]

def parse_line(line):
    card_str, rest = line.split(":")
    winners_str, chosen_str = rest.strip().split("|")
    winners = set([int(winner) for winner in winners_str.strip().split()])
    chosen = list([int(chosen) for chosen in chosen_str.strip().split()])
    return winners, chosen

def card_matches(card):
    match_count = 0
    winners, chosen = card
    for number in chosen:
        if number in winners:
            match_count += 1
    return match_count

def part1():
    cards = parse_input()
    total_score = 0
    for card in cards:
        winners, chosen = card
        score = 0
        for number in chosen:
            if number in winners:
                if score == 0:
                    score = 1
                else:
                    score *= 2
        total_score += score
    print(total_score)

def part2():
    cards = parse_input()
    carryover_cards = []
    card_count = 0
    for card_num, card in enumerate(cards):
        new_copies = []
        # original
        card_count += 1
        match_count = card_matches(card)
        if match_count > 0:
            new_copies.append(match_count)
        # copies
        for i in range(len(carryover_cards)):
            card_count += 1
            match_count = card_matches(card)
            carryover_cards[i] -= 1
            if match_count > 0:
                new_copies.append(match_count)
        carryover_cards = [card for card in carryover_cards if card > 0]
        carryover_cards.extend(new_copies)
        
    print(card_count)

if __name__ == "__main__":
    part2()