import decimal
import json
import os
import sqlite3

import bcrypt
import streamlit as st
from bcrypt import checkpw

from starwalkers.func import get_cost


# Function to initialize the database
def init_db():
    if not os.path.exists('user'):
        os.makedirs('user')

    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
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
                 p_number REAL,
                 trade_token INTEGER,
                 battle_played INTEGER,
                 grade_damage INTEGER,
                 damage_bonus REAL,
                 grade_resistance INTEGER,
                 resistance_bonus REAL,
                 grade_agility INTEGER,
                 agility_bonus REAL,
                 grade_treasure INTEGER,
                 treasure_money_bonus REAL,
                 treasure_resource_bonus REAL,
                 treasure_artifact_bonus REAL,
                 grade_commerce INTEGER,
                 commerce_bonus REAL,
                 grade_navigation INTEGER,
                 navigation_price_bonus REAL,
                 navigation_time_bonus INTEGER,
                 grade_token INTEGER,
                 token_bonus INTEGER)''')

    # Checks if the column exists, otherwise adds it
    c.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in c.fetchall()]

    if 'trade_token' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN trade_token INTEGER DEFAULT 0')
        c.execute('UPDATE users SET trade_token = 0 WHERE trade_token IS NULL')
    if 'battle_played' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN battle_played INTEGER DEFAULT 0')
        c.execute('UPDATE users SET battle_played = 0 WHERE battle_played IS NULL')
    if 'grade_damage' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN grade_damage INTEGER DEFAULT 0')
        c.execute('UPDATE users SET grade_damage = 0 WHERE grade_damage IS NULL')
    if 'damage_bonus' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN damage_bonus REAL DEFAULT 1.00')
        c.execute('UPDATE users SET damage_bonus = 1.00 WHERE damage_bonus IS NULL')

    if 'grade_resistance' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN grade_resistance INTEGER DEFAULT 0')
        c.execute('UPDATE users SET grade_resistance = 0 WHERE grade_resistance IS NULL')
    if 'resistance_bonus' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN resistance_bonus REAL DEFAULT 1.00')
        c.execute('UPDATE users SET resistance_bonus = 1.00 WHERE resistance_bonus IS NULL')

    if 'grade_agility' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN grade_agility INTEGER DEFAULT 0')
        c.execute('UPDATE users SET grade_agility = 0 WHERE grade_agility IS NULL')
    if 'agility_bonus' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN agility_bonus REAL DEFAULT 0.10')
        c.execute('UPDATE users SET agility_bonus = 0.10 WHERE agility_bonus IS NULL')

    if 'grade_treasure' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN grade_treasure INTEGER DEFAULT 0')
        c.execute('UPDATE users SET grade_treasure = 0 WHERE grade_treasure IS NULL')
    if 'treasure_money_bonus' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN treasure_money_bonus REAL DEFAULT 1.00')
        c.execute('UPDATE users SET treasure_money_bonus = 1.00 WHERE treasure_money_bonus IS NULL')
    if 'treasure_resource_bonus' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN treasure_resource_bonus REAL DEFAULT 1.00')
        c.execute('UPDATE users SET treasure_resource_bonus = 1.00 WHERE treasure_resource_bonus IS NULL')
    if 'treasure_artifact_bonus' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN treasure_artifact_bonus REAL DEFAULT 0.0001')
        c.execute('UPDATE users SET treasure_artifact_bonus = 0.0001 WHERE treasure_artifact_bonus IS NULL')

    if 'grade_commerce' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN grade_commerce INTEGER DEFAULT 0')
        c.execute('UPDATE users SET grade_commerce = 0 WHERE grade_commerce IS NULL')
    if 'commerce_bonus' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN commerce_bonus REAL DEFAULT 1.00')
        c.execute('UPDATE users SET commerce_bonus = 1.00 WHERE commerce_bonus IS NULL')

    if 'grade_navigation' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN grade_navigation INTEGER DEFAULT 0')
        c.execute('UPDATE users SET grade_navigation = 0 WHERE grade_navigation IS NULL')
    if 'navigation_price_bonus' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN navigation_price_bonus REAL DEFAULT 0.00')
        c.execute('UPDATE users SET navigation_price_bonus = 0.00 WHERE navigation_price_bonus IS NULL')
    if 'navigation_time_bonus' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN navigation_time_bonus INTEGER DEFAULT 0')
        c.execute('UPDATE users SET navigation_time_bonus = 0 WHERE navigation_time_bonus IS NULL')

    if 'grade_token' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN grade_token INTEGER DEFAULT 0')
        c.execute('UPDATE users SET grade_token = 0 WHERE grade_token IS NULL')
    if 'token_bonus' not in columns:
        c.execute('ALTER TABLE users ADD COLUMN token_bonus INTEGER DEFAULT 0')
        c.execute('UPDATE users SET token_bonus = 0 WHERE token_bonus IS NULL')

    conn.commit()
    conn.close()


# Add a user with hashed password
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
              "p_number,"
              "trade_token,"
              "battle_played,"
              "grade_damage,"
              "damage_bonus,"
              "grade_resistance,"
              "resistance_bonus,"
              "grade_agility,"
              "agility_bonus,"
              "grade_treasure,"
              "treasure_money_bonus,"
              "treasure_resource_bonus,"
              "treasure_artifact_bonus,"
              "grade_commerce,"
              "commerce_bonus,"
              "grade_navigation,"
              "navigation_price_bonus,"
              "navigation_time_bonus,"
              "grade_token,"
              "token_bonus)"
              "VALUES ("
              "?, ?, ?, ?, ?, ?, ?, ?, ?, ?,"
              "?, ?, ?, ?, ?, ?, ?, ?, ?, ?,"
              "?, ?, ?, ?, ?, ?, ?, ?, ?, ?,"
              "?, ?, ?)",
              (
                  username, hashed_password, 100, '', '', 10, 0, 0, 0.00, 0,
                  0, 0, 0.5, -0.0004, 0, 0, 0, 1.00, 0, 1.00,
                  0, 0.10, 0, 1.00, 1.00, 0.0001, 0, 1.00, 0, 1.00,
                  0, 0, 0))
    conn.commit()
    conn.close()


# DEPRECATED BUT MAYBE USEFUL
# def reset_profile(username):
#     conn = sqlite3.connect('user/users.db')
#     c = conn.cursor()
#     c.execute("UPDATE users SET money=?,"
#               "ship_list=?,"
#               "enemy_list=?,"
#               "fleet_size=?,"
#               "win=?,"
#               "loose=?,"
#               "ratio_WL=?,"
#               "money_win=?,"
#               "money_spent=?,"
#               "grade=?,"
#               "p_letter=?,"
#               "p_number=?,"
#               "WHERE username=?", (100, '', '', 10, 0, 0, 0.00, 0, 0, 0, 0.5, -0.0004, username))  # Réinitialiser les paramètres nécessaires
#     conn.commit()
#
#     user = get_user(username)
#     st.session_state.money = user[2]
#     st.session_state.ship_list = user[3]
#     st.session_state.enemy_list = user[4]
#     st.session_state.fleet_size = user[5]
#     st.session_state.win = user[6]
#     st.session_state.loose = user[7]
#     st.session_state.ratio_WL = user[8]
#     st.session_state.money_win = user[9]
#     st.session_state.money_spent = user[10]
#     st.session_state.grade = user[11]
#     st.session_state.p_letter = user[12]
#     st.session_state.p_number = user[13]
#
#     conn.close()


# Hasher password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


# Check password
def check_password(username, password):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    if result:
        stored_hash = result[0]
        return checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
    else:
        return False


# Retrieve user information
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


# Update money
def update_money(username, amount, context="win"):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    if context == 'sender':
        c.execute(""
                  "UPDATE users SET money=money - ?,"
                  "money_spent=money_spent + ? "
                  "WHERE username=?",
                  (amount, amount, username))

    elif context == "receiver" or context == "win":
        c.execute(""
                  "UPDATE users SET money=money + ?,"
                  "money_win=money_win + ? "
                  "WHERE username=?",
                  (amount, amount, username))

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


# Delete user
def delete_user(username):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()


# Add shuttles
def add_ship(username, new_ship, add_to, fight=False, price=None):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    if add_to == "player":  # For player
        c.execute("SELECT ship_list FROM users WHERE username=?", (username,))
        current_ship_list_json = c.fetchone()[0]
        current_ship_list = json.loads(current_ship_list_json) if current_ship_list_json else []
        current_ship_list.append(new_ship)
        updated_ship_list_json = json.dumps(current_ship_list)

        if fight is False:  # Not in fight, e.g: buy shuttles
            c.execute(""
                      "UPDATE users SET ship_list=?,"
                      "money=money - ?,"
                      "money_spent=money_spent + ? "
                      "WHERE username=?",
                      (updated_ship_list_json, price, price, username))
            conn.commit()

            user = get_user(username)
            st.session_state.money = user[2]
            st.session_state.ship_list = user[3]
            st.session_state.money_spent = user[10]

        elif fight is True:  # During fight
            c.execute("""
                UPDATE users 
                SET 
                    ship_list = ? WHERE username = ?
            """, (updated_ship_list_json, username))
            conn.commit()

            user = get_user(username)
            st.session_state.ship_list = user[3]

    elif add_to == "enemies":  # For enemies
        c.execute("SELECT enemy_list FROM users WHERE username=?", (username,))
        current_enemy_list_json = c.fetchone()[0]
        current_enemy_list = json.loads(current_enemy_list_json) if current_enemy_list_json else []
        current_enemy_list.append(new_ship)
        updated_enemy_list_json = json.dumps(current_enemy_list)

        c.execute("UPDATE users SET enemy_list=? WHERE username=?",
                  (updated_enemy_list_json, username))
        conn.commit()

        user = get_user(username)
        st.session_state.enemy_list = user[4]

    conn.close()


# Sell shuttles (can be compiled with remove_ship)
def sell_ship(username, ship):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    c.execute("SELECT ship_list FROM users WHERE username=?", (username,))
    current_ship_list_json = c.fetchone()[0]
    current_ship_list = json.loads(current_ship_list_json)

    if ship in current_ship_list:
        money_earned = get_cost(ship)
        current_ship_list.remove(ship)
    updated_ship_list_json = json.dumps(current_ship_list)

    c.execute(""
              "UPDATE users SET ship_list=?,"
              "money=money + ?,"
              "money_win=money_win + ? "
              "WHERE username=?",
              (updated_ship_list_json, money_earned, money_earned, username))
    conn.commit()

    user = get_user(username)
    st.session_state.money = user[2]
    st.session_state.ship_list = user[3]
    st.session_state.money_win = user[9]

    conn.close()


# Remove ship
def remove_ship(username, ship, remove_from, fight=False):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    if remove_from == "player":  # For player
        c.execute("SELECT ship_list FROM users WHERE username=?", (username,))
        current_ship_list_json = c.fetchone()[0]
        current_ship_list = json.loads(current_ship_list_json)

        if ship in current_ship_list:
            current_ship_list.remove(ship)
        updated_ship_list_json = json.dumps(current_ship_list)

        if fight is False:  # For update during battle
            c.execute("UPDATE users SET ship_list=? WHERE username=?",
                      (updated_ship_list_json, username))
            conn.commit()

            user = get_user(username)
            st.session_state.ship_list = user[3]

        elif fight is True:  # During battle win
            c.execute("""
                UPDATE users SET ship_list=?,
                loose=loose + ?, 
                ratio_WL = CASE WHEN win > 0.00 THEN win / (loose + ?) ELSE 0.00 / (loose + ?) END 
                WHERE username=?""",
                      (updated_ship_list_json, 1, 1.00, 1.00, username))
            conn.commit()

    elif remove_from == "enemies":  # For enemies
        c.execute("SELECT enemy_list FROM users WHERE username=?", (username,))
        current_enemy_list_json = c.fetchone()[0]
        current_enemy_list = json.loads(current_enemy_list_json)

        if ship in current_enemy_list:
            current_enemy_list.remove(ship)
        updated_enemy_list_json = json.dumps(current_enemy_list)

        if fight is True:  # For battle loose
            c.execute(""
                      "UPDATE users SET enemy_list=?,"
                      "win = win + ?,"
                      "ratio_WL = CASE WHEN loose > 0.00 THEN (win + ?) / loose ELSE win + ? END "
                      "WHERE username=?",
                      (updated_enemy_list_json, 1, 1.00, 1.00, username))

        elif fight is False:  # During battle
            c.execute(""
                      "UPDATE users SET enemy_list=? WHERE username=?",
                      (updated_enemy_list_json, username))
        conn.commit()

    conn.close()


# Upgrade fleet size
def upgrade_fleet_size(username, amount):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()
    c.execute(""
              "UPDATE users SET fleet_size=fleet_size + ?,"
              "money=money - ?,"
              "money_spent=money_spent + ? "
              "WHERE username=?",
              (5, amount, amount, username))
    conn.commit()
    conn.close()


# Trade token
def trade_token(username, number_battle):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    c.execute("""
        UPDATE users SET battle_played = CASE WHEN battle_played + ? >= 100 THEN 0 ELSE battle_played + ? END,
        trade_token = CASE WHEN battle_played + ? >= 100 THEN trade_token + 1 ELSE trade_token END 
        WHERE username=?
    """, (number_battle, number_battle, number_battle, username))
    conn.commit()
    conn.close()


# Grade commander
def upgrade_grade_commander(username, amount, p_letter, p_number):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    decimal.getcontext().prec = 6
    p_letter = decimal.Decimal(p_letter)
    p_number = decimal.Decimal(p_number)
    new_p_letter = round(p_letter + decimal.Decimal('-0.1'), 1)
    new_p_number = round(p_number + decimal.Decimal('0.0001'), 4)

    c.execute("""
        UPDATE users SET money = money - ?,
        money_spent = money_spent + ?, 
        grade = grade + ?, 
        p_letter = ?, 
        p_number = ? 
        WHERE username = ?""",
              (amount, amount, 1, float(new_p_letter), float(new_p_number), username))

    conn.commit()
    conn.close()


# Upgrade damage
def upgrade_damage(username, amount, damage_bonus):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    decimal.getcontext().prec = 4
    damage_bonus = decimal.Decimal(damage_bonus)
    new_damage_bonus = round(damage_bonus + decimal.Decimal('0.025'), 3)

    c.execute("""
        UPDATE users SET money = money - ?,
        money_spent = money_spent + ?,
        grade_damage = grade_damage + ?,
        damage_bonus = ?
        WHERE username = ?""",
              (amount, amount, 1, float(new_damage_bonus), username))

    conn.commit()
    conn.close()


# Upgrade resistance
def upgrade_resistance(username, amount, resistance_bonus):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    decimal.getcontext().prec = 4
    resistance_bonus = decimal.Decimal(resistance_bonus)
    new_resistance_bonus = round(resistance_bonus + decimal.Decimal('-0.025'), 3)

    c.execute("""
        UPDATE users SET money = money - ?,
        money_spent = money_spent + ?,
        grade_resistance = grade_resistance + ?,
        resistance_bonus = ? 
        WHERE username = ?""",
              (amount, amount, 1, float(new_resistance_bonus), username))

    conn.commit()
    conn.close()


# Upgrade agility
def upgrade_agility(username, amount, agility_bonus):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    decimal.getcontext().prec = 4
    agility_bonus = decimal.Decimal(agility_bonus)
    new_agility_bonus = round(agility_bonus + decimal.Decimal('0.09'), 3)

    c.execute("""
        UPDATE users SET money = money - ?,
        money_spent = money_spent + ?,
        grade_agility = grade_agility + ?,
        agility_bonus = ? 
        WHERE username = ?""",
              (amount, amount, 1, float(new_agility_bonus), username))

    conn.commit()
    conn.close()


# Upgrade treasure
def upgrade_treasure(username, amount, treasure_money_bonus, treasure_resource_bonus, treasure_artifact_bonus):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    decimal.getcontext().prec = 4
    treasure_money_bonus = decimal.Decimal(treasure_money_bonus)
    new_treasure_money_bonus = round(treasure_money_bonus + decimal.Decimal('0.05'), 3)

    decimal.getcontext().prec = 4
    treasure_resource_bonus = decimal.Decimal(treasure_resource_bonus)
    new_treasure_resource_bonus = round(treasure_resource_bonus + decimal.Decimal('0.025'), 3)

    decimal.getcontext().prec = 6
    treasure_artifact_bonus = decimal.Decimal(treasure_artifact_bonus)
    new_treasure_artifact_bonus = round(treasure_artifact_bonus + decimal.Decimal('0.00015'), 5)

    c.execute("""
        UPDATE users SET money = money - ?,
        money_spent = money_spent + ?,
        grade_treasure = grade_treasure + ?, 
        treasure_money_bonus = ?, 
        treasure_resource_bonus = ?, 
        treasure_artifact_bonus = ? 
        WHERE username = ?""",
              (amount, amount, 1, float(new_treasure_money_bonus), float(new_treasure_resource_bonus),
               float(new_treasure_artifact_bonus), username))

    conn.commit()
    conn.close()


# Upgrade commerce
def upgrade_commerce(username, amount, commerce_bonus):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    decimal.getcontext().prec = 4
    commerce_bonus = decimal.Decimal(commerce_bonus)
    new_commerce_bonus = round(commerce_bonus + decimal.Decimal('-0.05'), 3)

    c.execute("""
        UPDATE users SET money = money - ?,
        money_spent = money_spent + ?,
        grade_commerce = grade_commerce + ?,
        commerce_bonus = ? 
        WHERE username = ?""",
              (amount, amount, 1, float(new_commerce_bonus), username))

    conn.commit()
    conn.close()


# Upgrade navigation
def upgrade_navigation(username, amount, navigation_price_bonus, navigation_time_bonus):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    decimal.getcontext().prec = 4
    navigation_price_bonus = decimal.Decimal(navigation_price_bonus)
    new_navigation_price_bonus = round(navigation_price_bonus + decimal.Decimal('-0.025'), 3)

    c.execute("""
        UPDATE users SET money = money - ?,
        money_spent = money_spent + ?,
        grade_navigation = grade_navigation + ?,
        navigation_price_bonus = ?,
        navigation_time_bonus = navigation_time_bonus + ?
        WHERE username = ?""",
              (amount, amount, 1, float(new_navigation_price_bonus), 2, username))

    conn.commit()
    conn.close()


# Upgrade token
def upgrade_token(username, amount, token_bonus):
    conn = sqlite3.connect('user/users.db')
    c = conn.cursor()

    c.execute("""
        UPDATE users SET money = money - ?,
        money_spent = money_spent + ?,
        grade_token = grade_token + ?,
        token_bonus = token_bonus + ?
        WHERE username = ?""",
              (amount, amount, 1, 1, username))

    conn.commit()
    conn.close()
