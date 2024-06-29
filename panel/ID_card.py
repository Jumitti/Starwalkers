import json

import pandas as pd
import streamlit as st

from starwalkers import sql
from starwalkers.func import get_d_sym, get_cost


# Display Commander Grade with stars
def display_stars(grade):
    full_star = '⭐'
    empty_star = '☆'
    max_stars = 5
    stars = full_star * grade + empty_star * (max_stars - grade)
    return stars


# Reformatting money
def format_money(value):
    if value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T"
    elif value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.2f}K"
    else:
        return f"{value}"


def ID_card(username, display="community_info"):
    user_info = sql.get_user(username)  # Some elements are not necessary
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

    if user_info:
        st.header(f"🧑🏽‍🚀 Captain {username}'s ID Card {display_stars(grade)}")

        # Resources (money)
        st.subheader("💲 Resources")
        colres1, colres2, colres3, colres4 = st.columns(4, gap="small")
        colres1.metric(f"💲 Money", f"{format_money(money)}$")
        colres2.metric(f"💵 Earned", f"{format_money(money_win)}$")
        colres3.metric(f"🏷️ Spent", f"{format_money(money_spent)}$")
        colres4.metric(f"🪙 Trade token", f"{trade_token}")
        if display == "player_info":
            colres4.progress(battle_played)

        # Space fleet
        st.subheader("🚀 Space Fleet")
        with st.expander(f"Space fleet capacity: {fleet_size} ships", expanded=True):
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

        # Stats battles
        st.subheader("⚔️ Battles")
        colbattle1, colbattle2, colbattle3 = st.columns(3, gap="small")
        colbattle1.metric(f"🏆 Win", f"{win}")
        colbattle2.metric(f"💥 Loose", f"{loose}")
        colbattle3.metric(f"⚖️ Win/Loss Ratio", f"{ratio_WL}")

        # Skills and trophies
        st.subheader("🏆 Skills and trophies")
        if display == "player_info":
            colsu1, colsu2, colsu3 = st.columns(3, gap="small")
            colsu1.metric(f"⭐ Galactic\n\nCommander", grade, delta="" if grade < 5 else "MAX", help="Improve purchased shuttles but increases the price")
            colsu2.metric(f"🚀 Armada\n\nExpansion", fleet_size)
            colsu3.metric(f"🧭 Astral\n\nNavigator", grade_navigation, delta="" if grade_navigation < 10 else "MAX", help="Reduces the cost of Open Space and speeds up the obtaining of resources")

            colsu4, colsu5, colsu6 = st.columns(3, gap="small")
            colsu4.metric(f"💥 Stellar\n\nStrike", grade_damage, delta="" if grade_damage < 10 else "MAX", help="Increases damage inflict")
            colsu5.metric(f"🛡️ Cosmic\n\nFortitude", grade_resistance, delta="" if grade_resistance < 10 else "MAX", help="Reduces damage taken")
            colsu6.metric(f"🪶 Celestial\n\nAgility", grade_agility, delta="" if grade_agility < 10 else "MAX", help="Increases chances of escape")

            colsu7, colsu8, colsu9 = st.columns(3, gap="small")
            colsu7.metric(f"🛒 Interstellar\n\nCommerce", grade_commerce, delta="" if grade_commerce < 10 else "MAX", help="Reduces shuttle price")
            colsu8.metric(f"💎 Treasure\n\nHunter", grade_treasure, delta="" if grade_treasure < 10 else "MAX", help="Increases money, resources and artifacts earned")
            colsu9.metric(f"⚡ Token\n\nAccelerator", grade_token, delta="" if grade_token < 10 else "MAX", help="Accelerate Trade Token generation")

        return df, value_list
