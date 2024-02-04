import os
import json
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from func import roll, got_let_int, get_int_ship, get_d_sym, get_cost


def settings_file():
    settings_path = os.path.join(script_directory, 'settings.json')
    with open(settings_path, 'r') as settings_files:
        settings = json.load(settings_files)

        return settings


main_buttons = [
    [KeyboardButton(text='🏪 Case Menu'), KeyboardButton(text='💸 Buy case'), KeyboardButton(text='🎁 Open case')],
    [KeyboardButton(text='🚀 My stats'), KeyboardButton(text='🫱🏽‍🫲🏽 Sell ship'), KeyboardButton(text='💥 Fight !')],
    [KeyboardButton(text='🧑🏽‍🚀 Captains'), KeyboardButton(text='⏪ Exit'), KeyboardButton(text='❔ Help')]
]

language_buttons = [
    [InlineKeyboardButton(text=f"English", callback_data='ENG')],
    [InlineKeyboardButton(text=f"Russian", callback_data='RU')],
    [InlineKeyboardButton(text=f"Francais", callback_data='FR')],
]

case_menu_buttons = [[KeyboardButton(text='1'), KeyboardButton(text='Half'), KeyboardButton(text='Max')]]

captains_buttons = [[KeyboardButton(text='👀 See'), KeyboardButton(text='💸 Send')]]

script_directory = os.path.dirname(os.path.abspath(__file__))
settings = settings_file()
send_money_buttons = [
    [KeyboardButton(text=f"{settings['cost_case']}"), KeyboardButton(text='Half'), KeyboardButton(text='Max')]]


def main_keyboard():
    custom_keyboard = ReplyKeyboardMarkup(keyboard=main_buttons, resize_keyboard=True)
    return custom_keyboard


def case_menu_keyboard():
    buttons = case_menu_buttons + main_buttons
    custom_keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return custom_keyboard


def captains_keyboard():
    buttons = captains_buttons + main_buttons
    custom_keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return custom_keyboard


def send_money_keyboard():
    buttons = send_money_buttons + captains_buttons + main_buttons
    custom_keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return custom_keyboard


def ship_list_button(ship_list):
    buttons = []
    row = []
    for ship in ship_list:
        button = InlineKeyboardButton(text=f"{ship} {get_d_sym(get_cost(ship))}", callback_data=ship)
        row.append(button)
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    ship_list_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return ship_list_keyboard


def sell_ship_button(ship_list):
    buttons = []
    row = []
    for ship in ship_list:
        button = InlineKeyboardButton(text=f"{ship} {get_d_sym(get_cost(ship))}", callback_data=ship)
        row.append(button)
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(text='$', callback_data='$'),
        InlineKeyboardButton(text='$|$', callback_data='$|$')
    ])
    buttons.append([
        InlineKeyboardButton(text='$|$|$', callback_data='$|$|$'),
        InlineKeyboardButton(text='$|$|$|$', callback_data='$|$|$|$')
    ])
    buttons.append([
        InlineKeyboardButton(text='$|$|$|$|$', callback_data='$|$|$|$|$')
    ])

    custom_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return custom_keyboard


def captains_button(captains):
    buttons = []
    row = []
    for user_id, username in captains.items():
        button = InlineKeyboardButton(text=f"{username}", callback_data=user_id)
        row.append(button)
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    custom_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return custom_keyboard


def language_keyboard():
    custom_keyboard = InlineKeyboardMarkup(inline_keyboard=language_buttons)
    return custom_keyboard
