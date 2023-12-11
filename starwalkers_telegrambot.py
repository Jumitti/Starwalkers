import json
import os
import random
import re
import time

import telepot
from telepot.loop import MessageLoop

# import termcolor
# from termcolor import colored, cprint
from func import roll, got_let_int, get_int_ship, get_d_sym, get_cost

script_directory = os.path.dirname(os.path.abspath(__file__))
secrets_path = os.path.join(script_directory, 'SECRETS.json')
with open(secrets_path, 'r') as secrets_file:
    secrets = json.load(secrets_file)

chat_id_owner = secrets['id_owner']

save_tree_choice = {}
save_leaf_choice = {}
case_menu_list = ['/buy_case', '/open_case']


def save(chat_id, money, user_case, ship_list):
    chat_id_save = str(chat_id) + ".txt"
    filename = open(f"./user/{chat_id_save}", "w")
    filename.write(str(money) + "\n")
    filename.write(str(user_case) + "\n")
    for k in range(len(ship_list)):
        filename.write(ship_list[k] + "\n")
    filename.close()


def save_fight(chat_id, enemy_list):
    chat_id_save = str(chat_id) + "_fight.txt"
    filename_fight = open(f"./user/{chat_id_save}", "w")
    for k in range(len(enemy_list)):
        filename_fight.write(enemy_list[k] + '\n')
    filename_fight.close()


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    try:
        branch = save_tree_choice[chat_id]['branch']
        leaf = save_tree_choice[chat_id]['leaf']
    except KeyError:
        branch = '0'
        leaf = '0'

    chat_id_save = str(chat_id) + ".txt"
    chat_id_fight_save = str(chat_id) + "_fight.txt"

    try:
        ship_list = []
        enemy_list = []
        filename = open(f"./user/{chat_id_save}", "r")
        file_cont = filename.readlines()
        lines = len(filename.readlines())
        money = int(re.sub(r"\n", "", file_cont[0]))
        user_case = int(re.sub(r"\n", "", file_cont[1]))
        for j in range(len(file_cont) - 2):
            ship_list.append(re.sub(r"\n", "", file_cont[j + 2]))
        filename.close()

        filename_fight = open(f"./user/{chat_id_fight_save}", "r")
        file_cont_fight = filename_fight.readlines()
        for j in range(len(file_cont_fight)):
            enemy_list.append(re.sub(r"\n", "", file_cont_fight[j]))
        filename_fight.close()

    except FileNotFoundError:
        bot.sendMessage(chat_id, 'WELCOME TO STARWALKERS!')
        time.sleep(0.8)
        bot.sendMessage(chat_id, 'Version: 0.2')
        time.sleep(0.8)
        bot.sendMessage(chat_id, 'Create save...')
        filename = open(f"./user/{chat_id_save}", "w")
        filename.write("30\n")
        filename.write("0\n")
        filename.write("")
        filename.close()

        filename_fight = open(f"./user/{chat_id_fight_save}", "w")
        filename_fight.close()
        bot.sendMessage(chat_id, 'Save created')

        filename = open(f"./user/{chat_id_save}", "r")
        file_cont = filename.readlines()
        lines = len(filename.readlines())
        money = int(re.sub(r"\n", "", file_cont[0]))
        user_case = int(re.sub(r"\n", "", file_cont[1]))
        for j in range(len(file_cont) - 2):
            ship_list.append(re.sub(r"\n", "", file_cont[j + 2]))
        filename.close()

        filename_fight = open(f"./user/{chat_id_fight_save}", "r")
        file_cont_fight = filename_fight.readlines()
        for j in range(len(file_cont_fight)):
            enemy_list.append(re.sub(r"\n", "", file_cont_fight[j]))
        filename_fight.close()

        # print("Registered:", chat_id)
        bot.sendMessage(chat_id,
                        f"Money: {money}$ | Case(s): {user_case}\n\nMenu:\n1. /case_menu\n2. /collection\n3. /fight\n4. /help")
        bot.sendMessage(chat_id, 'Try /help to see rules, how to play and all functions')

    if command == '/restart':
        try:
            del save_tree_choice[chat_id]
        except KeyError:
            pass
        money = 30
        user_case = 0
        ship_list = []
        enemy_list = []
        save(chat_id, money, user_case, ship_list)
        save_fight(chat_id, enemy_list)
        bot.sendMessage(chat_id, "Party restarted, you have 30$, 0 case, no ship and no enemy")

    elif command == '/case_menu':
        try:
            del save_tree_choice[chat_id]
        except KeyError:
            pass
        bot.sendMessage(chat_id, "What do you want to do with cases?\n1. /buy_case\n2. /open_case\n")
        branch = 1
        leaf = 0
        tree_choice(chat_id, branch, leaf)

    elif command in case_menu_list:
        try:
            del save_tree_choice[chat_id]
        except KeyError:
            pass
        branch = 1
        leaf = 0
        tree_choice(chat_id, branch, leaf)
        branch_to_leaf(chat_id, command, chat_id_save, branch, leaf, money, user_case, ship_list)

    elif command == '/collection':
        try:
            del save_tree_choice[chat_id]
        except KeyError:
            pass
        display_ship_list = ""
        for zzz in range(len(ship_list)):
            time.sleep(0.1)
            display_ship_list += f'{str(zzz + 1)}) {str(ship_list[zzz])} {get_d_sym(get_cost(ship_list[zzz]))}\n'
        bot.sendMessage(chat_id, f"Your collection of ships:\n{display_ship_list}"
                                 f"\nEarn ships by /buy_case and /open_case"
                                 f"\nEarn money by /sell_ship and /fight")

    elif command == '/sell_ship':
        try:
            del save_tree_choice[chat_id]
        except KeyError:
            pass
        branch = 2
        leaf = 0
        tree_choice(chat_id, branch, leaf)
        branch_to_leaf(chat_id, command, chat_id_save, branch, leaf, money, user_case, ship_list)

    elif command == '/fight':
        try:
            del save_tree_choice[chat_id]
        except KeyError:
            pass
        branch = 3
        leaf = 0
        tree_choice(chat_id, branch, leaf)
        branch_to_leaf(chat_id, command, chat_id_save, branch, leaf, money, user_case, ship_list)

    elif command == '/exit':
        try:
            del save_tree_choice[chat_id]
        except KeyError:
            pass
        bot.sendMessage(chat_id,
                        f"Money: {money}$ | Case(s): {user_case}\n\nMenu:\n1. /case_menu\n2. /collection\n3. /fight\n4. /help")

    elif command == '/godmode':
        try:
            del save_tree_choice[chat_id]
        except KeyError:
            pass
        money = 1000000
        user_case = 1000000
        ship_list = []
        save(chat_id, money, user_case, ship_list)
        bot.sendMessage(chat_id, "God mode activated, you have 1000000$, 1000000 cases but no ship")

    elif command == '/help':
        try:
            del save_tree_choice[chat_id]
        except KeyError:
            pass
        bot.sendMessage(chat_id,
                        'WELCOME TO STARWALKERS!\nVersion: 0.2\n\n'
                        "Starwalkers is a seemingly simple game where mistakes can cost you dearly. Start your adventure with $30 and buy your first ships. It's time to fight! Can you be the winner?\n\n"

                        "Expand your fleet with /case_menu:\n"
                        "  • /buy_case allows you to buy $10 cases containing a random ship\n"
                        "  • /open_case allows you to open the crates\n\n"

                        "Organize your fleet with /collection:\n"
                        "   • /collection allows you to keep an eye on your ships and their statistics\n"
                        "   • /sell_ship allows you to sell a ship\n"
                        'The boats are named "Q-9191" where Q can be any letters from A to Z and 9191 a number between 0000 and 9999.\n'
                        "Cost and rank depend on letter and number. The higher the letter (example: A) and/or the number (example: 9999), the higher the cost and rank. The rank has a visual way of interpretation: $ to $$$$$.\n"
                        "Be careful, during combat it is the rank that counts and not the visual way of representing it.\n\n"

                        "Go to war with /fight:\n"
                        "You will fight randomly from 1 to 3 enemy boats. You can't choose your opponent so choose your boat wisely to fight.\n"
                        "Intuitively, the higher your ship's rank, the more likely it is to win. For example if your ship is A-9999 and it is fighting against Z-0000. You will win because your rank is higher than that of your opponent.\n"
                        "Be careful, during combat it is the rank that counts and not the visual way of representing it.\n"
                        "Ships take damage during combat and lose ranks\n\n"

                        "Some tips:\n"
                        "Don't worry about saving, it's automatic and individual. No one can mess with your game.\n"
                        "You can exit any actions at any time with /exit\n"
                        "No more money, no more cash, no more ship, in short, is it over? No, you can use /restart\n"
                        "Lost ? use /help to see all our commands and tips\n\n"
                        
                        "Credit:\n"
                        "Game by Gametoy20: https://github.com/Gametoy20\n"
                        'Telegram bot by Jumitti: https://github.com/Jumitti')

    else:
        if branch != 0 and leaf == 0:
            branch_to_leaf(chat_id, command, chat_id_save, branch, leaf, money, user_case, ship_list)

        elif branch != 0 and leaf != 0:
            leaf_output(chat_id, command, chat_id_save, branch, leaf, money, user_case, ship_list, enemy_list)


