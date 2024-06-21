import json

import pandas as pd
import streamlit as st

from starwalkers import sql
from starwalkers.func import get_d_sym, get_cost


def display_stars(grade):
    full_star = '⭐'
    empty_star = '☆'
    max_stars = 5

    stars = full_star * grade + empty_star * (max_stars - grade)
    return stars


def ID_card(username, display="community_info"):
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
    
    if user_info:
        st.header(f"🧑🏽‍🚀 Captain {username}'s ID Card {display_stars(grade)}")

        st.subheader("Resources")
        colres1, colres2, colres3, colres4 = st.columns(4, gap="small")
        colres1.metric(f"💲 Money", f"{money}$")
        colres2.metric(f"💵 Money earned", f"{money_win}$")
        colres3.metric(f"🏷️ Money spent", f"{user_info[10]}$")
        colres4.metric(f"🪙 Trade token", f"{trade_token}")
        if display == "player_info":
            colres4.progress(battle_played)

        st.subheader("Space Fleet")
        with st.expander(f"🚀 Space fleet capacity: {fleet_size} ships", expanded=True):
            ship_data = []
            value_list = []
            if len(ship_list) > 2:
                for ship in json.loads(ship_list):
                    ship_entry = {"Ship": ship,
                                  "Value": get_d_sym(get_cost(ship)).replace('$', '💲')}
                    if display == "player_info":
                        ship_entry["Sell"] = get_cost(ship)
                        if get_d_sym(get_cost(ship)) not in value_list:
                            value_list.append(get_d_sym(get_cost(ship)))
                    ship_data.append(ship_entry)
                if ship_data:
                    df = pd.DataFrame(ship_data).sort_values(by="Sell" if display == "player_info" else "Value", ascending=False)
                    styled_df = df.style.set_table_styles(
                        [
                            {'selector': 'th', 'props': [('max-width', '150px')]},
                            {'selector': 'td', 'props': [('max-width', '150px')]}
                        ]
                    ).set_properties(**{'text-align': 'left'})
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
            else:
                df = pd.DataFrame()

        st.subheader("Battles")
        colbattle1, colbattle2, colbattle3 = st.columns(3, gap="small")
        colbattle1.metric(f"🏆 Win", f"{win}")
        colbattle2.metric(f"💥 Loose", f"{loose}")
        colbattle3.metric(f"⚖️ Win/Loss Ratio", f"{ratio_WL}")

        return df, value_list
