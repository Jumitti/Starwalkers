import json
import math
import os
import random

import telepot

from starwalkers.user_manager import save_json, load_json, load_db_id_username


with open("SECRETS.json", 'r') as secrets_file:
    secrets = json.load(secrets_file)
bot = telepot.Bot(secrets["token"])


def settings_file():
    with open("starwalkers/settings.json", 'r') as settings_files:
        settings = json.load(settings_files)

        return settings


def got_let_int(ggg):  # Letter value
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
        "Z": 1
    }
    return letters.get(ggg, 0)


def roll(minimum=None, maximum=None, letter=None, number=None):  # Generate, modify ships
    # li = input()
    # fi += 1
    if letter is None:
        letters = ["*", 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                   'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        probabilities = []
        for x in range(0, len(letters)):
            probabilities.append(math.exp(0.15 * x))

        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]
        ship_let = random.choices(letters, weights=probabilities)[0]

        # ran = random.randint(1, 351)
        # if ran == 1:
        #     ship_let = "A"
        # elif ran <= 3:
        #     ship_let = "B"
        # elif ran <= 6:
        #     ship_let = "C"
        # elif ran <= 10:
        #     ship_let = "D"
        # elif ran <= 15:
        #     ship_let = "E"
        # elif ran <= 21:
        #     ship_let = "F"
        # elif ran <= 28:
        #     ship_let = "G"
        # elif ran <= 36:
        #     ship_let = "H"
        # elif ran <= 45:
        #     ship_let = "I"
        # elif ran <= 55:
        #     ship_let = "J"
        # elif ran <= 66:
        #     ship_let = "K"
        # elif ran <= 78:
        #     ship_let = "L"
        # elif ran <= 91:
        #     ship_let = "M"
        # elif ran <= 105:
        #     ship_let = "N"
        # elif ran <= 120:
        #     ship_let = "O"
        # elif ran <= 136:
        #     ship_let = "P"
        # elif ran <= 153:
        #     ship_let = "Q"
        # elif ran <= 171:
        #     ship_let = "R"
        # elif ran <= 190:
        #     ship_let = "S"
        # elif ran <= 210:
        #     ship_let = "T"
        # elif ran <= 231:
        #     ship_let = "U"
        # elif ran <= 253:
        #     ship_let = "V"
        # elif ran <= 276:
        #     ship_let = "W"
        # elif ran <= 300:
        #     ship_let = "X"
        # elif ran <= 325:
        #     ship_let = "Y"
        # elif ran <= 351:
        #     ship_let = "Z"
    else:
        ship_let = letter

    minimum = 0 if minimum is None else minimum
    maximum = 9999 if maximum is None else maximum
    ran = random.randint(minimum, maximum) if number is None else number

    niki = ship_let + "-" + str(ran)
    return niki


# Can be deprecated with modification of roll()
# def get_int_ship(self_int):
#     if int(self_int) / 10 >= 1:
#         if int(self_int) / 100 >= 1:
#             if int(self_int) / 1000 >= 1:
#                 niki = "-" + str(self_int)
#             elif int(self_int) / 1000 < 1:
#                 niki = "-0" + str(self_int)
#         elif int(self_int) / 100 < 1:
#             niki = "-00" + str(self_int)
#     elif int(self_int) / 10 < 1:
#         niki = "-000" + str(self_int)
#     return niki


def get_d_sym(a):  # Cost to dollar
    number_d_sym = a / 50
    total = "$"
    for i in range(0, int(number_d_sym)):
        total += "|$"

    # if a <= 20:
    #     total = "$"
    # elif a <= 70:
    #     total = "$|$"
    # elif a <= 120:
    #     total = "$|$|$"
    # elif a <= 200:
    #     total = "$|$|$|$"
    # else:
    #     total = "$|$|$|$|$"

    return total


def get_cost(a):  # Get cost of a ship
    s_let, s_int = a.split("-")
    cost = (got_let_int(s_let) * int(s_int)) // 1000
    return cost


def daily_reward():  # Daily reward
    data = load_db_id_username()
    for user_id, username in data.items():
        daily_reward = random.randint(30, 50)
        ID_info = load_json(user_id)
        money = ID_info['money']
        money_win = ID_info['money_win']
        money += daily_reward
        money_win += daily_reward
        message = f"Good morning Captain {username}. Here is your daily salary {daily_reward}$. May the space conquest be with you !"
        bot.sendMessage(user_id, message)
        save_json(user_id, money=money, money_win=money_win)


def upgrade_fleet(fleet_size):
    x1 = 10
    y1 = 0.5
    x2 = 40
    y2 = 1
    slope = (y2 - y1) / (x2 - x1)
    if fleet_size < 50:
        y_fleet_size = y1 + (fleet_size - x1) * slope
        price = math.floor(100 * math.exp(5 * y_fleet_size))
    elif fleet_size == 50:
        y_fleet_size = y1 + (100 - x1) * slope
        price = math.floor(100 * math.exp(5 * y_fleet_size))
    return price
