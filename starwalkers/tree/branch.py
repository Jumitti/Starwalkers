import json
import random
import time

import telepot

from starwalkers import keyboard as KB
from starwalkers.func import roll, get_d_sym, get_cost, settings_file
from starwalkers.user_manager import save_json, load_db_id_username, tree_choice, save_tree_choice

with open("SECRETS.json", 'r') as secrets_file:
    secrets = json.load(secrets_file)
bot = telepot.Bot(secrets["token"])

case_menu_list = ['/buy_case', '💸 Buy case', '/open_case', '🎁 Open case']
captain_menu_list = ['/see_captain', '👀 See', '/send_money', '💸 Send']


def branch_to_leaf(chat_id, command, branch, leaf, money, user_case, ship_list, win, loose, money_win, money_spent,
                   case_purchased, case_open, language=None):
    if language is not None:
        if language == 'ENG':
            pass
        elif language == 'RU':
            pass
        elif language == 'FR':
            pass
    else:
        pass
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
                            f"You don't have ships.\n/buy_case and /open_case to get ships",
                            reply_markup=KB.main_keyboard())

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
            bot.sendMessage(chat_id, "Which captain do you want to send money to?",
                            reply_markup=KB.captains_button(captains))
            tree_choice(chat_id, branch, 2)