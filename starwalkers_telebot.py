import json
import os
import random
import re
import time

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# import termcolor
# from termcolor import colored, cprint
import keyboard as KB
from func import roll, got_let_int, get_int_ship, get_d_sym, get_cost

script_directory = os.path.dirname(os.path.abspath(__file__))
secrets_path = os.path.join(script_directory, 'SECRETS.json')
with open(secrets_path, 'r') as secrets_file:
    secrets = json.load(secrets_file)

chat_id_owner = secrets['id_owner']

save_tree_choice = {}
case_menu_list = ['/buy_case', '💸 Buy case', '/open_case', '🎁 Open case']


def settings_file():
    settings_path = os.path.join(script_directory, 'settings.json')
    with open(settings_path, 'r') as settings_files:
        settings = json.load(settings_files)

        return settings


def save_json(chat_id, username=None, money=None, user_case=None, ship_list=None, enemy_list=None):
    try:
        with open(f"user/{chat_id}.json", "r") as read_file:
            ID_info = json.load(read_file)
    except FileNotFoundError:
        ID_info = {}

    ID_info["ID_player"] = chat_id
    if username is not None:
        ID_info["username"] = username
    if money is not None:
        ID_info["money"] = money
    if user_case is not None:
        ID_info["user_case"] = user_case
    if ship_list is not None:
        ID_info["ship_list"] = ship_list
    if enemy_list is not None:
        ID_info["enemy_list"] = enemy_list

    with open(f"user/{chat_id}.json", "w") as save_file:
        json.dump(ID_info, save_file, indent=2)


def load_json(chat_id):
    with open(f"user/{chat_id}.json", "r") as save_file:
        ID_info = json.load(save_file)
    return ID_info


def list_users():
    id_players = []
    for filename in os.listdir('user/'):
        if filename.endswith('.json'):
            with open(os.path.join('user/', filename)) as file:
                data = json.load(file)
                id_player = data.get('ID_player')
                if id_player is not None:
                    id_players.append(id_player)
    return id_players


def tree_choice(chat_id, branch=None, leaf=None):
    try:
        del save_tree_choice[chat_id]
    except KeyError:
        pass
    if branch is None:
        branch = 0
    if leaf is None:
        leaf = 0
    save_tree_choice[chat_id] = {'branch': branch, 'leaf': leaf}

    branch = save_tree_choice[chat_id]['branch']
    leaf = save_tree_choice[chat_id]['leaf']

    return branch, leaf


