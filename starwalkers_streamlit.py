import streamlit as st
import sqlite3
import bcrypt
from starwalkers import sql
import time
import json
from starwalkers.func import roll, get_d_sym, get_cost
import pandas as pd


# Fonction pour initialiser la base de données
sql.init_db()

ship_data = []
value_list = []

# Fonction pour afficher la page de connexion
def login():
    st.session_state.page = "login"


# Fonction pour afficher la page d'inscription
def register():
    st.session_state.page = "register"


# Fonction pour afficher la page de jeu
def game():
    st.session_state.page = "game"


# Initialisation de la session
if 'page' not in st.session_state:
    st.session_state.page = "login"

st.set_page_config(page_title="StarWalkers", page_icon="🚀", initial_sidebar_state="expanded", layout="wide")
col1, col2, col3 = st.columns(3, gap='small')

# Page de connexion
if st.session_state.page == "login":
    col2.title("Login")
    username = col2.text_input("Username")
    password = col2.text_input("Password", type="password")
    if col2.button("Login"):
        if username and password:
            if sql.check_password(username, password):
                user = sql.get_user(username)
                st.session_state.username = username
                st.session_state.cases = user[2]
                st.session_state.money = user[3]
                st.session_state.ship_list = user[4]
                st.session_state.enemy_list = user[5]
                st.session_state.fleet_size = user[6]
                st.session_state.win = user[7]
                st.session_state.loose = user[8]
                st.session_state.ratio_WL = user[9]
                st.session_state.money_win = user[10]
                st.session_state.money_spent = user[11]
                st.session_state.case_purchased = user[12]
                st.session_state.case_open = user[13]
                game() & st.rerun()
            else:
                col2.error("Username or password incorrect")
        else:
            col2.warning("Please complete all fields")
    if col2.button("Create an account", on_click=register):
        st.rerun()

# Page d'inscription
elif st.session_state.page == "register":
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
    if col2.button("Return to login", on_click=login):
        st.rerun()

