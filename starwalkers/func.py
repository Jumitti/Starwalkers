import json
import math
import random


def got_let_int(letter):  # Letter value
    letters = {
        "*": 100,
        "A": 26,
        "B": 25,
        "C": 24,
        "D": 23,
        "E": 22,
        "F": 21,
        "G": 20,
        "H": 19,
        "I": 18,
        "J": 17,
        "K": 16,
        "L": 15,
        "M": 14,
        "N": 13,
        "O": 12,
        "P": 11,
        "Q": 10,
        "R": 9,
        "S": 8,
        "T": 7,
        "U": 6,
        "V": 5,
        "W": 4,
        "X": 3,
        "Y": 2,
        "Z": 1}
    return letters.get(letter, 0)


def roll(proba_letter=None, proba_number=None, number_min=None, number_max=None, letter_min=None, letter_max=None, number=None, letter=None):  # Generate, modify ships
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
               'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    if letter_min or letter_max:
        min_index = letters.index(letter_min.upper())
        max_index = letters.index(letter_max.upper())
        if min_index < max_index:
            sub_letters = letters[min_index:max_index + 1]
        else:
            sub_letters = letters[max_index:min_index + 1]
        ship_let = random.choice(sub_letters)

    elif letter is not None:
        ship_let = letter

    else:
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                   'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        with open(f'probabilities/probabilities_letter_{proba_letter}.json', 'r') as f:
            probabilities = json.load(f)
        ship_let = random.choices(letters, weights=probabilities)[0]

    if number_min or number_max:
        number_min = 0 if number_min is None else number_min
        number_max = 9999 if number_max is None else number_max
        ran = random.randint(number_min, number_max) if number is None else number

    elif number is not None:
        ran = number

    else:
        digits = list(range(10000))
        with open(f'probabilities/probabilities_number_{proba_number}.json', 'r') as f:
            probabilities_number = json.load(f)
        ran = random.choices(digits, weights=probabilities_number)[0]

    niki = ship_let + "-" + str(ran).zfill(4)
    return niki


def get_d_sym(a):  # Cost to dollar
    number_d_sym = a / 50
    total = "$"
    for i in range(0, int(number_d_sym)):
        total += "$"

    return total


def get_cost(a):  # Get cost of a ship
    letter, number = a.split("-")
    cost = (got_let_int(letter) * int(number)) // 1000
    return cost


def upgrade_fleet(fleet_size):
    x1 = 10
    y1 = 0.5
    x2 = 40
    y2 = 1
    slope = (y2 - y1) / (x2 - x1)
    y_fleet_size = y1 + (fleet_size - x1) * slope
    price = math.floor(100 * math.exp(5 * y_fleet_size))
    return price


def upgrade(grade):
    price = math.floor(1000 * math.exp(0.35 * (grade + 1)))
    return price
