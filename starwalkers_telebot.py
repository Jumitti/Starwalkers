import json
import os
import random
import re
import time
import math

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
captain_menu_list = ['/see_captain', '👀 See', '/send_money', '💸 Send']


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


def db_id_username(chat_id, username):
    try:
        with open(f"user/db_id_username.json", "r") as read_file:
            ID_info = json.load(read_file)
    except FileNotFoundError:
        ID_info = {}

    ID_info[f"{chat_id}"] = username
    with open(f"user/db_id_username.json", "w") as save_file:
        json.dump(ID_info, save_file, indent=2)


def load_db_id_username():
    with open("user/db_id_username.json", "r") as file:
        data = json.load(file)
    return data


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


def tree_choice(chat_id, branch=None, leaf=None, contact_captain=None):
    try:
        del save_tree_choice[chat_id]
    except KeyError:
        pass
    if branch is None:
        branch = 0
    if leaf is None:
        leaf = 0
    if contact_captain is None:
        contact_captain = 0

    save_tree_choice[chat_id] = {'branch': branch, 'leaf': leaf, 'contact_captain': contact_captain}

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

    if 'username' in ID_info:
        username = ID_info['username']
    money = ID_info['money']
    user_case = ID_info['user_case']
    ship_list = ID_info['ship_list']
    enemy_list = ID_info['enemy_list']

    if branch == 4 and leaf == 0:
        branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list)

    elif command == '/all_user':
        if chat_id == chat_id_owner:
            data = load_db_id_username()
            message = "Users list:\n"
            for user_id, username in data.items():
                message += f"ID : {user_id}, Username : {username}\n"
            bot.sendMessage(chat_id, message)

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
        bot.sendMessage(chat_id, f"Welcome to your fleet Captain {username} !\n\n Your collection of ships:",
                        reply_markup=KB.ship_list_button(ship_list))
        bot.sendMessage(chat_id, f"\nEarn ships by /buy_case and /open_case"
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
    
    elif command in ['/captains_list', '🧑🏽‍🚀 Captains']:
        tree_choice(chat_id, branch=5)
        bot.sendMessage(chat_id,
                        f"Did you want to /see_captain or /send_money to captain ?",
                        reply_markup=KB.captains_keyboard())

    elif command in captain_menu_list:
        branch, leaf = tree_choice(chat_id, 5, 0)
        branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list)

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
            leaf_output(chat_id, username, command, branch, leaf, money, user_case, ship_list, enemy_list)


def branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list):
    settings = settings_file()
    if branch == 1:  # Case menu
        if command.isdigit() or command in case_menu_list:
            if command in ['1', '/buy_case', '💸 Buy case']:  # Buy case
                bot.sendMessage(chat_id,
                                f"Money: {money}$ | Case(s): {user_case}\nBuy how many cases ? ({settings['cost_case']}$ per case)",
                                reply_markup=KB.case_menu_keyboard())
                tree_choice(chat_id, branch, 1)

            elif command in ['2', '/open_case', '🎁 Open case']:  # Open case
                bot.sendMessage(chat_id, f"Money: {money}$ | Case(s): {user_case}\nOpen how many cases ?",
                                reply_markup=KB.case_menu_keyboard())
                tree_choice(chat_id, branch, 2)
        else:
            bot.sendMessage(chat_id, "What do you want to do with cases?\n1. /buy_case\n2. /open_case",
                            reply_markup=KB.main_keyboard())

    elif branch == 2:  # Collection and selling
        bot.sendMessage(chat_id,
                        f"Choose your ship to sell:", reply_markup=KB.sell_ship_button(ship_list))
        bot.sendMessage(chat_id,
                        f'/exit selling ship.', reply_markup=KB.main_keyboard())
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
            bot.sendMessage(chat_id,
                            f'Choose your ship to attack:', reply_markup=KB.ship_list_button(ship_list))
            bot.sendMessage(chat_id, '/exit to leave the battlefield', reply_markup=KB.main_keyboard())
            tree_choice(chat_id, branch, 1)
        else:
            bot.sendMessage(chat_id,
                            f"You don't have ships.\n/buy_case and /open_case to get ships", reply_markup=KB.main_keyboard())

    elif branch == 4:
        bot.sendMessage(chat_id,
                        f"What is you nickname ?", reply_markup=KB.main_keyboard())
        tree_choice(chat_id, branch, 1)

    elif branch == 5:
        captains = load_db_id_username()
        if command in ['/see_captain', '👀 See']:
            bot.sendMessage(chat_id, "Which captain do you want to see?", reply_markup=KB.captains_button(captains))
            tree_choice(chat_id, branch, 1)
        elif command in ['/send_money', '💸 Send']:
            bot.sendMessage(chat_id, "Which captain do you want to send money to?", reply_markup=KB.captains_button(captains))
            tree_choice(chat_id, branch, 2)