def tree_choice(chat_id, branch, leaf):
    save_tree_choice[chat_id] = {'branch': branch, 'leaf': leaf}


def branch_to_leaf(chat_id, command, chat_id_save, branch, leaf, money, user_case, ship_list):
    if branch == 1:  # Case menu
        if command.isdigit() or command in case_menu_list:
            if command == '1' or command == '/buy_case':  # Buy case
                bot.sendMessage(chat_id, f"Money: {money}$ | Case(s): {user_case}\nBuy how many cases ? (10$ per case)")
                leaf = 1
                del save_tree_choice[chat_id]
                tree_choice(chat_id, branch, leaf)

            elif command == '2' or command == '/open_case':  # Open case
                bot.sendMessage(chat_id, f"Money: {money}$ | Case(s): {user_case}\nOpen how many cases ?")
                leaf = 2
                del save_tree_choice[chat_id]
                tree_choice(chat_id, branch, leaf)
        else:
            bot.sendMessage(chat_id, "What do you want to do with cases?\n1. /buy_case\n2. /open_case")

    elif branch == 2:  # Collection and selling
        display_ship_list = ""
        for zzz in range(len(ship_list)):
            time.sleep(0.1)
            display_ship_list += f'{str(zzz + 1)}) {str(ship_list[zzz])} {get_d_sym(get_cost(ship_list[zzz]))}\n'
        bot.sendMessage(chat_id,
                        f"Your collection of ships:\n{display_ship_list}\nSell by input the number of the ship")
        leaf = 1
        del save_tree_choice[chat_id]
        tree_choice(chat_id, branch, leaf)

    elif branch == 3:  # Fight
        enemy_list = []
        enemy_rand = random.randint(1, 3)
        for en_i in range(enemy_rand):
            roll_en = roll()
            enemy_list.append(roll_en)
        save_fight(chat_id, enemy_list)
        if len(enemy_list) != 0 and len(ship_list) != 0:
            bot.sendMessage(chat_id, "Your enemies:")
            for en_i1 in range(len(enemy_list)):
                bot.sendMessage(chat_id, str(en_i1 + 1) + ". " + enemy_list[en_i1])
                time.sleep(0.8)
            save_fight(chat_id, enemy_list)
            bot.sendMessage(chat_id,
                            f"You will be fighting with: {str(enemy_list[0])} {str(get_d_sym(get_cost(str(enemy_list[0]))))}")
            display_ship_list = ""
            for i_non in range(len(ship_list)):
                display_ship_list += f"{str(i_non + 1)}) {ship_list[i_non]} {str(get_d_sym(get_cost(ship_list[i_non])))}\n"
            bot.sendMessage(chat_id,
                            f'Choose your ship to attack:\n{display_ship_list}\n/exit or 0 to leave the battlefield')

            leaf = 1
            del save_tree_choice[chat_id]
            tree_choice(chat_id, branch, leaf)
        else:
            bot.sendMessage(chat_id,
                            f"You don't have ships.\n/buy_case and /open_case to get ships")


