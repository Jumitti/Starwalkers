from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from func import roll, got_let_int, get_int_ship, get_d_sym, get_cost

main_buttons = [
            [KeyboardButton(text='🏪 Case Menu'), KeyboardButton(text='💸 Buy case'), KeyboardButton(text='🎁 Open case')],
            [KeyboardButton(text='🚀 Collection/Fleet'), KeyboardButton(text='🫱🏽‍🫲🏽 Sell ship'), KeyboardButton(text='💥 Fight !')],
            [KeyboardButton(text='⏪ Exit'), KeyboardButton(text='🔄️ Restart'), KeyboardButton(text='❔ Help')]
        ]

case_menu_buttons = [[KeyboardButton(text='1'), KeyboardButton(text='Half'), KeyboardButton(text='Max')]]


def main_keyboard():
    custom_keyboard = ReplyKeyboardMarkup(keyboard=main_buttons, resize_keyboard=True)
    return custom_keyboard


def case_menu_keyboard():
    buttons = case_menu_buttons + main_buttons
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


def sell_ship_keyboard(ship_list):
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
