from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def main_keyboard():
    buttons = [
            [KeyboardButton(text='🏪 Case Menu'), KeyboardButton(text='💸 Buy case'), KeyboardButton(text='🎁 Open case')],
            [KeyboardButton(text='🚀 Collection/Fleet'), KeyboardButton(text='🫱🏽‍🫲🏽 Sell ship'), KeyboardButton(text='💥 Fight !')],
            [KeyboardButton(text='⏪ Exit'), KeyboardButton(text='🔄️ Restart'), KeyboardButton(text='❔ Help')]
        ]

    custom_keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    return custom_keyboard
