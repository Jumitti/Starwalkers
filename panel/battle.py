import json
import random
import time

import pandas as pd
import streamlit as st

from starwalkers import sql
from starwalkers.func import roll, get_d_sym, get_cost


def battle(username, df):
    user_info = sql.get_user(username)
    money = user_info[2]
    ship_list = user_info[3]
    enemy_list = user_info[4]
    fleet_size = user_info[5]
    win = user_info[6]
    loose = user_info[7]
    ratio_WL = user_info[8]
    money_win = user_info[9]
    money_spent = user_info[10]
    grade = user_info[11]
    p_letter = user_info[12]
    p_number = user_info[13]
    trade_token = user_info[14]
    battle_played = user_info[15]
    grade_damage = user_info[16]
    damage_bonus = user_info[17]
    grade_resistance = user_info[18]
    resistance_bonus = user_info[19]
    grade_agility = user_info[20]
    agility_bonus = user_info[21]
    grade_treasure = user_info[22]
    treasure_money_bonus = user_info[23]
    treasure_resource_bonus = user_info[24]
    treasure_artifact_bonus = user_info[25]
    grade_commerce = user_info[26]
    commerce_bonus = user_info[27]
    grade_navigation = user_info[28]
    navigation_price_bonus = user_info[29]
    navigation_time_bonus = user_info[30]
    grade_token = user_info[31]
    token_bonus = user_info[32]

    st.header("⚔️ Space war")
    colwar1, colwar2 = st.columns(2, gap="small")

    if 'selected_ships_enemy' not in st.session_state or not st.session_state.selected_ships_enemy:
        st.session_state.selected_ships_enemy = []

    if enemy_list:
        enemy_data = []
        colfight1, colfight2 = st.columns(2, gap="small")
        for ship in json.loads(enemy_list):
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
            colselectfight1, colselectfight2 = st.columns([2, 1], gap="small")
            shuttles_for_fight = colselectfight1.multiselect("Select shuttles to fight", df["Ship"].tolist(),
                                                             label_visibility="collapsed",
                                                             placeholder="Select shuttles to fight (max:4)",
                                                             max_selections=4, default=df["Ship"].tolist()[:4])
            value_player = int(sum(get_cost(ship) for ship in shuttles_for_fight) * random.uniform(1, damage_bonus))
            value_enemies = int(sum(get_cost(ship) for ship in styled_df_enemy["Ship"]))
            # colselectfight2.write(value_enemies)
            # colselectfight2.write(value_player)
            if colselectfight2.button(f"FIGHT !"):
                damage = random.randint(0, 100)
                if value_player > value_enemies:
                    sql.trade_token(username, len(styled_df_enemy['Ship']))
                    money_win = int((sum(get_cost(ship) for ship in styled_df_enemy['Ship']) // 1.5) * random.uniform(1, treasure_money_bonus))
                    sql.update_money(username, money_win if money_win != 0 else 1, context="win")
                    for ship in styled_df_enemy['Ship']:
                        sql.remove_ship(username, ship, "enemies")
                    st.session_state.pop('selected_ships_enemy', None)
                    for ship in shuttles_for_fight:
                        player_let, player_int = ship.split("-")
                        new_number = int(player_int) - (int((damage * random.uniform(1, resistance_bonus))) // len(shuttles_for_fight))
                        if new_number >= 0:
                            update_ship = roll(letter=player_let, number=new_number)
                            sql.add_ship(username, update_ship, "player", fight=True)
                            sql.remove_ship(username, ship, "player")
                        else:
                            sql.remove_ship(username, ship, "player", fight=True)
                            st.toast(f"💥 You loose {ship} in the battle.")
                    st.toast(f'🏆 You win the battle. 💲 Money win: {money_win}$. 🛠️ Damage: {damage}.')
                    time.sleep(2) & st.rerun()

                if value_player <= value_enemies:
                    sql.trade_token(username, len(shuttles_for_fight))
                    for ship in shuttles_for_fight:
                        sql.remove_ship(username, ship, "player", fight=True)
                    for ship in styled_df_enemy['Ship']:
                        enemy_let, enemy_int = ship.split("-")
                        new_number = int(enemy_int) - (int((damage / random.uniform(1, resistance_bonus))) // len(styled_df_enemy))
                        if new_number >= 0:
                            update_ship = roll(letter=enemy_let, number=new_number)
                            sql.add_ship(username, update_ship, "enemies", fight=True)
                            sql.remove_ship(username, ship, "enemies")
                        else:
                            sql.remove_ship(username, ship, "enemies", fight=True)
                    st.session_state.pop('selected_ships_enemy', None)
                    st.toast(
                        f'💥 You lost the battle and {" ".join(ship for ship in shuttles_for_fight)} shuttle(s)')
                    time.sleep(0.75) & st.rerun()

            if colwar2.button("🏃‍♂️Leave fight"):
                if random.random() <= agility_bonus:
                    for ship in json.loads(enemy_list):
                        sql.remove_ship(username, ship, "enemies")
                    st.session_state.pop('selected_ships_enemy', None)
                    st.toast("🏃‍♂️You left the battle")
                    time.sleep(0.25) & st.rerun()
                else:
                    st.toast("✊🏽 We will not run away from this battle!")

        elif df.empty:
            st.warning("You don't have shuttles")

    if colwar1.button("💥 Look for enemies !", disabled=True if len(enemy_list) > 2 else False):
        for _ in range(random.randint(1, 10)):
            ship = roll(proba_letter=p_letter, proba_number=p_number)
            sql.add_ship(username, ship, "enemies")
        st.toast("⚔️ The enemies enter the battles")
        time.sleep(0.75) & st.rerun()