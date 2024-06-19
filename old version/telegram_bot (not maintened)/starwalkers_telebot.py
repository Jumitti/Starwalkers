import json
import os

import schedule
import telepot
from telepot.loop import MessageLoop

from starwalkers.func import daily_reward
from starwalkers.tree.query import on_callback_query
from starwalkers.tree.trunk import handle

script_directory = os.path.dirname(os.path.abspath(__file__))
secrets_path = os.path.join(script_directory, 'SECRETS.json')
with open(secrets_path, 'r') as secrets_file:
    secrets = json.load(secrets_file)

chat_id_owner = secrets['id_owner']

# Initializing bot
bot = telepot.Bot(secrets['token'])
MessageLoop(bot, {'chat': handle, 'callback_query': on_callback_query}).run_as_thread()
print('StarWalkers online')
bot.sendMessage(chat_id_owner, 'StarWalkers online')
schedule.every().day.at("05:00").do(daily_reward)  # Daily reward

while True:
    schedule.run_pending()  # Daily reward
    pass