def on_callback_query(msg):
    settings = settings_file()
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    branch = save_tree_choice[chat_id]['branch']
    leaf = save_tree_choice[chat_id]['leaf']

    ID_info = load_json(chat_id)
    money = ID_info['money']
    user_case = ID_info['user_case']
    ship_list = ID_info['ship_list']
    enemy_list = ID_info['enemy_list']
    username = ID_info['username']

    if branch == 0 and leaf == 0:
        bot.answerCallbackQuery(query_id, text=f"{query_data} is a nice ship")
        bot.sendMessage(chat_id, f"{query_data} is a nice ship")

    elif branch == 2 and leaf == 1:
        if query_data in ship_list:
            s_cost = get_cost(query_data) // 2
            ship_list.remove(query_data)
            money += s_cost
            save_json(chat_id, money=money, ship_list=ship_list)
            bot.answerCallbackQuery(query_id, text=f"Ship {query_data} sold 💲💲💲")
            bot.sendMessage(chat_id,
                            f"Money: {money}$ | Case(s): {user_case}\nYour ship {query_data} was sold and you got {s_cost}$ !")
            bot.sendMessage(chat_id,
                            f"Choose your ship to sell:", reply_markup=KB.sell_ship_button(ship_list))
            bot.sendMessage(chat_id,
                            f'/exit selling ship.', reply_markup=KB.main_keyboard())
        else:
            ship_sell = []
            money_earned = 0
            for ship in ship_list:
                if get_d_sym(get_cost(ship)) == query_data:
                    s_cost = get_cost(ship) // 2
                    ship_sell.append(ship)
                    money += s_cost
                    money_earned += s_cost
                    save_json(chat_id, money=money)
                    bot.sendMessage(chat_id,
                                    f"Money: {money}$ | Case(s): {user_case}\nYour ship {ship} was sold and you got {s_cost}$ !")
            if len(ship_sell) > 0:
                for ship in ship_sell:
                    ship_list.remove(ship)
                save_json(chat_id, ship_list=ship_list)
                bot.sendMessage(chat_id,
                                f"Money: {money}$ | Case(s): {user_case}\n{money_earned}$ earned by selling {len(ship_sell)} ship(s) !")
                bot.answerCallbackQuery(query_id, text=f"{money_earned}$ earned 💲💲💲")
            else:
                bot.sendMessage(chat_id, "No ship(s) to sell")
                bot.answerCallbackQuery(query_id, "No ship(s) to sell")
            bot.sendMessage(chat_id,
                            f"Choose your ship to sell:", reply_markup=KB.sell_ship_button(ship_list))
            bot.sendMessage(chat_id,
                            f'/exit selling ship.', reply_markup=KB.main_keyboard())

    elif branch == 3 and leaf == 1:
        player_cost = 0
        enemy_cost = 0
        player_ship = query_data
        player_let, player_int = player_ship.split("-")
        player_cost = get_cost(player_ship)

        enemy_ship = enemy_list[0]
        enemy_cost = get_cost(enemy_ship)
        if player_cost != 0 and enemy_cost != 0:
            if player_cost > enemy_cost:
                bot.sendMessage(chat_id, f"You won and got: {enemy_cost // 2}$ !")
                damage = random.randint(0, 30)
                time_player_int = int(player_int)
                fin_player_int = time_player_int - damage
                player_int = get_int_ship(fin_player_int)
                new_ship = str(player_let) + str(player_int)
                ship_list.remove(player_ship)
                ship_list.append(new_ship)
                bot.sendMessage(chat_id,
                                f"Your ship has taken {damage} damage. Now it is {new_ship}.")
                money += enemy_cost // 2
                enemy_list.remove(enemy_ship)
                save_json(chat_id, money=money, ship_list=ship_list, enemy_list=enemy_list)
                if len(enemy_list) > 0:
                    bot.answerCallbackQuery(query_id, text=f"Enemy ship {enemy_ship} destroy 🏅")
                    bot.sendMessage(chat_id,
                                    f"You will be fighting with: {str(enemy_list[0])} {str(get_d_sym(get_cost(str(enemy_list[0]))))}")
                    bot.sendMessage(chat_id,
                                    f'Choose your ship to attack:', reply_markup=KB.ship_list_button(ship_list))
                    bot.sendMessage(chat_id, '/exit to leave the battlefield', reply_markup=KB.main_keyboard())
                else:
                    bot.sendMessage(chat_id, f"Battle is finished ! Congratulation !")
                    bot.answerCallbackQuery(query_id, text=f"Battle won 🏆")
                    tree_choice(chat_id)
                    bot.sendMessage(chat_id,
                                    f"Money: {money}$ | Case(s): {user_case}\n\nMenu:\n1. /case_menu\n2. /collection\n3. /fight\n4. /help",
                                    reply_markup=KB.main_keyboard())

            else:
                ship_list.remove(player_ship)
                bot.sendMessage(chat_id, "You've lost your ship! Be careful next time!")
                save_json(chat_id, money=money, ship_list=ship_list, enemy_list=enemy_list)
                if len(ship_list) == 0:
                    bot.sendMessage(chat_id, "Battle is finished. You loose all your ships.")
                    bot.answerCallbackQuery(query_id, text=f"Battle failed 💥")
                    tree_choice(chat_id)
                    bot.sendMessage(chat_id,
                                    f"Money: {money}$ | Case(s): {user_case}\n\nMenu:\n1. /case_menu\n2. /collection\n3. /fight\n4. /help",
                                    reply_markup=KB.main_keyboard())

                else:
                    bot.answerCallbackQuery(query_id, text=f"Your ship {enemy_ship} destroy 💥")
                    bot.sendMessage(chat_id,
                                    f'Choose your ship to attack:', reply_markup=KB.ship_list_button(ship_list))
                    bot.sendMessage(chat_id, '/exit to leave the battlefield', reply_markup=KB.main_keyboard())

    elif branch == 5 and leaf == 1:
        captain_info = load_json(query_data)
        money = captain_info['money']
        username = captain_info['username']
        user_case = captain_info['user_case']
        ship_list = captain_info['ship_list']
        ship_list_str = '\n'.join(ship_list)
        enemy_list = captain_info['enemy_list']
        enemy_list_str = '\n'.join(enemy_list)
        bot.sendMessage(chat_id,
                        f"Captain {username}\n\nMoney: {money}\nCase(s): {user_case}\n\n"
                        f"Ship list:\n{ship_list_str}\n\n"
                        f"Enemy list:\n{enemy_list_str}", reply_markup=KB.captains_keyboard())
        bot.answerCallbackQuery(query_id, text=f"Access to ID card of Captain {username}")

    elif branch == 5 and leaf == 2:
        if int(chat_id) != int(query_data):
            tree_choice(chat_id, branch, leaf, query_data)
            captain_info = load_json(query_data)
            money_captain = captain_info['money']
            username = captain_info['username']
            bot.sendMessage(chat_id,
                            f"How much do you want to send to Captain {username}?\n\nCaptain {username} has {money_captain}$"
                            f"\n\nYou have {money}$\n\n"
                            f"You can choose {settings['cost_case']}, Half, Max or send as you want by typing", reply_markup=KB.send_money_keyboard())
            bot.answerCallbackQuery(query_id, text=f"Login to account of Captain {username}")
        else:
            bot.sendMessage(chat_id, "You can't send money yourself", reply_markup=KB.send_money_keyboard())
            bot.answerCallbackQuery(query_id, text=f"Failed login to account of Captain {username}")


