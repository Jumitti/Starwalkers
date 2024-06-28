import json
import random
import sys
import time
import base64

import pandas as pd
import streamlit as st

from starwalkers import sql, sound_effects
from starwalkers.func import roll, get_d_sym, get_cost, upgrade_fleet
from panel import ID_card, shop, community, battle

import logging


# Page redirection
def login():
    st.session_state.page = "login"


def register():
    st.session_state.page = "register"


def game():
    st.session_state.page = "game"


# streamlit_app.log for error
logging.basicConfig(
    filename='streamlit_app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Version
version = "Version 3.1.12e_fix2"

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
with st.sidebar.expander("Info and help", expanded=False):
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

    # Audio settings
    if "ambient_sound" not in st.session_state:
        st.session_state.ambient_sound = False
        st.session_state.effect_sound = False
    with st.sidebar.expander("Audio"):
        if st.toggle("Audio"):
            st.session_state.ambient_sound = st.toggle("Ambient sound", value=True)
            st.session_state.effect_sound = st.toggle("Effect sound", value=True)
        else:
            st.session_state.ambient_sound = False
            st.session_state.effect_sound = False

    # Documentation
    st.sidebar.link_button("Documentation", "https://github.com/Jumitti/Starwalkers/blob/main/documentation/DOCUMENTATION.md")


# Login page
if st.session_state.page == "login":
    try:
        st.sidebar.write(version)
        col2.title("Login")
        if st.session_state.ambient_sound:
            sound_effects.ambient()
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
                    st.session_state.trade_token = user[14]
                    st.session_state.battle_played = user[15]
                    st.session_state.grade_damage = user[16]
                    st.session_state.damage_bonus = user[17]
                    st.session_state.grade_resistance = user[18]
                    st.session_state.resistance_bonus = user[19]
                    st.session_state.grade_agility = user[20]
                    st.session_state.agility_bonus = user[21]
                    st.session_state.grade_treasure = user[22]
                    st.session_state.treasure_money_bonus = user[23]
                    st.session_state.treasure_resource_bonus = user[24]
                    st.session_state.treasure_artifact_bonus = user[25]
                    st.session_state.grade_commerce = user[26]
                    st.session_state.commerce_bonus = user[27]
                    st.session_state.grade_navigation = user[28]
                    st.session_state.navigation_price_bonus = user[29]
                    st.session_state.navigation_time_bonus = user[30]
                    st.session_state.grade_token = user[31]
                    st.session_state.token_bonus = user[32]
                    game() & st.rerun()
                else:
                    col2.error("Username or password incorrect")
            else:
                col2.warning("Please complete all fields")
    except Exception as e:
        col2.error(f"Problem with login: {e}")
        logging.exception(f"Error: {e}")

    if col2.button("Create an account", on_click=register):
        st.rerun()

# Register page
elif st.session_state.page == "register":
    try:
        st.sidebar.write(version)
        col2.title("Register")
        if st.session_state.ambient_sound is True:
            sound_effects.ambient()
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
    if st.session_state.ambient_sound:
        sound_effects.ambient()

    # Sidebar
    st.sidebar.divider()
    if st.sidebar.button("🧹 Refresh"):  # For refresh manually
        st.rerun()

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
            st.session_state.trade_token = None
            st.session_state.battle_played = None
            st.session_state.grade_commerce = None
            st.session_state.commerce_bonus = None
            st.session_state.grade_navigation = None
            st.session_state.navigation_price_bonus = None
            st.session_state.navigation_time_bonus = None
            st.session_state.grade_token = None
            st.session_state.token_bonus = None
            login() & st.rerun()
        except Exception as e:
            col2.error(f"Problem during sign out: {e}")
            logging.exception(f"Error: {e}")

    st.sidebar.write(version)

    # Main ID card
    try:
        with col1.container(border=True):
            df, value_list = ID_card.ID_card(st.session_state.username, display='player_info')
    except Exception as e:
        col1.error(f"Problem with ID card: {e}")
        logging.exception(f"Error: {e}")

    # Main shop
    try:
        with col2.container(border=True):
            shop.shop(st.session_state.username, df, value_list)
    except Exception as e:
        col2.error(f"Problem with Shop: {e}")
        logging.exception(f"Error: {e}")

    # Community
    try:
        with col2.container(border=True):
            community.community(st.session_state.username)
    except Exception as e:
        col2.error(f"Problem with Community: {e}")
        logging.exception(f"Error: {e}")

    # Battle
    try:
        with col3.container(border=True):
            battle.battle(st.session_state.username, df)
    except Exception as e:
        col3.error(f"Problem with Battle: {e}")
        logging.exception(f"Error: {e}")
