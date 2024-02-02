from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

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
