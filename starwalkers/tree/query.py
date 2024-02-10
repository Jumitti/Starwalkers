import json
import random

import telepot

from starwalkers import keyboard as KB
from starwalkers.func import roll, get_d_sym, get_cost, settings_file, upgrade_fleet
from starwalkers.user_manager import save_json, load_json, tree_choice, save_tree_choice

with open("SECRETS.json", 'r') as secrets_file:
    secrets = json.load(secrets_file)
bot = telepot.Bot(secrets["token"])


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
    if 'username' in ID_info:
        username = ID_info['username']
    win = ID_info['win']
    loose = ID_info['loose']
    ratio_WL = ID_info['ratio_WL']
    fleet_size = ID_info['fleet_size']
    money_win = ID_info['money_win']
    money_spent = ID_info['money_spent']
    case_purchased = ID_info['case_purchased']
    case_open = ID_info['case_open']
    if 'language' in ID_info:
        language = ID_info['language']
        if language == 'ENG':
            pass
        elif language == 'RU':
            pass
        elif language == 'FR':
            pass
    else:
        pass

    if query_data in ['ENG', 'RU', 'FR']:
        save_json(chat_id, language=query_data)
        bot.answerCallbackQuery(query_id, text=f"Language {query_data} selected")
        bot.sendMessage(chat_id, f"Language {query_data} selected")
        bot.sendMessage(chat_id, 'Save created')
        bot.sendMessage(chat_id,
                        f"Welcome on board Captain {username}\n\n"
                        f"Money: {money}$ | Case(s): {user_case}\n\nMenu:\n1. /case_menu\n2. /collection\n3. /fight\n4. /help")
        bot.sendMessage(chat_id, 'Try /help to see rules, how to play and all functions',
                        reply_markup=KB.main_keyboard())

    elif query_data == "upgrade_fleet":
        if money >= upgrade_fleet(fleet_size):
            money -= upgrade_fleet(fleet_size)
            money_spent += upgrade_fleet(fleet_size)
            fleet_size += 5
            save_json(chat_id, money=money, fleet_size=fleet_size, money_spent=money_spent)
            price = upgrade_fleet(fleet_size)
            bot.sendMessage(chat_id, f'5 places have been purchased. Congratulations Captain {username}\n\n'
                                     f'Increase the fleet by 5 places for {price}$', reply_markup=KB.upgrade_keyboard())
            bot.answerCallbackQuery(query_id, text=f"5 places have been purchased 🚀")
        else:
            bot.sendMessage(chat_id, f"You don't have the money you need")
            bot.answerCallbackQuery(query_id, text=f"Not purchased 📉")

    elif branch == 0 and leaf == 0:
        bot.answerCallbackQuery(query_id, text=f"{query_data} is a nice ship")
        bot.sendMessage(chat_id, f"{query_data} is a nice ship")

    elif branch == 2 and leaf == 1:
        if query_data in ship_list:
            s_cost = get_cost(query_data) // 2
            ship_list.remove(query_data)
            money += s_cost
            money_win += s_cost
            save_json(chat_id, money=money, ship_list=ship_list, money_win=money_win)
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
                    money_win += s_cost
                    money_earned += s_cost
                    save_json(chat_id, money=money, money_win=money_win)
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
                new_ship = roll(letter=player_let, number=fin_player_int)
                ship_list.remove(player_ship)
                ship_list.append(new_ship)
                bot.sendMessage(chat_id,
                                f"Your ship has taken {damage} damage. Now it is {new_ship}.")
                money += enemy_cost // 2
                money_win += enemy_cost // 2
                enemy_list.remove(enemy_ship)
                win += 1
                save_json(chat_id, money=money, ship_list=ship_list, enemy_list=enemy_list, win=win, money_win=money_win)
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
                loose += 1
                save_json(chat_id, ship_list=ship_list, enemy_list=enemy_list, loose=loose, money_win=money_win)
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

    elif branch == 5 and leaf == 1:  # See stats from other player
        captain_info = load_json(query_data)
        money = captain_info['money']
        username = captain_info['username']
        user_case = captain_info['user_case']
        ship_list = captain_info['ship_list']
        ship_list_str = '\n'.join([f"{ship} {get_d_sym(get_cost(ship))}" for ship in ship_list])
        enemy_list = captain_info['enemy_list']
        enemy_list_str = '\n'.join([f"{ship} {get_d_sym(get_cost(ship))}" for ship in enemy_list])
        if not all(key in captain_info for key in ['win', 'loose', 'money_spent', 'money_win', 'case_purchased', 'case_open']):
            if 'win' not in captain_info:
                win = captain_info.get('win', 0)
                save_json(query_data, win=win)
            if 'loose' not in captain_info:
                loose = captain_info.get('loose', 0)
                save_json(query_data, loose=loose)
            if 'money_win' not in captain_info:
                money_win = captain_info.get('money_win', 0)
                save_json(query_data, money_win=money_win)
            if 'money_spent' not in captain_info:
                money_spent = captain_info.get('money_spent', 0)
                save_json(query_data, money_spent=money_spent)
            if 'case_purchased' not in captain_info:
                case_purchased = captain_info.get('case_purchased', 0)
                save_json(query_data, case_purchased=case_purchased)
            if 'case_open' not in captain_info:
                case_open = captain_info.get('case_open', 0)
                save_json(query_data, case_open=case_open)
            captain_info = load_json(query_data)
        win = captain_info['win']
        loose = captain_info['loose']
        money_win = captain_info['money_win']
        money_spent = captain_info['money_spent']
        case_purchased = captain_info['case_purchased']
        case_open = captain_info['case_open']
        ratio_WL = captain_info['ratio_WL']
        message = f"GODMODE: ON\n\nCaptain {username}\n\n" if captain_info['godmode'] == 'ON' else f"Captain {username}\n\n"
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
                            f"You can choose {settings['cost_case']}, Half, Max or send as you want by typing",
                            reply_markup=KB.send_money_keyboard())
            bot.answerCallbackQuery(query_id, text=f"Login to account of Captain {username}")
        else:
            bot.sendMessage(chat_id, "You can't send money yourself", reply_markup=KB.send_money_keyboard())
            bot.answerCallbackQuery(query_id, text=f"Failed login to account of Captain {username}")
