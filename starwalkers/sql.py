import json
import os
import sqlite3

import bcrypt
import streamlit as st
from bcrypt import checkpw

from starwalkers.func import get_cost


# Fonction pour initialiser la base de données
def init_db():
    if not os.path.exists('user'):
        os.makedirs('user')

    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    # Crée une table temporaire sans la colonne 'money'
    c.execute('''CREATE TABLE IF NOT EXISTS users_temp
                 (username TEXT PRIMARY KEY,
                 password_hash TEXT,
                 money INTEGER,
                 ship_list TEXT,
                 enemy_list TEXT,
                 fleet_size INTEGER,
                 win INTEGER,
                 loose INTEGER,
                 ratio_WL REAL,
                 money_win INTEGER,
                 money_spent INTEGER,
                 grade INTEGER,
                 p_letter REAL,
                 p_number REAL)''')
    
    # Vérifie si la colonne existe, sinon l'ajoute
    c.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in c.fetchall()]

    if 'case_purchased' in columns:
        c.execute('ALTER TABLE users DROP COLUMN case_purchased')
    if 'case_open' in columns:
        c.execute('ALTER TABLE users DROP COLUMN case_open')
    if 'p_letter' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN p_letter REAL DEFAULT 0.5')
        c.execute('UPDATE users SET p_letter = 0.5 WHERE p_letter IS NULL')
    if 'p_number' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN p_number REAL DEFAULT -0.0004')
        c.execute('UPDATE users SET p_number = -0.0004 WHERE p_number IS NULL')

    conn.commit()
    conn.close()


# Fonction pour ajouter un utilisateur avec mot de passe hashé
def add_user(username, password):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute("INSERT INTO users (username,"
              "password_hash,"
              "money,"
              "ship_list,"
              "enemy_list,"
              "fleet_size,"
              "win,"
              "loose,"
              "ratio_WL,"
              "money_win,"
              "money_spent,"
              "grade,"
              "p_letter,"
              "p_number)"
              "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (username, hashed_password, 100, '', '', 10, 0, 0, 0.00, 0, 0, 0, 0.5, -0.0004))
    conn.commit()
    conn.close()


def reset_profile(username):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET money=?,"
              "ship_list=?,"
              "enemy_list=?,"
              "fleet_size=?,"
              "win=?,"
              "loose=?,"
              "ratio_WL=?,"
              "money_win=?,"
              "money_spent=?,"
              "grade=?,"
              "p_letter=?,"
              "p_number=? "
              "WHERE username=?", (100, '', '', 10, 0, 0, 0.00, 0, 0, 0, 0.5, -0.0004, username))  # Réinitialiser les paramètres nécessaires
    conn.commit()

    user = get_user(username)
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

    conn.close()


# Fonction pour hasher le mot de passe
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


# Fonction pour vérifier si le mot de passe correspond
def check_password(username, password):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        stored_hash = result[0]  # Récupérer le hash du mot de passe depuis le résultat
        return checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
    else:
        return False


# Fonction pour obtenir un utilisateur
def get_user(username=None):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()
    if username:
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
    elif not username:
        c.execute("SELECT username FROM users")
        user = [row[0] for row in c.fetchall()]
    conn.close()
    return user


# Fonction pour mettre à jour les informations de l'utilisateur (argent)
def update_money(username, amount, context="win"):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    if context == 'sender':
        c.execute("UPDATE users SET money=money - ?, money_spent=money_spent + ? WHERE username=?", (amount, amount, username))

    elif context == "receiver" or context == "win":
        c.execute("UPDATE users SET money=money + ?, money_win=money_win + ? WHERE username=?", (amount, amount, username))

    conn.commit()

    if context == "sender":
        user = get_user(username)
        st.session_state.money = user[2]
        st.session_state.money_spent = user[10]
    elif context == 'win':
        user = get_user(username)
        st.session_state.money = user[2]
        st.session_state.money_win = user[9]

    conn.close()


# Fonction pour mettre à jour les informations de l'utilisateur (cases)
def update_user(username, money, ship_list, enemy_list, fleet_size, win, loose, ratio_WL, money_win, money_spent, grade, p_letter, p_number):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET money=?,"
              "ship_list=?,"
              "enemy_list=?,"
              "fleet_size=?,"
              "win=?,"
              "loose=?,"
              "ratio_WL=?,"
              "money_win=?,"
              "money_spent=?,"
              "grade=?,"
              "p_letter=?,"
              "p_number=? "
              "WHERE username=?",
              (money, ship_list, enemy_list, fleet_size, win, loose, ratio_WL, money_win, money_spent, grade, p_letter, p_number, username))
    conn.commit()
    conn.close()


def delete_user(username):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()


