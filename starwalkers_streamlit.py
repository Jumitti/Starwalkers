import json
import random
import sys
import time

import pandas as pd
import streamlit as st

from starwalkers import sql
from starwalkers.func import roll, get_d_sym, get_cost, upgrade_fleet
from panel import ID_card

import logging

logging.basicConfig(
    filename='streamlit_app.log',  # Spécifiez le chemin complet si nécessaire
    level=logging.ERROR,  # Niveau de journalisation (INFO par exemple)
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


# Page redirection
def login():
    st.session_state.page = "login"


def register():
    st.session_state.page = "register"


def game():
    st.session_state.page = "game"


def display_stars(grade):
    full_star = '⭐'  # Emoji pour étoile pleine
    empty_star = '☆'  # Emoji pour étoile vide
    max_stars = 5  # Nombre maximum d'étoiles à afficher

    stars = full_star * grade + empty_star * (max_stars - grade)
    return stars


ship_data = []
enemy_data = []
value_list = []

# Database initialization
sql.init_db()

# Page redirection session_state
if 'page' not in st.session_state:
    st.session_state.page = "login"

# Page config
st.set_page_config(page_title="StarWalkers", page_icon="🚀", initial_sidebar_state="expanded", layout="wide")
col1, col2, col3 = st.columns(3, gap='small')
st.logo("img/starwalkers_v1.png")
st.sidebar.image("img/starwalkers_v1.png")
st.sidebar.header("Welcome to StarWalkers")
st.sidebar.divider()
with st.sidebar.expander("Info and help", expanded=True):
    st.markdown("""
    **Starwalkers** is a seemingly simple game where mistakes can cost you dearly. Start your adventure with **100$** and buy your first ships. It's time to fight! Can you be the winner?

    **Expand** your fleet with **🏪 Shop**:
      - **Buy** and **open** $10 **cases** each containing a random **shuttle**

    Organize your fleet with **🧑🏽‍🚀 ID card**:
      - Keep an **eye** on your **shuttles** and their **statistics**.
      - **Sell** shuttles to earn **money** in the **🏪 Shop**.

    The shuttle are named **"Q-9191"** where **Q** can be any letter from **A to Z** (or a special...) and 9191 a number between **0000 and 9999**.
    **Cost** and **rank** depend on the **letter** and **number**. The higher the letter (example: A) and/or the number (example: 9999), the higher the cost and rank. The **rank** has a visual way of interpretation: 💲.
    Be **careful**, during **combat** it is the **rank** that counts and **not** the visual way of representing it.

    Go to **war** with **⚔️Space battle**:

    You will **fight** randomly from **1 to 4 enemies shuttles** par waves of 1 to 10 enemies. You **can't choose** your **opponent** so **choose your shuttles wisely** to fight.
    Intuitively, the **higher your ship's rank**, the more likely it is to **win**. For example if your ship is **A-9999** and it is fighting against **Z-0000**, you will **win** because **your rank is higher** than that of your opponent.
    Be careful, during combat it is the rank that counts and not the visual way of representing it. **Shuttles** take **damage** during combat and **lose ranks**.

    **Some tips**:
      - Don't worry about saving, it's automatic and individual. No one can mess with your game.
      - No more money, no more cash, no more ship, is it over? No, you can use **"🔃 Reset my profile" button** in the **sidebar**

    **Credit**:
      - GitHub: [https://github.com/Jumitti/starwalkers_telegrambot](https://github.com/Jumitti/starwalkers)
      - Game by Gametoy20: [https://github.com/Gametoy20](https://github.com/Gametoy20)
      - Streamlit app and maintain by Jumitti: [https://github.com/Jumitti](https://github.com/Jumitti)
    """)

# Login page
if st.session_state.page == "login":
    try:
        col2.title("Login")
        username = col2.text_input("Username")
        password = col2.text_input("Password", type="password")
        if col2.button("Login"):
            if username and password:
                if sql.check_password(username, password):
                    user = sql.get_user(username)
                    st.session_state.username = username
                    st.session_state.money = user[2]
                    st.session_state.ship_list = user[3]
                    st.session_state.enemy_list = user[4]
                    st.session_state.fleet_size = user[5]
                    st.session_state.win = user[6]
                    st.session_state.loose = user[7]
                    st.session_state.ratio_WL = user[8]
                    st.session_state.money_win = user[9]
                    st.session_state.money_spent = user[10]
                    st.session_state.grade = user[11]
                    st.session_state.p_letter = user[12]
                    st.session_state.p_number = user[13]
                    game() & st.rerun()
                else:
                    col2.error("Username or password incorrect")
            else:
                col2.warning("Please complete all fields")
    except Exception as e:
        col2.error(f"Problem with login: {e}")
        logging.erro(f"Error: {e}")

    if col2.button("Create an account", on_click=register):
        st.rerun()

# Register page
elif st.session_state.page == "register":
    try:
        col2.title("Register")
        username = col2.text_input("Username")
        password = col2.text_input("Password", type="password")
        if col2.button("Register"):
            if username and password:
                if not sql.get_user(username):
                    sql.add_user(username, password)
                    st.toast("Successful registration !")
                    login() & st.rerun()
                else:
                    col2.error("Username already taken")
            else:
                col2.warning("Please complete all fields")
    except Exception as e:
        col2.error(f"Problem with registration: {e}")
        logging.exception(f"Error: {e}")

    if col2.button("Return to login", on_click=login):
        st.rerun()

# Game page
elif st.session_state.page == "game":
    # Sidebar
    st.sidebar.divider()

    # Sidebar reset profile
    if st.sidebar.button("🔃 Reset my profile"):
        try:
            sql.reset_profile(st.session_state.username)
            st.toast("Your profile has been successfully reset.")
            time.sleep(0.75) & st.rerun()
        except Exception as e:
            st.error(f"Problem during reseting your profil: {e}")
            logging.exception(f"Error: {e}")

    # Sidebar delete account
    if st.sidebar.toggle("🚮 Delete my account"):
        password = st.sidebar.text_input("Entrez votre mot de passe", type="password", label_visibility="collapsed",
                                         placeholder="Enter your password")
        if st.sidebar.button("Confirm deletion"):
            try:
                if sql.check_password(st.session_state.username, password):
                    sql.delete_user(st.session_state.username)
                    st.toast("Your account has been successfully deleted.")
                    register() & st.rerun()
                else:
                    st.sidebar.error("Incorrect password. Try Again.")
            except Exception as e:
                st.error(f"Problem with deletion: {e}")
                logging.exception(f"Error: {e}")

    # Sidebar sign out
    if st.sidebar.button("👋🏽 Sign out"):
        try:
            sql.update_user(st.session_state.username,
                            st.session_state.money,
                            st.session_state.ship_list,
                            st.session_state.enemy_list,
                            st.session_state.fleet_size,
                            st.session_state.win,
                            st.session_state.loose,
                            st.session_state.ratio_WL,
                            st.session_state.money_win,
                            st.session_state.money_spent,
                            st.session_state.grade,
                            st.session_state.p_letter,
                            st.session_state.p_number)
            st.session_state.username = None
            st.session_state.money = None
            st.session_state.ship_list = None
            st.session_state.enemy_list = None
            st.session_state.fleet_size = None
            st.session_state.win = None
            st.session_state.loose = None
            st.session_state.ratio_WL = None
            st.session_state.money_win = None
            st.session_state.money_spent = None
            st.session_state.grade = None
            st.session_state.p_letter = None
            st.session_state.p_number = None
            login() & st.rerun()
        except Exception as e:
            col2.error(f"Problem during sign out: {e}")
            logging.exception(f"Error: {e}")

    # Main ID card
    try:
        with col1.container(border=True):
            df, value_list = ID_card.ID_card(st.session_state.username)

        # id_card.header(f"🧑🏽‍🚀 Captain {st.session_state.username}'s ID Card {display_stars(st.session_state.grade)}")
        #
        # id_card.subheader("Resources")
        # colres1, colres2, colres3 = id_card.columns(3, gap="small")
        # colres1.metric(f"💲 Money", f"{st.session_state.money}$")
        # colres2.metric(f"💵 Money earned", f"{st.session_state.money_win}$")
        # colres3.metric(f"🏷️ Money spent", f"{st.session_state.money_spent}$")
        #
        # id_card.subheader("Space Fleet")
        # with id_card.expander(f"🚀 Space fleet capacity: {st.session_state.fleet_size} ships", expanded=True):
        #     if st.session_state.ship_list:
        #         for ship in json.loads(st.session_state.ship_list):
        #             ship_data.append(
        #                 {"Ship": ship, "Value": get_d_sym(get_cost(ship)).replace('$', '💲'), "Sell": get_cost(ship)})
        #             if get_d_sym(get_cost(ship)) not in value_list:
        #                 value_list.append(get_d_sym(get_cost(ship)))
        #         if ship_data:
        #             df = pd.DataFrame(ship_data).sort_values(by="Sell", ascending=False)
        #             styled_df = df.style.set_table_styles(
        #                 [
        #                     {'selector': 'th', 'props': [('max-width', '150px')]},
        #                     {'selector': 'td', 'props': [('max-width', '150px')]}
        #                 ]
        #             ).set_properties(**{'text-align': 'left'})
        #             st.dataframe(styled_df, use_container_width=True, hide_index=True)
        #
        # id_card.subheader("Battles")
        # colbattle1, colbattle2, colbattle3 = id_card.columns(3, gap="small")
        # colbattle1.metric(f"🏆 Win", f"{st.session_state.win}")
        # colbattle2.metric(f"💥 Loose", f"{st.session_state.loose}")
        # colbattle3.metric(f"⚖️ Win/Loss Ratio", f"{st.session_state.ratio_WL}")
    except Exception as e:
        col1.error(f"Problem with ID card: {e}")
        logging.exception(f"Error: {e}")

    # Main shop
    try:
        shop = col2.container(border=True)
        shop.header("🏪 Store")

        # Open case
        colopencase1, colopencase2 = shop.columns([2, 1], gap="small")
        open_case = colopencase1.slider("**📦 ➡ 🚀 Buy shuttles**", value=int(
            min(st.session_state.fleet_size - len(ship_data), st.session_state.money / 10) / 2) if min(
            st.session_state.fleet_size - len(ship_data), st.session_state.money / 10) > 0 else 1,
                                        step=1, min_value=0,
                                        max_value=int(min(st.session_state.fleet_size - len(ship_data),
                                                      st.session_state.money / 10) if min(
                                            st.session_state.fleet_size - len(ship_data),
                                            st.session_state.money / 10) >= 1 else 1),
                                        disabled=True if st.session_state.money < 10 or len(
                                            ship_data) >= st.session_state.fleet_size else False)

        colopencase2.markdown("")
        if colopencase2.button(f"Open {open_case} case(s) for {open_case * 10}$",
                               disabled=True if st.session_state.money < 10 or len(
                                   ship_data) >= st.session_state.fleet_size else False):
            for i in range(0, open_case):
                ship = roll(proba_letter=st.session_state.p_letter, proba_number=st.session_state.p_number)
                sql.add_ship(st.session_state.username, ship, price=10, add_to="player")
            st.toast("🚀 New shuttle(s) in your fleet!")
            time.sleep(0.75) & st.rerun()

        # Sell ships
        with shop.expander("**🚀 ➡ 💲 Sell shuttle**", expanded=True):
            colsellship1, colsellship2 = st.columns([2, 1], gap="small")

            if not df.empty:
                sell = colsellship1.multiselect("Sell ship", df["Ship"].tolist(), label_visibility="collapsed",
                                                placeholder="Select shuttles for sale")
                price = sum(get_cost(ship) for ship in sell)

                if colsellship2.button(f"Sell selection for {price}$"):
                    for ship in sell:
                        sql.sell_ship(st.session_state.username, ship)

                    st.toast("The shuttles have been sold!")
                    time.sleep(0.75) & st.rerun()

                st.markdown("Sell shuttles of the same value")
                sorted_values = sorted(value_list, reverse=True)
                num_columns = 3
                columns = st.columns(num_columns)
                for i, item in enumerate(sorted_values):
                    col = columns[i % num_columns]
                    elements_safe = item.replace('$', '💲')
                    with col:
                        if st.button(
                                f"{elements_safe} ({sum(get_cost(ship) for ship in json.loads(st.session_state.ship_list) if get_d_sym(get_cost(ship)) == item)}$)",
                                key=f"value_{item}"):
                            for ship in json.loads(st.session_state.ship_list):
                                if get_d_sym(get_cost(ship)) == item:
                                    sql.sell_ship(st.session_state.username, ship)
                            time.sleep(0.75) & st.rerun()
            else:
                st.warning("You don't have any shuttles to sell.")

        # Upgrade fleet size
        if shop.button(
                f"📈 🚀 Upgrade the size of the space fleet by 5 places for {upgrade_fleet(st.session_state.fleet_size)}$",
                disabled=True if st.session_state.money < upgrade_fleet(st.session_state.fleet_size) else False):
            sql.upgrade_fleet_size(st.session_state.username, upgrade_fleet(st.session_state.fleet_size))
            time.sleep(0.75) & st.rerun()
    except Exception as e:
        col2.error(f"Problem with Shop: {e}")
        logging.exception(f"Error: {e}")

    # Community
    try:
        with col2.container(border=True):
            usernames = sql.get_user()
            default_user = st.session_state.username if st.session_state.username in sql.get_user() else usernames[0]
            selected_username = st.selectbox('👨🏽‍🚀 See a Captain', usernames, placeholder="Choose a captain")
            if selected_username:
                ID_card.ID_card(selected_username)

                colsm1, colsm2 = st.columns([2, 1], gap="small")
                send_money = colsm1.slider("💸 Send money", step=1, min_value=0,
                                           max_value=st.session_state.money if st.session_state.money > 0 else 1,
                                           disabled=True if st.session_state.money < 1 or selected_username == st.session_state.username else False)

                colsm2.markdown("")
                if colsm2.button(f"Send {send_money}$ to {selected_username}",
                                 disabled=True if st.session_state.money < 1 or selected_username == st.session_state.username else False):
                    sql.update_money(selected_username, send_money, context="receiver")
                    sql.update_money(st.session_state.username, send_money, context="sender")
                    st.toast(f"💸 {send_money}$ sends to {selected_username}")
                    time.sleep(0.75) & st.rerun()
    except Exception as e:
        col2.error(f"Problem with Community: {e}")
        logging.exception(f"Error: {e}")

    # Battle
    try:
        battle = col3.container(border=True)
        battle.header("⚔️ Space war")
        colwar1, colwar2 = battle.columns(2, gap="small")

        if 'selected_ships_enemy' not in st.session_state or not st.session_state.selected_ships_enemy:
            st.session_state.selected_ships_enemy = []

        if st.session_state.enemy_list:
            colfight1, colfight2 = battle.columns(2, gap="small")
            for ship in json.loads(st.session_state.enemy_list):
                enemy_data.append(
                    {"Ship": ship, "Value": get_d_sym(get_cost(ship)).replace('$', '💲')})
            if enemy_data:
                df_enemy = pd.DataFrame(enemy_data).sort_values(by="Value", ascending=False)
                styled_df_enemy = df_enemy.style.set_table_styles(
                    [
                        {'selector': 'th', 'props': [('max-width', '150px')]},
                        {'selector': 'td', 'props': [('max-width', '150px')]}
                    ]
                ).set_properties(**{'text-align': 'left'})
                colfight1.write("Enemies list:")
                colfight1.dataframe(styled_df_enemy, use_container_width=True, hide_index=True)

                # Vérifiez et sélectionnez aléatoirement les navires ennemis si nécessaire
                if not st.session_state.selected_ships_enemy:
                    num_ships_to_select = random.randint(1, 4 if len(enemy_data) >= 4 else len(enemy_data))
                    st.session_state.selected_ships_enemy = random.sample(enemy_data, num_ships_to_select)

                # Affichage des navires sélectionnés dans le deuxième tableau
                colfight2.write("Fight against:")
                styled_df_enemy = pd.DataFrame(st.session_state.selected_ships_enemy).sort_values(by="Value",
                                                                                                  ascending=False)
                styled_selected_df_enemy = styled_df_enemy.style.set_table_styles([
                    {'selector': 'th', 'props': [('max-width', '150px')]},
                    {'selector': 'td', 'props': [('max-width', '150px')]}
                ]).set_properties(**{'text-align': 'left'})
                colfight2.dataframe(styled_selected_df_enemy, use_container_width=True, hide_index=True)

            if not df.empty and enemy_data:
                colselectfight1, colselectfight2 = battle.columns([2, 1], gap="small")
                shuttles_for_fight = colselectfight1.multiselect("Select shuttles to fight", df["Ship"].tolist(),
                                                                 label_visibility="collapsed",
                                                                 placeholder="Select shuttles to fight (max:4)",
                                                                 max_selections=4, default=df["Ship"].tolist()[:4])
                value_player = sum(get_cost(ship) for ship in shuttles_for_fight)
                value_enemies = sum(get_cost(ship) for ship in styled_df_enemy["Ship"])
                # colselectfight2.write(value_enemies)
                # colselectfight2.write(value_player)
                if colselectfight2.button(f"FIGHT !"):
                    damage = random.randint(0, 30)
                    if value_player > value_enemies:
                        money_win = sum(get_cost(ship) for ship in styled_df_enemy['Ship']) // 1.5
                        sql.update_money(st.session_state.username, money_win if money_win != 0 else 1, context="win")
                        for ship in styled_df_enemy['Ship']:
                            sql.remove_ship(st.session_state.username, ship, "enemies")
                        st.session_state.pop('selected_ships_enemy', None)
                        for ship in shuttles_for_fight:
                            player_let, player_int = ship.split("-")
                            new_number = int(player_int) - (damage // len(shuttles_for_fight))
                            if new_number >= 0:
                                update_ship = roll(letter=player_let, number=new_number)
                                sql.add_ship(st.session_state.username, update_ship, "player", fight=True)
                                sql.remove_ship(st.session_state.username, ship, "player")
                            else:
                                sql.remove_ship(st.session_state.username, ship, "player", fight=True)
                                st.toast(f"💥 You loose {ship} in the battle.")
                        st.toast(f'🏆 You win the battle. 💲 Money win: {money_win}$. 🛠️ Damage: {damage}.')
                        time.sleep(2) & st.rerun()

                    if value_player <= value_enemies:
                        for ship in shuttles_for_fight:
                            sql.remove_ship(st.session_state.username, ship, "player", fight=True)
                        for ship in styled_df_enemy['Ship']:
                            enemy_let, enemy_int = ship.split("-")
                            new_number = int(enemy_int) - (damage // len(styled_df_enemy))
                            if new_number >= 0:
                                update_ship = roll(letter=enemy_let, number=new_number)
                                sql.add_ship(st.session_state.username, update_ship, "enemies", fight=True)
                                sql.remove_ship(st.session_state.username, ship, "enemies")
                            else:
                                sql.remove_ship(st.session_state.username, ship, "enemies", fight=True)
                        st.session_state.pop('selected_ships_enemy', None)
                        st.toast(
                            f'💥 You lost the battle and {" ".join(ship for ship in shuttles_for_fight)} shuttle(s)')
                        time.sleep(0.75) & st.rerun()

                if colwar2.button("🏃‍♂️Leave fight"):
                    if random.random() <= 0.10:  # 10% probability
                        for ship in json.loads(st.session_state.enemy_list):
                            sql.remove_ship(st.session_state.username, ship, "enemies")
                        st.session_state.pop('selected_ships_enemy', None)
                        st.toast("🏃‍♂️You left the battle")
                        time.sleep(0.25) & st.rerun()
                    else:
                        st.toast("✊🏽 We will not run away from this battle!")

            elif df.empty:
                battle.warning("You don't have shuttles")

        if colwar1.button("💥 Look for enemies !", disabled=True if len(enemy_data) > 0 else False):
            for _ in range(random.randint(1, 10)):
                ship = roll(proba_letter=st.session_state.p_letter, proba_number=st.session_state.p_number)
                sql.add_ship(st.session_state.username, ship, "enemies")
            st.toast("⚔️ The enemies enter the battles")
            time.sleep(0.75) & st.rerun()
    except Exception as e:
        col3.error(f"Problem with Battle: {e}")
        logging.exception(f"Error: {e}")