def leaf_output(chat_id, command, chat_id_save, branch, leaf, money, user_case, ship_list, enemy_list):
    if branch == 1 and leaf == 1:  # Buy case
        if command.isdigit():
            number = int(command)
            if money >= 10 * number:
                money -= 10 * number
                user_case += number
                bot.sendMessage(chat_id,
                                f"Money: {money}$ | Case(s): {user_case}\nThanks for buying {number} cases.\n\n/open_case to earn ship\n/exit buying case.")
                save(chat_id, money, user_case, ship_list)
            else:
                bot.sendMessage(chat_id, "Not enough money, bro. Try to /sell_ship or /fight\n\n/exit buying case.")
        else:
            bot.sendMessage(chat_id, "Please use number or /exit")

    elif branch == 1 and leaf == 2:  # Open case
        if command.isdigit():
            number = int(command)
            if user_case >= 1 and len(ship_list) < 10:
                if number + len(ship_list) > 10:
                    number = 10 - len(ship_list)
                    bot.sendMessage(chat_id, f"Only 10 ships is allowed. {number} case(s) will be opened.")

                for i in range(1, number + 1):
                    user_case -= 1
                    gotter = roll()
                    ship_list.append(gotter)
                    gotter_letter, gotter_int = gotter.split("-")
                    cost = (got_let_int(gotter_letter) * int(gotter_int)) // 1000
                    bot.sendMessage(chat_id,
                                    f"You got: {gotter} ! It costs: {str(cost)}$ and its rank: {get_d_sym(cost)} !")
                    save(chat_id, money, user_case, ship_list)

                bot.sendMessage(chat_id,
                                f"Money: {money}$ | Case(s): {user_case}\nThanks for buying {number} ship(s)."
                                f"\n\nSee your ship(s) in /collection"
                                f"\n\n Earn money by /sell_fight or /fight"
                                f"\n\n/exit opening case.")

            elif len(ship_list) == 10:
                bot.sendMessage(chat_id,
                                "You have too many ships. /sell_ship and you can open cases again.\n\n/exit opening case.")
            elif user_case == 0:
                bot.sendMessage(chat_id,
                                "You don't have case. /buy_case\n\n/exit opening case.")
        else:
            bot.sendMessage(chat_id, "Please use number or /exit")

    elif branch == 2 and leaf == 1:  # Selling ship
        if command.isdigit():
            number = int(command)
            try:
                s_cost = get_cost(ship_list[number - 1]) // 2
                s_name = ship_list[number - 1]
                ship_list.pop(number - 1)
                money += s_cost
                save(chat_id, money, user_case, ship_list)
                bot.sendMessage(chat_id,
                                f"Money: {money}$ | Case(s): {user_case}\nYour ship {str(s_name)} was sold and you got {str(s_cost)}$ !")
                display_ship_list = ""
                for zzz in range(len(ship_list)):
                    time.sleep(0.1)
                    display_ship_list += f'{str(zzz + 1)}) {str(ship_list[zzz])} {get_d_sym(get_cost(ship_list[zzz]))}\n'
                bot.sendMessage(chat_id,
                                f'Choose your ship to sell:\n{display_ship_list}\n/exit selling ship.')
            except KeyError:
                bot.sendMessage(chat_id, "Ship not found.\n\n/exit selling ship.")
        else:
            bot.sendMessage(chat_id, "Please use number or /exit")

    elif branch == 3 and leaf == 1:  # FIGHT !
        if command.isdigit():
            print(f"Enemy fight {enemy_list}")
            user_input = int(command)
            player_cost = 0
            enemy_cost = 0
            if len(ship_list) >= user_input > 0:
                player_ship = ship_list[user_input - 1]
                player_let, player_int = player_ship.split("-")
                ship_list.pop(user_input - 1)
                player_cost = get_cost(player_ship)

                enemy_ship = enemy_list[0]
                enemy_cost = get_cost(enemy_ship)
            elif user_input == 0:
                bot.sendMessage(chat_id, "You left the battlefield.")
                try:
                    del save_tree_choice[chat_id]
                except KeyError:
                    pass
                enemy_list = []
                save_fight(chat_id, enemy_list)
                bot.sendMessage(chat_id,
                                f"Money: {money}$ | Case(s): {user_case}\n\nMenu:\n1. /case_menu\n2. /collection\n3. /fight\n4. /help")

            else:
                bot.sendMessage(chat_id, "You do not have ship with choosed number.")
            if player_cost != 0 and enemy_cost != 0:
                if player_cost > enemy_cost:
                    bot.sendMessage(chat_id, "You won and got: " + str(enemy_cost // 2) + "$ !")
                    damage = random.randint(0, 30)
                    time_player_int = int(player_int)
                    fin_player_int = time_player_int - damage
                    player_int = get_int_ship(fin_player_int)
                    new_ship = str(player_let) + str(player_int)
                    ship_list.append(new_ship)
                    bot.sendMessage(chat_id,
                                    "Your ship has taken " + str(damage) + " damage. Now it is " + str(new_ship) + ".")
                    money += enemy_cost // 2
                    enemy_list.pop(0)
                    save(chat_id, money, user_case, ship_list)
                    save_fight(chat_id, enemy_list)
                    try:
                        bot.sendMessage(chat_id,
                                        f"You will be fighting with: {str(enemy_list[0])} {str(get_d_sym(get_cost(str(enemy_list[0]))))}")

                        display_ship_list = ""
                        for zzz in range(len(ship_list)):
                            time.sleep(0.1)
                            display_ship_list += f'{str(zzz + 1)}) {str(ship_list[zzz])} {get_d_sym(get_cost(ship_list[zzz]))}\n'
                        bot.sendMessage(chat_id,
                                        f'Choose your ship to attack:\n{display_ship_list}\n/exit to leave the battlefield')
                    except IndexError:
                        bot.sendMessage(chat_id, f"Battle is finished ! Congratulation !")
                        try:
                            del save_tree_choice[chat_id]
                        except KeyError:
                            pass
                        bot.sendMessage(chat_id,
                                        f"Money: {money}$ | Case(s): {user_case}\n\nMenu:\n1. /case_menu\n2. /collection\n3. /fight\n4. /help")

                else:
                    bot.sendMessage(chat_id, "You've lost your ship! Be careful next time!")
                    save(chat_id, money, user_case, ship_list)
                    save_fight(chat_id, enemy_list)
                    if len(ship_list) == 0:
                        bot.sendMessage(chat_id, "Battle is finished. You loose all your ships.")
                        try:
                            del save_tree_choice[chat_id]
                        except KeyError:
                            pass
                        bot.sendMessage(chat_id,
                                        f"Money: {money}$ | Case(s): {user_case}\n\nMenu:\n1. /case_menu\n2. /collection\n3. /fight\n4. /help")

                    else:
                        display_ship_list = ""
                        for zzz in range(len(ship_list)):
                            time.sleep(0.1)
                            display_ship_list += f'{str(zzz + 1)}) {str(ship_list[zzz])} {get_d_sym(get_cost(ship_list[zzz]))}\n'
                        bot.sendMessage(chat_id,
                                        f'Choose your ship to attack:\n{display_ship_list}\n/exit to leave the battlefield')
        else:
            bot.sendMessage(chat_id, "Please use number.")


# Initializing bot
bot = telepot.Bot(secrets['token'])
MessageLoop(bot, {'chat': handle}).run_as_thread()
print('StarWalkers_telegrambot online')
bot.sendMessage(chat_id_owner, 'StarWalkers_telegrambot online')

while True:
    pass