def add_ship(username, new_ship, add_to, fight=False, price=None):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    if add_to == "player":
        # Récupérer la ship_list actuelle du joueur
        c.execute("SELECT ship_list FROM users WHERE username=?", (username,))
        current_ship_list_json = c.fetchone()[0]

        # Charger la liste actuelle depuis JSON ou initialiser une liste vide si elle est nulle
        current_ship_list = json.loads(current_ship_list_json) if current_ship_list_json else []

        # Ajouter la nouvelle navette à la liste
        current_ship_list.append(new_ship)

        # Convertir la liste en JSON pour la sauvegarde dans la base de données
        updated_ship_list_json = json.dumps(current_ship_list)

        # Mettre à jour la base de données avec la nouvelle liste de navettes
        if fight is False:
            c.execute("UPDATE users SET ship_list=?, money=money - ?, money_spent=money_spent + ? WHERE username=?", (updated_ship_list_json, price, price, username))
            conn.commit()

            user = get_user(username)
            st.session_state.money = user[2]
            st.session_state.ship_list = user[3]
            st.session_state.money_spent = user[10]
        elif fight is True:
            c.execute("UPDATE users SET ship_list=?, win=win + ?, ratio_WL = CASE WHEN loose > 0.00 THEN (win + ?) / loose ELSE win + ?  END WHERE username=?",
                      (updated_ship_list_json, 1, 1.00, 1.00, username))
            conn.commit()

            user = get_user(username)
            st.session_state.cases = user[2]
            st.session_state.win = user[6]
            st.session_state.ratio_WL = user[8]

    elif add_to == "enemies":
        # Récupérer la ship_list actuelle du joueur
        c.execute("SELECT enemy_list FROM users WHERE username=?", (username,))
        current_enemy_list_json = c.fetchone()[0]

        # Charger la liste actuelle depuis JSON ou initialiser une liste vide si elle est nulle
        current_enemy_list = json.loads(current_enemy_list_json) if current_enemy_list_json else []

        # Ajouter la nouvelle navette à la liste
        current_enemy_list.append(new_ship)

        # Convertir la liste en JSON pour la sauvegarde dans la base de données
        updated_enemy_list_json = json.dumps(current_enemy_list)

        # Mettre à jour la base de données avec la nouvelle liste de navettes
        c.execute("UPDATE users SET enemy_list=? WHERE username=?",
                  (updated_enemy_list_json, username))
        conn.commit()

        user = get_user(username)
        st.session_state.enemy_list = user[4]

    conn.close()


# Fonction pour supprimer une navette spécifique d'un utilisateur
def sell_ship(username, ship):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    # Récupérer la ship_list actuelle du joueur
    c.execute("SELECT ship_list FROM users WHERE username=?", (username,))
    current_ship_list_json = c.fetchone()[0]

    # Charger la liste actuelle depuis JSON
    current_ship_list = json.loads(current_ship_list_json)

    # Supprimer la navette spécifique
    if ship in current_ship_list:
        money_earned = get_cost(ship)
        current_ship_list.remove(ship)

    # Convertir la liste mise à jour en JSON pour la sauvegarde dans la base de données
    updated_ship_list_json = json.dumps(current_ship_list)

    # Mettre à jour la base de données avec la nouvelle liste de navettes
    c.execute("UPDATE users SET ship_list=?, money=money + ?, money_win=money_win + ? WHERE username=?", (updated_ship_list_json, money_earned, money_earned, username))
    conn.commit()

    user = get_user(username)
    st.session_state.money = user[2]
    st.session_state.ship_list = user[3]
    st.session_state.money_win = user[9]

    conn.close()


def remove_ship(username, ship, remove_from, fight=False):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    if remove_from == "player":
        # Récupérer la ship_list actuelle du joueur
        c.execute("SELECT ship_list FROM users WHERE username=?", (username,))
        current_ship_list_json = c.fetchone()[0]

        # Charger la liste actuelle depuis JSON
        current_ship_list = json.loads(current_ship_list_json)

        # Supprimer la navette spécifique
        if ship in current_ship_list:
            current_ship_list.remove(ship)

        # Convertir la liste mise à jour en JSON pour la sauvegarde dans la base de données
        updated_ship_list_json = json.dumps(current_ship_list)

        if fight is False:
            # Mettre à jour la base de données avec la nouvelle liste de navettes
            c.execute("UPDATE users SET ship_list=? WHERE username=?",
                      (updated_ship_list_json, username))
            conn.commit()

            user = get_user(username)
            st.session_state.ship_list = user[3]

        elif fight is True:
            # Mettre à jour la base de données avec la nouvelle liste de navettes
            c.execute("UPDATE users SET ship_list=?, loose=loose + ?, ratio_WL = CASE WHEN win > 0.00 THEN win / (loose + ?) ELSE 0.00 / (loose + ?) END WHERE username=?",
                      (updated_ship_list_json, 1, 1.00, 1.00, username))
            conn.commit()

            user = get_user(username)
            st.session_state.ship_list = user[3]
            st.session_state.loose = user[7]
            st.session_state.ratio_WL = user[8]

    elif remove_from == "enemies":
        # Récupérer la ship_list actuelle du joueur
        c.execute("SELECT enemy_list FROM users WHERE username=?", (username,))
        current_enemy_list_json = c.fetchone()[0]

        # Charger la liste actuelle depuis JSON
        current_enemy_list = json.loads(current_enemy_list_json)

        # Supprimer la navette spécifique
        if ship in current_enemy_list:
            current_enemy_list.remove(ship)

        # Convertir la liste mise à jour en JSON pour la sauvegarde dans la base de données
        updated_enemy_list_json = json.dumps(current_enemy_list)

        # Mettre à jour la base de données avec la nouvelle liste de navettes
        c.execute("UPDATE users SET enemy_list=? WHERE username=?",
                  (updated_enemy_list_json, username))
        conn.commit()

        user = get_user(username)
        st.session_state.enemy_list = user[4]

    conn.close()


# Upgrade fleet size
def upgrade_fleet_size(username, amount):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET fleet_size=fleet_size + ?, money=money - ?, money_spent=money_spent + ? WHERE username=?", (5, amount, amount, username))
    conn.commit()

    # Mettre à jour st.session_state.money
    user = get_user(username)
    st.session_state.money = user[2]
    st.session_state.fleet_size = user[5]
    st.session_state.money_spent = user[10]

    conn.close()
