import json
import time

import telepot

from starwalkers import keyboard as KB
from starwalkers.func import settings_file, upgrade_fleet
from starwalkers.tree.branch import branch_to_leaf
from starwalkers.tree.leaf import leaf_output
from starwalkers.user_manager import save_json, load_json, load_db_id_username, tree_choice, save_tree_choice

with open("SECRETS.json", 'r') as secrets_file:
    secrets = json.load(secrets_file)
bot = telepot.Bot(secrets["token"])

case_menu_list = ['/buy_case', '💸 Buy case', '/open_case', '🎁 Open case']
captain_menu_list = ['/see_captain', '👀 See', '/send_money', '💸 Send']


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
        time.sleep(0.5)
        bot.sendMessage(chat_id, f'Version: {settings["version"]}')
        time.sleep(0.5)
        bot.sendMessage(chat_id, 'Create save...')
        save_json(chat_id, money=settings['starting_money'], user_case=0, ship_list=[], enemy_list=[], win=0, loose=0)
        ID_info = load_json(chat_id)
        money = ID_info['money']
        user_case = ID_info['user_case']
        ship_list = ID_info['ship_list']
        enemy_list = ID_info['enemy_list']

    try:
        win = ID_info['win']
        loose = ID_info['loose']
        fleet_size = ID_info['fleet_size']
        username = ID_info['username']
        language = ID_info['language']
        if language == 'ENG':
            import starwalkers.language.eng as LANG
        elif language == 'RU':
            import starwalkers.language.ru as LANG
        elif language == 'FR':
            import starwalkers.language.fr as LANG
        godmode = ID_info['godmode']
        money_win = ID_info['money_win']
        money_spent = ID_info['money_spent']
        case_purchased = ID_info['case_purchased']
        case_open = ID_info['case_open']
    except KeyError:
        bot.sendMessage(chat_id, f'Update for v{settings["version"]}')
        if 'username' not in ID_info and leaf == 0:
            branch, leaf = tree_choice(chat_id, 4, 0)
        if 'win' not in ID_info:
            win = ID_info.get('win', 0)
            save_json(chat_id, win=win)
        if 'loose' not in ID_info:
            loose = ID_info.get('loose', 0)
            save_json(chat_id, loose=loose)
            ID_info = load_json(chat_id)
        if 'fleet_size' not in ID_info:
            fleet_size = ID_info.get('fleet_size', settings['ship_fleet'])
            save_json(chat_id, fleet_size=fleet_size)
        if 'language' not in ID_info and 'username' in ID_info:
            bot.sendMessage(chat_id, 'Choose your language:', reply_markup=KB.language_keyboard())
        if 'godmode' not in ID_info:
            godmode = ID_info.get('godmode', 'OFF')
            save_json(chat_id, godmode=godmode)
        if 'money_win' not in ID_info:
            money_win = ID_info.get('money_win', 0)
            save_json(chat_id, money_win=money_win)
        if 'money_spent' not in ID_info:
            money_spent = ID_info.get('money_spent', 0)
            save_json(chat_id, money_spent=money_spent)
        if 'case_purchased' not in ID_info:
            case_purchased = ID_info.get('case_purchased', 0)
            save_json(chat_id, case_purchased=case_purchased)
        if 'case_open' not in ID_info:
            case_open = ID_info.get('case_open', 0)
            save_json(chat_id, case_open=case_open)

    ratio_WL = ID_info['ratio_WL']
    money = ID_info['money']
    user_case = ID_info['user_case']
    ship_list = ID_info['ship_list']
    enemy_list = ID_info['enemy_list']

    if branch == 4 and leaf == 0:
        branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list, win, loose, money_win, money_spent, case_purchased, case_open)

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

    elif command == '/restart':
        tree_choice(chat_id)
        save_json(chat_id, money=settings['starting_money'], user_case=0, ship_list=[], enemy_list=[],
                  fleet_size=settings['ship_fleet'], win=0, loose=0, godmode='OFF', money_win=0, money_spent=0, case_open=0, case_purchased=0)
        bot.sendMessage(chat_id,
                        f"Party restarted, you have {settings['starting_money']}$, 0 case, no ship and no enemy",
                        reply_markup=KB.main_keyboard())

    elif command in ['/case_menu', '🏪 Case Menu']:
        bot.sendMessage(chat_id, "What do you want to do with cases?\n1. /buy_case\n2. /open_case\n",
                        reply_markup=KB.main_keyboard())
        tree_choice(chat_id, 1, 0)

    elif command in case_menu_list:
        branch, leaf = tree_choice(chat_id, 1, 0)
        branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list, win, loose, money_win, money_spent, case_purchased, case_open, language)

    elif command in ['/collection', '🚀 My stats']:
        tree_choice(chat_id)
        message = f"GODMODE: ON\n\nWelcome to your fleet Captain {username} !\n\n" if ID_info[
                                                                  'godmode'] == 'ON' else f"Welcome to your fleet Captain {username} !\n\n"
        bot.sendMessage(chat_id,
                        f"{message}"
                        f"Money: {money}$\n"
                        f"  - Earn: {money_win}$\n"
                        f"  - Spent: {money_spent}$\n"
                        f"  - Ration E-S: {money_win - money_spent}\n\n"
                        f"Case(s): {user_case}\n"
                        f"  - Purchased: {case_purchased}\n"
                        f"  - Open: {case_open}\n\n"
                        f"Battle:\n"
                        f"  - Win: {win}\n"
                        f"  - Loose: {loose}\n"
                        f"  - Ratio W/L: {ratio_WL}\n\n"
                        f"Your collection of ships:",
                        reply_markup=KB.ship_list_button(ship_list))
        bot.sendMessage(chat_id, f"\nEarn ships by /buy_case and /open_case"
                                 f"\nEarn money by /sell_ship and /fight", reply_markup=KB.main_keyboard())
        price = upgrade_fleet(fleet_size)
        bot.sendMessage(chat_id, f"Increase the fleet by 5 places for {price}$", reply_markup=KB.upgrade_keyboard())

    elif command in ['/sell_ship', '🫱🏽‍🫲🏽 Sell ship']:
        branch, leaf = tree_choice(chat_id, 2, 0)
        branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list, win, loose, money_win, money_spent, case_purchased, case_open, language)

    elif command in ['/fight', '💥 Fight !']:
        branch, leaf = tree_choice(chat_id, 3, 0)
        branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list, win, loose, money_win, money_spent, case_purchased, case_open, language)

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
        branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list, win, loose, money_win, money_spent, case_purchased, case_open, language)

    elif command == '/godmode':
        tree_choice(chat_id)
        ship_list = []
        save_json(chat_id, money=1000000, user_case=1000000, ship_list=[], enemy_list=[], win=0, loose=0,
                  fleet_size=settings['ship_fleet'], godmode='ON', money_win=0, money_spent=0, case_purchased=0, case_open=0)
        bot.sendMessage(chat_id, "God mode activated, you have 1000000$, 1000000 cases but no ship",
                        reply_markup=KB.main_keyboard())

    elif command in ['/help', '❔ Help']:
        tree_choice(chat_id)
        bot.sendMessage(chat_id,
                        f'WELCOME TO STARWALKERS!\nVersion: {settings["version"]}\n\n'
                        f"Starwalkers is a seemingly simple game where mistakes can cost you dearly. Start your adventure with ${settings['starting_money']} and buy your first ships. It's time to fight! Can you be the winner?\n\n"

                        "Expand your fleet with /case_menu:\n"
                        f"  • /buy_case allows you to buy ${settings['cost_case']} cases containing a random ship\n"
                        "  • /open_case allows you to open the crates\n\n"

                        "Organize your fleet with /collection:\n"
                        "   • /collection allows you to keep an eye on your ships and their statistics\n"
                        "   • /sell_ship allows you to sell a ship\n"
                        'The boats are named "Q-9191" where Q can be any letters from A to Z and 9191 a number between 0000 and 9999.\n'
                        "Cost and rank depend on letter and number. The higher the letter (example: A) and/or the number (example: 9999), the higher the cost and rank. The rank has a visual way of interpretation: $ to $$$$$.\n"
                        "Be careful, during combat it is the rank that counts and not the visual way of representing it.\n\n"

                        "Go to war with /fight:\n"
                        f"You will fight randomly from {settings['min_enemy']} to {settings['max_enemy']} enemy boats. You can't choose your opponent so choose your boat wisely to fight.\n"
                        "Intuitively, the higher your ship's rank, the more likely it is to win. For example if your ship is A-9999 and it is fighting against Z-0000. You will win because your rank is higher than that of your opponent.\n"
                        "Be careful, during combat it is the rank that counts and not the visual way of representing it.\n"
                        "Ships take damage during combat and lose ranks\n\n"

                        "Some tips:\n"
                        "   • Don't worry about saving, it's automatic and individual. No one can mess with your game.\n"
                        "   • You can exit any actions at any time with /exit\n"
                        "   • No more money, no more cash, no more ship, in short, is it over? No, you can use /restart or wait your daily reward\n"
                        "   • Lost ? use /help to see all our commands and tips\n\n"

                        "Credit:\n"
                        "GitHub: https://github.com/Jumitti/starwalkers_telegrambot\n"
                        "Game by Gametoy20: https://github.com/Gametoy20\n"
                        'Telegram bot by Jumitti: https://github.com/Jumitti', reply_markup=KB.main_keyboard())

    else:
        if branch != 0 and leaf == 0:
            branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list, win, loose, money_win,
                           money_spent, case_purchased, case_open, language if 'language' in ID_info else None)

        elif branch != 0 and leaf != 0:
            leaf_output(chat_id, command, branch, leaf, money, user_case, ship_list, enemy_list, godmode, money_win,
                        money_spent, case_purchased, case_open, fleet_size, language if 'language' in ID_info else None,
                        username if 'username' in ID_info else None)