def leaf_output(chat_id, username, command, branch, leaf, money, user_case, ship_list, enemy_list):
    settings = settings_file()
    if branch == 1 and leaf == 1:  # Buy case
        if command.isdigit() or command in ['Half', 'Max']:
            if command.isdigit() and money >= settings['cost_case'] * int(command):
                number = int(command)
            elif command == 'Half' and money >= settings['cost_case']:
                if money == settings['cost_case']:
                    number = 1
                else:
                    number = math.floor((money/settings['cost_case'])/2)
            elif command == 'Max' and money >= settings['cost_case']:
                number = math.floor((money/settings['cost_case']))
            else:
                number = 0
                bot.sendMessage(chat_id, "Not enough money, bro. Try to /sell_ship or /fight\n\n/exit buying case.",
                                reply_markup=KB.case_menu_keyboard())

            if number != 0:
                money -= settings['cost_case'] * number
                user_case += number
                bot.sendMessage(chat_id,
                                f"Money: {money}$ | Case(s): {user_case}\nThanks for buying {number} cases.\n\n/open_case to earn ship\n/exit buying case.",
                                reply_markup=KB.case_menu_keyboard())
                save_json(chat_id, money=money, user_case=user_case)
        else:
            bot.sendMessage(chat_id, "Please use number or /exit", reply_markup=KB.case_menu_keyboard())

    elif branch == 1 and leaf == 2:  # Open case
        if command.isdigit() or command in ['Half', 'Max']:
            if user_case >= 1 and len(ship_list) < settings['ship_fleet']:
                if command.isdigit():
                    number = int(command)
                elif command == 'Half':
                    if user_case == 1:
                        number = 1
                    else:
                        number = math.floor(user_case / 2)
                elif command == 'Max':
                    number = user_case

                if number + len(ship_list) > settings['ship_fleet']:
                    if number > user_case:
                        number = user_case
                        bot.sendMessage(chat_id,
                                        f"Only {number} case(s) will be opened.", reply_markup=KB.case_menu_keyboard())
                    else:
                        number = settings['ship_fleet'] - len(ship_list)
                        bot.sendMessage(chat_id,
                                        f"Only {settings['ship_fleet']} ships is allowed. {number} case(s) will be opened.",
                                        reply_markup=KB.case_menu_keyboard())

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
                                f"\n\n/exit opening case.", reply_markup=KB.case_menu_keyboard())

            elif len(ship_list) == settings['ship_fleet']:
                bot.sendMessage(chat_id,
                                "You have too many ships. /sell_ship and you can open cases again.\n\n/exit opening case.",
                                reply_markup=KB.case_menu_keyboard())
            elif user_case <= 0:
                bot.sendMessage(chat_id,
                                "You don't have case. /buy_case\n\n/exit opening case.", reply_markup=KB.case_menu_keyboard())
        else:
            bot.sendMessage(chat_id, "Please use number or /exit", reply_markup=KB.case_menu_keyboard())

    elif branch == 4 and leaf == 1:
        username = command
        save_json(chat_id, username=username)
        db_id_username(chat_id, username)
        bot.sendMessage(chat_id, 'Save created')
        bot.sendMessage(chat_id,
                        f"Welcome on board Captain {username}\n\n"
                        f"Money: {money}$ | Case(s): {user_case}\n\nMenu:\n1. /case_menu\n2. /collection\n3. /fight\n4. /help")
        bot.sendMessage(chat_id, 'Try /help to see rules, how to play and all functions', reply_markup=KB.main_keyboard())

    elif branch == 5 and leaf == 2:
        contact_captain = save_tree_choice[chat_id]['contact_captain']
        captain_info = load_json(contact_captain)
        money_receiver = captain_info['money']
        if command.isdigit() or command in ['Half', 'Max']:
            if command.isdigit() and money >= int(command):
                gift = int(command)
                if gift == 0:
                    bot.sendMessage(chat_id, "Why did you want to send 0$ ?",
                                    reply_markup=KB.send_money_keyboard())
            elif command == 'Half' and money > 0:
                gift = money / 2
            elif command == 'Max' and money > 0:
                gift = money
            else:
                gift = 0
                bot.sendMessage(chat_id, "Not enough money, bro. Try to /sell_ship or /fight\n\n/exit buying case.",
                                reply_markup=KB.send_money_keyboard())
            if gift > 0:
                bot.sendMessage(contact_captain, f"Captain {username} send you {gift}$")
                money_receiver += gift
                save_json(contact_captain, money=money_receiver)

                bot.sendMessage(chat_id, f"{gift}$ sent to Captain {username}", reply_markup=KB.main_keyboard())
                money -= gift
                save_json(chat_id, money=money)
        else:
            bot.sendMessage(chat_id, "Please use number or /exit", reply_markup=KB.send_money_keyboard())


# Initializing bot
bot = telepot.Bot(secrets['token'])
MessageLoop(bot, {'chat': handle,
                  'callback_query': on_callback_query}).run_as_thread()
print('StarWalkers online')
bot.sendMessage(chat_id_owner, 'StarWalkers online')

while True:
    pass
