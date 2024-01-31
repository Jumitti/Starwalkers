# WELCOME TO STARWALKERS!
Starwalkers is a seemingly simple game where mistakes can cost you dearly. Start your adventure with $30 and buy your first ships. It's time to fight! Can you be the winner?

## Where to play ?
On Telegram directly. Add: [STARWALKERS_bot](https://t.me/StarWalkersBot)

## How to play ?
### Expand your fleet with ``/case_menu``:
  - ``/buy_case`` allows you to buy $10 cases containing a random ship
  - ``/open_case`` allows you to open the crates

### Organize your fleet with ``/collection``:
   - ``/collection`` allows you to keep an eye on your ships and their statistics
   - ``/sell_ship`` allows you to sell a ship

The boats are named "Q-9191" where Q can be any letters from A to Z and 9191 a number between 0000 and 9999.
Cost and rank depend on letter and number. The higher the letter (example: A) and/or the number (example: 9999), the higher the cost and rank.

The rank has a visual way of interpretation: $ to $$$$$.
Be careful, during combat it is the rank that counts and not the visual way of representing it.

### Go to war with ``/fight``:
You will fight randomly from 1 to 3 enemy boats. You can't choose your opponent so choose your boat wisely to fight.
Intuitively, the higher your ship's rank, the more likely it is to win. For example if your ship is A-9999 and it is fighting against Z-0000. You will win because your rank is higher than that of your opponent.

Be careful, during combat it is the rank that counts and not the visual way of representing it.

Ships take damage during combat and lose ranks

### Some tips:
Don't worry about saving, it's automatic and individual. No one can mess with your game.

You can exit any actions at any time with ``/exit``

No more money, no more cash, no more ship, in short, is it over? No, you can use ``/restart``

Lost ? use ``/help`` to see all our commands and tips

## For moding and test with your own TelegramBot 
1. Install [Telepot](https://github.com/nickoala/telepot):
    ```
    pip install telepot
    ```
    (For Raspberry only) Install [gpiozero](https://gpiozero.readthedocs.io/en/latest/):
    ```
    pip install gpiozero
    ```
2. Extract ```starwalkers_telebot.zip``` where you want → [Release]()
   - (For Raspberry) Don't forget to give all permissions at ```starwalkers_telebot``` folder:
     - In ```starwalkers_telebot``` folder, open a terminal:
     ```
     sudo 777 starwalkers_telebot.py
     sudo 777 SECRETS.py
     ```
3. Config ```SECRETS.json``` in ```starwalkers_telebot``` folder

   - How to get your **ID**:
     - send ```/getid``` to [myidbot](https://telegram.me/myidbot) on [Telegram](https://web.telegram.org/k/)
     - Copy/paste your ID in ```SECRETS.json``` without (') or (")
   
   - How to get your **TOKEN**:
     - Config a bot with [@BotFather](https://telegram.me/BotFather):
       - Create a bot with ```/newbot``` and follow instructions
       - Get API token with ```/mybots```, select your bot and get API token
       - Copy/paste your token in ```SECRETS.json``` between (') or (")
     - Don't forget to send ```/start``` at your Telegram bot
4. Run ```starwalkers_telebot.py```:
   - In ```starwalkers_telebot``` folder, open a terminal:
     ```
     python3 starwalkers_telebot.py
     ```
5. That all folks ! You can talk with you Chatbot and play @ Starwalkers🎉

## Credit:
Game by Gametoy20: https://github.com/Gametoy20

Telegram bot by Jumitti: https://github.com/Jumitti