def handle(msg):
    settings = settings_file()

    chat_id = msg['chat']['id']
    command = msg['text']

    try:
        branch = save_tree_choice[chat_id]['branch']
        leaf = save_tree_choice[chat_id]['leaf']
    except KeyError:
        branch, leaf = tree_choice(chat_id)

    try:
        ID_info = load_json(chat_id)
        money = ID_info['money']
        user_case = ID_info['user_case']
        ship_list = ID_info['ship_list']
        enemy_list = ID_info['enemy_list']

    except FileNotFoundError:
        bot.sendMessage(chat_id, 'WELCOME TO STARWALKERS!')
        time.sleep(0.8)
        bot.sendMessage(chat_id, f'Version: {settings["version"]}')
        time.sleep(0.8)
        bot.sendMessage(chat_id, 'Create save...')
        save_json(chat_id, money=settings['starting_money'], user_case=0, ship_list=[], enemy_list=[])
        ID_info = load_json(chat_id)
        money = ID_info['money']
        user_case = ID_info['user_case']
        ship_list = ID_info['ship_list']
        enemy_list = ID_info['enemy_list']
        branch, leaf = tree_choice(chat_id, 4, 0)

    if branch == 4 and leaf == 0:
        branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list)

    elif command == '/all_user':
        if chat_id == chat_id_owner:
            ID_players = list_users()
            bot.sendMessage(chat_id_owner, ID_players)

    elif command == '/command_bot':
        if chat_id == chat_id_owner:
            bot.sendMessage(chat_id_owner,
                            "/case_menu - Buy/open cases\n"
                            "/buy_case - Buy cases (10$ per case)\n"
                            "/open_case - Open cases\n"
                            "/collection - List of your ships\n"
                            "/sell_ship - Sell ship. Earn money\n"
                            "/fight - Enter on the battlefield\n"
                            "/exit - Leave any actions\n"
                            "/restart - Ne beef ? Restart the game\n"
                            "/help - A little reminder", reply_markup=KB.main_keyboard())

    elif command in ['/restart', '🔄️ Restart']:
        tree_choice(chat_id)
        money = settings['starting_money']
        user_case = 0
        ship_list = []
        enemy_list = []
        save_json(chat_id, money=settings['starting_money'], user_case=0, ship_list=[], enemy_list=[])
        bot.sendMessage(chat_id,
                        f"Party restarted, you have {settings['starting_money']}$, 0 case, no ship and no enemy", reply_markup=KB.main_keyboard())

    elif command in ['/case_menu', '🏪 Case Menu']:
        bot.sendMessage(chat_id, "What do you want to do with cases?\n1. /buy_case\n2. /open_case\n", reply_markup=KB.main_keyboard())
        tree_choice(chat_id, 1, 0)

    elif command in case_menu_list:
        branch, leaf = tree_choice(chat_id, 1, 0)
        branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list)

    elif command in ['/collection', '🚀 Collection/Fleet']:
        tree_choice(chat_id)
        display_ship_list = ""
        for zzz in range(len(ship_list)):
            time.sleep(0.1)
            display_ship_list += f'{str(zzz + 1)}) {str(ship_list[zzz])} {get_d_sym(get_cost(ship_list[zzz]))}\n'
        bot.sendMessage(chat_id, f"Your collection of ships:\n{display_ship_list}"
                                 f"\nEarn ships by /buy_case and /open_case"
                                 f"\nEarn money by /sell_ship and /fight", reply_markup=KB.main_keyboard())

    elif command in ['/sell_ship', '🫱🏽‍🫲🏽 Sell ship']:
        branch, leaf = tree_choice(chat_id, 2, 0)
        branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list)

    elif command in ['/fight', '💥 Fight !']:
        branch, leaf = tree_choice(chat_id, 3, 0)
        branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list)

    elif command in ['/exit', '⏪ Exit']:
        tree_choice(chat_id)
        bot.sendMessage(chat_id,
                        f"Money: {money}$ | Case(s): {user_case}\n\nMenu:\n1. /case_menu\n2. /collection\n3. /fight\n4. /help",
                        reply_markup=KB.main_keyboard())

    elif command == '/godmode':
        tree_choice(chat_id)
        money = 1000000
        user_case = 1000000
        ship_list = []
        save_json(chat_id, money=1000000, user_case=1000000, ship_list=[], enemy_list=[])
        bot.sendMessage(chat_id, "God mode activated, you have 1000000$, 1000000 cases but no ship", reply_markup=KB.main_keyboard())

    elif command in ['/help', '❔ Help']:
        tree_choice(chat_id)
        bot.sendMessage(chat_id,
                        f'WELCOME TO STARWALKERS!\nVersion: {settings["version"]}\n\n'
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
                        "   • Don't worry about saving, it's automatic and individual. No one can mess with your game.\n"
                        "   • You can exit any actions at any time with /exit\n"
                        "   • No more money, no more cash, no more ship, in short, is it over? No, you can use /restart\n"
                        "   • Lost ? use /help to see all our commands and tips\n\n"

                        "Credit:\n"
                        "GitHub: https://github.com/Jumitti/starwalkers_telegrambot\n"
                        "Game by Gametoy20: https://github.com/Gametoy20\n"
                        'Telegram bot by Jumitti: https://github.com/Jumitti', reply_markup=KB.main_keyboard())

    else:
        if branch != 0 and leaf == 0:
            branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list)

        elif branch != 0 and leaf != 0:
            leaf_output(chat_id, command, branch, leaf, money, user_case, ship_list, enemy_list)


def branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list):
    settings = settings_file()
    if branch == 1:  # Case menu
        if command.isdigit() or command in case_menu_list:
            if command in ['1', '/buy_case', '💸 Buy case']:  # Buy case
                bot.sendMessage(chat_id,
                                f"Money: {money}$ | Case(s): {user_case}\nBuy how many cases ? ({settings['cost_case']}$ per case)",
                                reply_markup=KB.main_keyboard())
                tree_choice(chat_id, branch, 1)

            elif command in ['2', '/open_case', '🎁 Open case']:  # Open case
                bot.sendMessage(chat_id, f"Money: {money}$ | Case(s): {user_case}\nOpen how many cases ?",
                                reply_markup=KB.main_keyboard())
                tree_choice(chat_id, branch, 2)
        else:
            bot.sendMessage(chat_id, "What do you want to do with cases?\n1. /buy_case\n2. /open_case",
                            reply_markup=KB.main_keyboard())

    elif branch == 2:  # Collection and selling
        display_ship_list = ""
        for zzz in range(len(ship_list)):
            time.sleep(0.1)
            display_ship_list += f'{str(zzz + 1)}) {str(ship_list[zzz])} {get_d_sym(get_cost(ship_list[zzz]))}\n'
        bot.sendMessage(chat_id,
                        f"Your collection of ships:\n{display_ship_list}\nSell by input the number of the ship",
                        reply_markup=KB.main_keyboard())
        tree_choice(chat_id, branch, 1)

    elif branch == 3:  # Fight
        enemy_list = []
        enemy_rand = random.randint(settings['min_enemy'], settings['max_enemy'])
        for en_i in range(enemy_rand):
            roll_en = roll()
            enemy_list.append(roll_en)
        save_json(chat_id, enemy_list=enemy_list)
        if len(enemy_list) != 0 and len(ship_list) != 0:
            bot.sendMessage(chat_id, "Your enemies:")
            for en_i1 in range(len(enemy_list)):
                bot.sendMessage(chat_id, str(en_i1 + 1) + ". " + enemy_list[en_i1])
                time.sleep(0.8)
            save_json(chat_id, enemy_list=enemy_list)
            bot.sendMessage(chat_id,
                            f"You will be fighting with: {str(enemy_list[0])} {str(get_d_sym(get_cost(str(enemy_list[0]))))}")
            display_ship_list = ""
            for i_non in range(len(ship_list)):
                display_ship_list += f"{str(i_non + 1)}) {ship_list[i_non]} {str(get_d_sym(get_cost(ship_list[i_non])))}\n"
            bot.sendMessage(chat_id,
                            f'Choose your ship to attack:\n{display_ship_list}\n/exit or 0 to leave the battlefield',
                            reply_markup=KB.main_keyboard())
            tree_choice(chat_id, branch, 1)
        else:
            bot.sendMessage(chat_id,
                            f"You don't have ships.\n/buy_case and /open_case to get ships", reply_markup=KB.main_keyboard())

    elif branch == 4:
        bot.sendMessage(chat_id,
                        f"What is you nickname ?", reply_markup=KB.main_keyboard())
        tree_choice(chat_id, branch, 1)


