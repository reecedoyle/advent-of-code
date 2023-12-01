import json

file_path = "data/01.txt"
number_words = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four" : 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine" : 9
}

class NumberParser:
    terminator = '.'
    base_state = dict()
    for word, value in number_words.items():
        current_dict = base_state
        for i, char in enumerate(word):
            if char not in current_dict:
                current_dict[char] = {}
            current_dict = current_dict[char]
            if i == len(word) - 1:
                current_dict[terminator] = value

    def parse(self, line):
        states = []
        for char in line:
            states.append(self.base_state)
            # check if any states have terminated
            for state in states:
                if self.terminator in state:
                    yield state[self.terminator]
                    states.remove(state)
                    break # only one state can terminate at a time
            # break state chains if character is a digit
            if char.isdigit():
                states = []
                yield int(char)
                continue
            # Progress states to next state if character matches transition
            new_states = []
            for state in states:
                if char in state:
                    new_states.append(state[char])
            states = new_states

def main():
    with open(file_path, "r") as file:
        lines = file.readlines()
    calibration_values = []
    parser = NumberParser()
    for line in lines:
        digits = list(parser.parse(line))
        value = int(f"{digits[0]}{digits[-1]}")
        print(f"{line} - {digits} - {value}")
        calibration_values.append(value)
    
    print(sum(calibration_values))  # Print the sum of calibration_values
                

if __name__ == "__main__":
    main()