# Page de jeu
elif st.session_state.page == "game":
    if st.sidebar.button("Réinitialiser mon profil"):
        sql.reset_profile(st.session_state.username)
        st.toast("Votre profil a été réinitialisé avec succès.")
        time.sleep(0.25) & st.rerun()

        # Section pour supprimer le compte
    if st.sidebar.checkbox("Supprimer mon compte"):
        password = st.sidebar.text_input("Entrez votre mot de passe", type="password")
        if st.sidebar.button("Confirmer la suppression"):
            if sql.check_password(st.session_state.username, password):
                sql.delete_user(st.session_state.username)
                st.toast("Votre compte a été supprimé avec succès.")
                register() & st.rerun()
            else:
                st.error("Mot de passe incorrect. Veuillez réessayer.")

    if st.sidebar.button("Sign out"):
        sql.update_user(st.session_state.username,
                        st.session_state.cases,
                        st.session_state.money,
                        st.session_state.ship_list,
                        st.session_state.enemy_list,
                        st.session_state.fleet_size,
                        st.session_state.win,
                        st.session_state.loose,
                        st.session_state.ratio_WL,
                        st.session_state.money_win,
                        st.session_state.money_spent,
                        st.session_state.case_purchased,
                        st.session_state.case_open)
        st.session_state.username = None
        st.session_state.cases = None
        st.session_state.money = None
        st.session_state.ship_list = None
        st.session_state.enemy_list = None
        st.session_state.fleet_size = None
        st.session_state.win = None
        st.session_state.loose = None
        st.session_state.ratio_WL = None
        st.session_state.money_win = None
        st.session_state.money_spent = None
        st.session_state.case_purchased = None
        st.session_state.case_open = None
        login() & st.rerun()

    container = col1.container(border=True)
    container.header(f"Captain {st.session_state.username}'s Identity Card")

    container.subheader("Resources")
    container.write(f"Available Money: {st.session_state.money}$")
    container.write(f"Number of cases: {st.session_state.cases}")

    container.subheader("Space Fleet")
    container.write(f"Space fleet capacity: {st.session_state.fleet_size} ships")
    if st.session_state.ship_list:
        for ship in json.loads(st.session_state.ship_list):
            ship_data.append({"Ship": ship, "Value": get_d_sym(get_cost(ship)).replace('$', '💲'), "Sell": get_cost(ship)})
            if get_d_sym(get_cost(ship)) not in value_list:
                value_list.append(get_d_sym(get_cost(ship)))
        if ship_data:
            df = pd.DataFrame(ship_data).sort_values(by="Value", ascending=False)
            styled_df = df.style.set_table_styles(
                [
                    {'selector': 'th', 'props': [('max-width', '150px')]},
                    {'selector': 'td', 'props': [('max-width', '150px')]}
                ]
            ).set_properties(**{'text-align': 'left'})
            container.dataframe(styled_df, use_container_width=True, hide_index=True)

    container.subheader("Battles")
    container.write(f"Number of wins: {st.session_state.win}")
    container.write(f"Number of losses: {st.session_state.loose}")
    container.write(f"Win/Loss Ratio: {st.session_state.ratio_WL}")

    container.subheader("Financial Statistics")
    container.write(f"Money earned: ${st.session_state.money_win}")
    container.write(f"Money spent: ${st.session_state.money_spent}")
    container.write(f"Number of cases purchased: {st.session_state.case_purchased}")
    container.write(f"Number of cases opened: {st.session_state.case_open}")

    buy_cases = col2.slider("Buy cases (10$)", value=int(st.session_state.money/20) if st.session_state.money > 10 else 0,
                            step=1, min_value=0, max_value=int(st.session_state.money/10) if st.session_state.money > 10 else 1,
                            disabled=True if st.session_state.money < 10 else False)
    if col2.button(f"Buy {buy_cases} case(s) for {10*buy_cases}$"):
        sql.buy_cases(st.session_state.username, buy_cases)
        st.toast(f"You have buy {buy_cases} case(s) for {10*buy_cases}$.")
        time.sleep(0.25) & st.rerun()

    open_case = col2.slider("Open cases", value=int(min(st.session_state.fleet_size - len(ship_data), st.session_state.cases)/2) if min(st.session_state.fleet_size - len(ship_data), st.session_state.cases) > 0 else 1,
                            step=1, min_value=0,
                            max_value=min(st.session_state.fleet_size - len(ship_data), st.session_state.cases) if min(st.session_state.fleet_size - len(ship_data), st.session_state.cases) > 0 else 1,
                            disabled=True if st.session_state.cases < 1 or len(ship_data) >= st.session_state.fleet_size else False)
    if col2.button("Ajouter aléatoirement une navette", disabled=True if st.session_state.cases < 1 else False):
        for i in range(0, open_case):
            ship = roll()
            sql.add_ship(st.session_state.username, ship)
            st.toast("Une nouvelle navette a été ajoutée à votre flotte !")
        time.sleep(0.25) & st.rerun()
    with col2.expander("Sell ship", expanded=True):
        if ship_data:
            sell = st.multiselect("Sell ship", df["Ship"].tolist())
            if st.button("Sell selection"):
                for ship in sell:
                    sql.sell_ship(st.session_state.username, ship)
                time.sleep(0.25) & st.rerun()
            st.markdown("Sell ships with same value")
            sorted_values = sorted(value_list, reverse=True)
            for item in sorted_values:
                elements_safe = item.replace('$', '💲')
                if st.button(f"{elements_safe} "
                             f"({sum(get_cost(ship) for ship in json.loads(st.session_state.ship_list) if get_d_sym(get_cost(ship)) == item)}$)",
                             key=f"value_{item}"):
                    for ship in json.loads(st.session_state.ship_list):
                        if get_d_sym(get_cost(ship)) == item:
                            sql.sell_ship(st.session_state.username, ship)
                    time.sleep(0.25) & st.rerun()
        else:
            st.warning("Vous n'avez pas de navettes à vendre")

