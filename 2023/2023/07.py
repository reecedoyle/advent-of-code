# Camel Cards

from dataclasses import dataclass

file_path = "data/07.txt"

def parse_input():
    with open(file_path, "r") as file:
        lines = file.readlines()
    lines = [line.rstrip('\n').split() for line in lines]
    return [(line[0], int(line[1])) for line in lines]

@dataclass
class Card:
    _card_values = {
        "?": 1,  # Joker
        "2": 2,
        "3": 3,
        "4": 4,
        "5" : 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9" : 9,
        "T": 10,
        "J": 11,
        "Q": 12,
        "K" : 13,
        "A": 14,
    }

    def __init__(self, name, jokers_active=False):
        self.is_joker = False
        if jokers_active and name == 'J':
            name = '?'
            self.is_joker = True
        self.name = name
        self.value = self._card_values[name]

    def __repr__(self): 
        return self.name

    def __lt__(self, other):
        return self.value < other.value
    
@dataclass
class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid
        self.card_count = self.count_cards()
        self.type_score = self.score_hand_type()

    def __repr__(self):
        return f"{self.cards} - {self.bid} - {self.type_score}"

    def count_cards(self):
        # handle jokers ('?') here
        card_count = {}
        normal_cards = []
        jokers = []
        for card in self.cards:
            (jokers if card.is_joker else normal_cards).append(card)
        for card in normal_cards:
            if card.value in card_count:
                card_count[card.value] += 1
            else:
                card_count[card.value] = 1
        num_jokers = len(jokers)
        if num_jokers == 5:
            return {1: 5}  # No normal cards
        if num_jokers > 0:
            max_count = 0
            max_value = 0
            for value, count in card_count.items():
                if count > max_count:
                    max_count = count
                    max_value = value
            card_count[max_value] += num_jokers
        return card_count

    def score_hand_type(self):
        score = 0
        for count in self.card_count.values():
            score += (10 ** (count - 1))
        return score

    def __lt__(self, other):
        if self.type_score < other.type_score:
            return True
        elif self.type_score > other.type_score:
            return False
        for i in range(5):
            if self.cards[i] < other.cards[i]:
                return True
            elif self.cards[i] > other.cards[i]:
                return False
        return False #  equal

def part1():
    input = parse_input()
    hands = []
    for cards, bid in input:
        print(cards, bid)
        cards = [Card(card) for card in cards]
        hands.append(Hand(cards, bid))
    hands = sorted(hands)
    score = 0
    for i, hand in enumerate(hands):
        print(i + 1,hand)
        score += hand.bid * (i + 1)
    print(score)

def part2():
    input = parse_input()
    hands = []
    for cards, bid in input:
        print(cards, bid)
        cards = [Card(card, jokers_active=True) for card in cards]
        hands.append(Hand(cards, bid))
    hands = sorted(hands)
    score = 0
    for i, hand in enumerate(hands):
        print(i + 1,hand)
        score += hand.bid * (i + 1)
    print(score)

if __name__ == "__main__":
    # part1()
    part2()
