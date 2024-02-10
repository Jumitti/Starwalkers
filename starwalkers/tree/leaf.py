import json
import math

import telepot

from starwalkers import keyboard as KB
from starwalkers.func import roll, got_let_int, get_d_sym, settings_file
from starwalkers.user_manager import save_json, load_json, db_id_username, save_tree_choice

with open("SECRETS.json", 'r') as secrets_file:
    secrets = json.load(secrets_file)
bot = telepot.Bot(secrets["token"])


def leaf_output(chat_id, command, branch, leaf, money, user_case, ship_list, enemy_list, godmode, money_win,
                money_spent, case_purchased, case_open, fleet_size, language=None, username=None):
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
    if branch == 1 and leaf == 1:  # Buy case
        if command.isdigit() or command in ['Half', 'Max']:
            if command.isdigit() and money >= settings['cost_case'] * int(command):
                number = int(command)
            elif command == 'Half' and money >= settings['cost_case']:
                if money == settings['cost_case']:
                    number = 1
                else:
                    number = math.floor((money / settings['cost_case']) / 2)
            elif command == 'Max' and money >= settings['cost_case']:
                number = math.floor((money / settings['cost_case']))
            else:
                number = 0
                bot.sendMessage(chat_id, "Not enough money, bro. Try to /sell_ship or /fight\n\n/exit buying case.",
                                reply_markup=KB.case_menu_keyboard())

            if number != 0:
                money -= settings['cost_case'] * number
                money_spent += settings['cost_case'] * number
                user_case += number
                case_purchased += number
                bot.sendMessage(chat_id,
                                f"Money: {money}$ | Case(s): {user_case}\nThanks for buying {number} cases.\n\n/open_case to earn ship\n/exit buying case.",
                                reply_markup=KB.case_menu_keyboard())
                save_json(chat_id, money=money, user_case=user_case, money_spent=money_spent, case_purchased=case_purchased)
        else:
            bot.sendMessage(chat_id, "Please use number or /exit", reply_markup=KB.case_menu_keyboard())

    elif branch == 1 and leaf == 2:  # Open case
        if command.isdigit() or command in ['Half', 'Max']:
            if user_case >= 1 and len(ship_list) < fleet_size:
                if command.isdigit():
                    number = int(command)
                elif command == 'Half':
                    if user_case == 1:
                        number = 1
                    else:
                        number = math.floor(user_case / 2)
                elif command == 'Max':
                    number = user_case

                if number + len(ship_list) > fleet_size:
                    if number > user_case:
                        number = user_case
                        bot.sendMessage(chat_id,
                                        f"Only {number} case(s) will be opened.", reply_markup=KB.case_menu_keyboard())
                    else:
                        number = fleet_size - len(ship_list)
                        bot.sendMessage(chat_id,
                                        f"Only {fleet_size} ships is allowed. {number} case(s) will be opened.",
                                        reply_markup=KB.case_menu_keyboard())

                for i in range(0, number):
                    user_case -= 1
                    case_open += 1
                    gotter = roll()
                    ship_list.append(gotter)
                    gotter_letter, gotter_int = gotter.split("-")
                    cost = (got_let_int(gotter_letter) * int(gotter_int)) // 1000
                    bot.sendMessage(chat_id,
                                    f"You got: {gotter} ! It costs: {str(cost)}$ and its rank: {get_d_sym(cost)} !")
                    save_json(chat_id, user_case=user_case, ship_list=ship_list, case_open=case_open)

                bot.sendMessage(chat_id,
                                f"Money: {money}$ | Case(s): {user_case}\nThanks for buying {number} ship(s)."
                                f"\n\nSee your ship(s) in /collection"
                                f"\n\n Earn money by /sell_ship or /fight"
                                f"\n\n/exit opening case.", reply_markup=KB.case_menu_keyboard())

            elif len(ship_list) == fleet_size:
                bot.sendMessage(chat_id,
                                "You have too many ships. /sell_ship and you can open cases again.\n\n/exit opening case.",
                                reply_markup=KB.case_menu_keyboard())
            elif user_case <= 0:
                bot.sendMessage(chat_id,
                                "You don't have case. /buy_case\n\n/exit opening case.",
                                reply_markup=KB.case_menu_keyboard())
        else:
            bot.sendMessage(chat_id, "Please use number or /exit", reply_markup=KB.case_menu_keyboard())

    elif branch == 4 and leaf == 1:  # Username
        username = command
        save_json(chat_id, username=username)
        db_id_username(chat_id, username)
        bot.sendMessage(chat_id, 'Choose your language:', reply_markup=KB.language_keyboard())

    elif branch == 5 and leaf == 2:
        contact_captain = save_tree_choice[chat_id]['contact_captain']
        captain_info = load_json(contact_captain)
        captain_username = captain_info['username']
        if 'godmode' in captain_info:
            captain_godmode = captain_info['godmode']
        else:
            captain_godmode = 'OFF'
            save_json(contact_captain, godmode=captain_godmode)
        if godmode == 'OFF' and captain_godmode == 'OFF':
            money_receiver = captain_info['money']
            if not all(key in captain_info for key in
                       ['win', 'loose', 'money_spent', 'money_win', 'case_purchased', 'case_open']):
                if 'win' not in captain_info:
                    captain_win = captain_info.get('win', 0)
                    save_json(contact_captain, win=captain_win)
                if 'loose' not in captain_info:
                    captain_loose = captain_info.get('loose', 0)
                    save_json(contact_captain, loose=captain_loose)
                if 'money_win' not in captain_info:
                    captain_money_win = captain_info.get('money_win', 0)
                    save_json(contact_captain, money_win=captain_money_win)
                if 'money_spent' not in captain_info:
                    captain_money_spent = captain_info.get('money_spent', 0)
                    save_json(contact_captain, money_spent=captain_money_spent)
                if 'case_purchased' not in captain_info:
                    captain_case_purchased = captain_info.get('case_purchased', 0)
                    save_json(contact_captain, case_purchased=captain_case_purchased)
                if 'case_open' not in captain_info:
                    captain_case_open = captain_info.get('case_open', 0)
                    save_json(contact_captain, case_open=captain_case_open)
                captain_info = load_json(contact_captain)
            else:
                captain_money_win = captain_info['money_win']
            ratio_WL = captain_info['ratio_WL']
            if 'language' in captain_info:
                captain_language = captain_info['language']
                if captain_language == 'ENG':
                    pass
                elif captain_language == 'RU':
                    pass
                elif captain_language == 'FR':
                    pass
            else:
                pass

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
                    captain_money_win += gift
                    save_json(contact_captain, money=money_receiver, money_win=captain_money_win)

                    bot.sendMessage(chat_id, f"{gift}$ sent to Captain {captain_username}", reply_markup=KB.main_keyboard())
                    money -= gift
                    money_spent += gift
                    save_json(chat_id, money=money, money_spent=money_spent)
            else:
                bot.sendMessage(chat_id, "Please use number or /exit", reply_markup=KB.send_money_keyboard())
        else:
            bot.sendMessage(chat_id, f"You or Captain {captain_username} is in godmode. Sending money not allowed")
