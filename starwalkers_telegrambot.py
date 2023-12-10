import random
import os
import re
import time
from datetime import datetime
import telepot
from telepot.loop import MessageLoop
import json
import requests
# import termcolor
# from termcolor import colored, cprint
from func import roll, got_let_int, get_int_ship, get_d_sym, get_cost

script_directory = os.path.dirname(os.path.abspath(__file__))
secrets_path = os.path.join(script_directory, 'SECRETS.json')
with open(secrets_path, 'r') as secrets_file:
    secrets = json.load(secrets_file)

chat_id_owner = secrets['id_owner']
clear = lambda: os.system('cls')
money = 30
user_case = 0
ship_list = []

save_tree_choice = {}
save_leaf_choice = {}


def save(chat_id, money, user_case):
    chat_id_save = str(chat_id) + ".txt"
    filename = open(chat_id_save, "w")
    filename.write(str(money) + "\n")
    filename.write(str(user_case))
    for k in range(len(ship_list)):
        filename.write("\n" + ship_list[k - 1])
    filename.close()


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    try:
        branch = save_tree_choice[chat_id]['branch']
        leaf = save_tree_choice[chat_id]['leaf']
    except KeyError:
        branch = '0'
        leaf = '0'

    # try:
    #     branch = save_leaf_choice[chat_id]['branch']
    #     leaf = save_leaf_choice[chat_id]['leaf']
    # except KeyError:
    #     branch = '0'
    #     leaf = '0'

    chat_id_save = str(chat_id) + ".txt"

    try:
        filename = open(chat_id_save, "r")
        file_cont = filename.readlines()
        lines = len(filename.readlines())
        money = int(re.sub(r"\n", "", file_cont[0]))
        user_case = int(re.sub(r"\n", "", file_cont[1]))
        for j in range(len(file_cont) - 2):
            ship_list.append(re.sub(r"\n", "", file_cont[j + 2]))
        filename.close()
    except FileNotFoundError:
        bot.sendMessage(chat_id, 'WELCOME TO STARWALKERS!')
        time.sleep(0.8)
        bot.sendMessage(chat_id, 'Version: 0.2')
        time.sleep(0.8)
        bot.sendMessage(chat_id, 'Create save...')
        filename = open(chat_id_save, "w")
        filename.write("30\n")
        filename.write("0")
        filename.close()
        bot.sendMessage(chat_id, 'Save created')

        filename = open(chat_id_save, "r")
        file_cont = filename.readlines()
        lines = len(filename.readlines())
        money = int(re.sub(r"\n", "", file_cont[0]))
        user_case = int(re.sub(r"\n", "", file_cont[1]))
        for j in range(len(file_cont) - 2):
            ship_list.append(re.sub(r"\n", "", file_cont[j + 2]))
        filename.close()
        print("Registered:", chat_id)

        bot.sendMessage(chat_id, 'Try /help to see rules, how to play and all functions')

    if command == '/restart':
        try:
            del save_tree_choice[chat_id]
        except:
            pass
        money = 30
        user_case = 0
        save(chat_id, money, user_case)
        bot.sendMessage(chat_id, "Party restarted, you have 30$ and 0 case")
    elif command == '/case_menu':
        try:
            del save_tree_choice[chat_id]
        except:
            pass
        print('case_menu')
        bot.sendMessage(chat_id, "What do you want to do with cases?\n1. Buy\n2. Open\n3. Close")
        branch = 1
        leaf = 0
        tree_choice(chat_id, branch, leaf)
    else:
        if branch != 0 and leaf == 0:
            print(branch)
            print(leaf)
            branch_to_leaf(chat_id, command, chat_id_save, branch, leaf, money, user_case)
        elif branch != 0 and leaf != 0:
            print(branch)
            print(leaf)
            leaf_output(chat_id, command, chat_id_save, branch, leaf, money, user_case)


def tree_choice(chat_id, branch, leaf):
    save_tree_choice[chat_id] = {'branch': branch, 'leaf': leaf}


# def leaf_choice(chat_id, branch, leaf):
#     save_leaf_choice[chat_id] = {'branch': branch, 'leaf': leaf}


def branch_to_leaf(chat_id, command, chat_id_save, branch, leaf, money, user_case):
    if branch == 1:  # Case menu
        if command.isdigit():
            if command == '1':  # Buy case
                bot.sendMessage(chat_id, f"Money: {money}$ | Case(s): {user_case}\nBuy how many cases ? (10$ per case)")
                leaf = 1
                del save_tree_choice[chat_id]
                tree_choice(chat_id, branch, leaf)
            elif command == '2':  # Open case
                bot.sendMessage(chat_id, f"Money: {money}$ | Case(s): {user_case}\nOpen how many cases")
                leaf = 2
                del save_tree_choice[chat_id]
                tree_choice(chat_id, branch, leaf)
            elif command == '3':  # Close case menu
                bot.sendMessage(chat_id, "How many sell")
                del save_tree_choice[chat_id]
        else:
            bot.sendMessage(chat_id, "What do you want to do with cases?\n1. Buy\n2. Open\n3. Close")


def leaf_output(chat_id, command, chat_id_save, branch, leaf, money, user_case):
    if branch == 1 and leaf == 1:
        if command.isdigit():
            number = int(command)
            if money >= 10 * number:
                money -= 10 * number
                user_case += number
                bot.sendMessage(chat_id, f"Money: {money}$ | Case(s): {user_case}\nThanks for buying {number} cases.")
                save(chat_id, money, user_case)
                del save_tree_choice[chat_id]
            else:
                bot.sendMessage(chat_id, "Not enough money, bro.")
        else:
            bot.sendMessage(chat_id, "Please use number")
    elif branch == 1 and leaf == 2:
        if command.isdigit():
            number = int(command)
            if user_case >= 1 and len(ship_list) < 10:
                user_case -= 1
                gotter = roll()
                ship_list.append(gotter)
                gotter_letter, gotter_int = gotter.split("-")
                cost = (got_let_int(gotter_letter) * int(gotter_int)) // 1000
                print("You got:", gotter + "! It costs: " + str(cost) + ", and its rank: " + get_d_sym(cost) + "!")
                save()
                input_enter = input("Press ENTER to continue... ")
            elif len(ship_list) == 10:
                clear()
                print("You have too many ships. Sell one and you can open cases again.")
                input_enter = input("Press ENTER to continue... ")
        else:
            bot.sendMessage(chat_id, "Please use number")





bot = telepot.Bot(secrets['token'])
MessageLoop(bot, {'chat': handle}).run_as_thread()
print('StarWalkers_telegrambot online')
bot.sendMessage(chat_id_owner, 'StarWalkers_telegrambot online')

while True:
    pass