def leaf_output(chat_id, command, branch, leaf, money, user_case, ship_list, enemy_list):
    settings = settings_file()
    if branch == 1 and leaf == 1:  # Buy case
        if command.isdigit():
            number = int(command)
            if money >= settings['cost_case'] * number:
                money -= settings['cost_case'] * number
                user_case += number
                bot.sendMessage(chat_id,
                                f"Money: {money}$ | Case(s): {user_case}\nThanks for buying {number} cases.\n\n/open_case to earn ship\n/exit buying case.",
                                reply_markup=KB.main_keyboard())
                save_json(chat_id, money=money, user_case=user_case)
            else:
                bot.sendMessage(chat_id, "Not enough money, bro. Try to /sell_ship or /fight\n\n/exit buying case.",
                                reply_markup=KB.main_keyboard())
        else:
            bot.sendMessage(chat_id, "Please use number or /exit", reply_markup=KB.main_keyboard())

    elif branch == 1 and leaf == 2:  # Open case
        if command.isdigit():
            number = int(command)
            if user_case >= 1 and len(ship_list) < settings['ship_fleet']:
                if number + len(ship_list) > settings['ship_fleet']:
                    if number > user_case:
                        number = user_case
                        bot.sendMessage(chat_id,
                                        f"Only {number} case(s) will be opened.", reply_markup=KB.main_keyboard())
                    else:
                        number = settings['ship_fleet'] - len(ship_list)
                        bot.sendMessage(chat_id,
                                        f"Only {settings['ship_fleet']} ships is allowed. {number} case(s) will be opened.",
                                        reply_markup=KB.main_keyboard())

                for i in range(0, number):
                    user_case -= 1
                    gotter = roll()
                    ship_list.append(gotter)
                    gotter_letter, gotter_int = gotter.split("-")
                    cost = (got_let_int(gotter_letter) * int(gotter_int)) // 1000
                    bot.sendMessage(chat_id,
                                    f"You got: {gotter} ! It costs: {str(cost)}$ and its rank: {get_d_sym(cost)} !")
                    save_json(chat_id, user_case=user_case, ship_list=ship_list)

                bot.sendMessage(chat_id,
                                f"Money: {money}$ | Case(s): {user_case}\nThanks for buying {number} ship(s)."
                                f"\n\nSee your ship(s) in /collection"
                                f"\n\n Earn money by /sell_ship or /fight"
                                f"\n\n/exit opening case.", reply_markup=KB.main_keyboard())

            elif len(ship_list) == settings['ship_fleet']:
                bot.sendMessage(chat_id,
                                "You have too many ships. /sell_ship and you can open cases again.\n\n/exit opening case.",
                                reply_markup=KB.main_keyboard())
            elif user_case <= 0:
                bot.sendMessage(chat_id,
                                "You don't have case. /buy_case\n\n/exit opening case.", reply_markup=KB.main_keyboard())
        else:
            bot.sendMessage(chat_id, "Please use number or /exit", reply_markup=KB.main_keyboard())

    elif branch == 2 and leaf == 1:  # Selling ship
        if command.isdigit():
            number = int(command)
            try:
                s_cost = get_cost(ship_list[number - 1]) // 2
                s_name = ship_list[number - 1]
                ship_list.pop(number - 1)
                money += s_cost
                save_json(chat_id, money=money, ship_list=ship_list)
                bot.sendMessage(chat_id,
                                f"Money: {money}$ | Case(s): {user_case}\nYour ship {str(s_name)} was sold and you got {str(s_cost)}$ !")
                display_ship_list = ""
                for zzz in range(len(ship_list)):
                    time.sleep(0.1)
                    display_ship_list += f'{str(zzz + 1)}) {str(ship_list[zzz])} {get_d_sym(get_cost(ship_list[zzz]))}\n'
                bot.sendMessage(chat_id,
                                f'Choose your ship to sell:\n{display_ship_list}\n/exit selling ship.', reply_markup=KB.main_keyboard())
            except KeyError:
                bot.sendMessage(chat_id, "Ship not found.\n\n/exit selling ship.", reply_markup=KB.main_keyboard())
        else:
            bot.sendMessage(chat_id, "Please use number or /exit", reply_markup=KB.main_keyboard())

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
                save_json(chat_id, ship_list=ship_list, enemy_list=enemy_list)
                bot.sendMessage(chat_id,
                                f"Money: {money}$ | Case(s): {user_case}\n\nMenu:\n1. /case_menu\n2. /collection\n3. /fight\n4. /help",
                                reply_markup=KB.main_keyboard())

            else:
                bot.sendMessage(chat_id, "You do not have ship with choosed number.", reply_markup=KB.main_keyboard())
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
                    save_json(chat_id, money=money, ship_list=ship_list, enemy_list=enemy_list)
                    try:
                        bot.sendMessage(chat_id,
                                        f"You will be fighting with: {str(enemy_list[0])} {str(get_d_sym(get_cost(str(enemy_list[0]))))}")

                        display_ship_list = ""
                        for zzz in range(len(ship_list)):
                            time.sleep(0.1)
                            display_ship_list += f'{str(zzz + 1)}) {str(ship_list[zzz])} {get_d_sym(get_cost(ship_list[zzz]))}\n'
                        bot.sendMessage(chat_id,
                                        f'Choose your ship to attack:\n{display_ship_list}\n/exit to leave the battlefield',
                                        reply_markup=KB.main_keyboard())
                    except IndexError:
                        bot.sendMessage(chat_id, f"Battle is finished ! Congratulation !")
                        tree_choice(chat_id)
                        bot.sendMessage(chat_id,
                                        f"Money: {money}$ | Case(s): {user_case}\n\nMenu:\n1. /case_menu\n2. /collection\n3. /fight\n4. /help",
                                        reply_markup=KB.main_keyboard())

                else:
                    bot.sendMessage(chat_id, "You've lost your ship! Be careful next time!")
                    save_json(chat_id, money=money, ship_list=ship_list, enemy_list=enemy_list)
                    if len(ship_list) == 0:
                        bot.sendMessage(chat_id, "Battle is finished. You loose all your ships.")
                        tree_choice(chat_id)
                        bot.sendMessage(chat_id,
                                        f"Money: {money}$ | Case(s): {user_case}\n\nMenu:\n1. /case_menu\n2. /collection\n3. /fight\n4. /help",
                                        reply_markup=KB.main_keyboard())

                    else:
                        display_ship_list = ""
                        for zzz in range(len(ship_list)):
                            time.sleep(0.1)
                            display_ship_list += f'{str(zzz + 1)}) {str(ship_list[zzz])} {get_d_sym(get_cost(ship_list[zzz]))}\n'
                        bot.sendMessage(chat_id,
                                        f'Choose your ship to attack:\n{display_ship_list}\n/exit to leave the battlefield', reply_markup=KB.main_keyboard())
        else:
            bot.sendMessage(chat_id, "Please use number.")
    elif branch == 4 and leaf == 1:
        username = command
        save_json(chat_id, username=username)
        bot.sendMessage(chat_id, 'Save created')
        bot.sendMessage(chat_id,
                        f"Welcome on board Captain {username}\n\n"
                        f"Money: {money}$ | Case(s): {user_case}\n\nMenu:\n1. /case_menu\n2. /collection\n3. /fight\n4. /help")
        bot.sendMessage(chat_id, 'Try /help to see rules, how to play and all functions', reply_markup=KB.main_keyboard())


# Initializing bot
bot = telepot.Bot(secrets['token'])
MessageLoop(bot, {'chat': handle}).run_as_thread()
print('StarWalkers online')
bot.sendMessage(chat_id_owner, 'StarWalkers online')

while True:
    pass
