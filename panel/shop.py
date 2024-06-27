import json
import time

import streamlit as st

from starwalkers import sql
from starwalkers.func import roll, get_d_sym, get_cost, upgrade_fleet, upgrade


def shop(username, df, value_list):
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

    st.header("🏪 Store")

    # Open case
    colopencase1, colopencase2 = st.columns([2, 1], gap="small")
    open_case = colopencase1.slider(
        "**📦 ➡ 🚀 Buy shuttles**",
        value=int(min(fleet_size - len(df), money / ((10 + 10 * grade) * commerce_bonus)) / 2) if min(fleet_size - len(df), money / ((10 + 10 * grade) * commerce_bonus)) > 0 else 1, step=1,
        min_value=0, max_value=int(min(fleet_size - len(df), money / ((10 + 10 * grade) * commerce_bonus)) if min(fleet_size - len(df), money / ((10 + 10 * grade) * commerce_bonus)) >= 1 else 1),
        disabled=True if money < ((10 + 10 * grade) * commerce_bonus) or len(df) >= fleet_size else False)

    colopencase2.markdown("")
    if colopencase2.button(f"Open {open_case} case(s) for {open_case * ((10 + 10 * grade) * commerce_bonus)}$",
                           disabled=True if money < ((10 + 10 * grade) * commerce_bonus) or len(df) >= fleet_size else False):
        for i in range(0, open_case):
            ship = roll(proba_letter=p_letter, proba_number=p_number)
            sql.add_ship(username, ship, price=10, add_to="player")
        st.toast("🚀 New shuttle(s) in your fleet!")
        time.sleep(0.75) & st.rerun()

    # Sell ships
    with st.expander("**🚀 ➡ 💲 Sell shuttle**", expanded=True):
        colsellship1, colsellship2 = st.columns([2, 1], gap="small")

        if not df.empty:
            sell = colsellship1.multiselect("Sell ship", df["Ship"].tolist(), label_visibility="collapsed",
                                            placeholder="Select shuttles for sale")
            price = sum(get_cost(ship) for ship in sell)

            if colsellship2.button(f"Sell selection for {price}$"):
                for ship in sell:
                    sql.sell_ship(username, ship)

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
                            f"{elements_safe} ({sum(get_cost(ship) for ship in json.loads(ship_list) if get_d_sym(get_cost(ship)) == item)}$)",
                            key=f"value_{item}"):
                        for ship in json.loads(ship_list):
                            if get_d_sym(get_cost(ship)) == item:
                                sql.sell_ship(username, ship)
                        time.sleep(0.75) & st.rerun()
        else:
            st.warning("You don't have any shuttles to sell.")

    # Skills and upgrade
    with st.expander("✨ Skills and upgrade", expanded=True):
        colsu1, colsu2, colsu3 = st.columns(3, gap="small")

        colsu1.metric(f"⭐ Galactic Commander", grade, delta=1 if grade < 5 else "MAX")
        if grade < 5:
            if colsu1.button(
                    f"⬆️ Upgrade\n\n{upgrade(grade, 0.4, 1000)}$",
                    disabled=True if money < upgrade(grade, 0.4, 1000) and grade < 5 else False, key="captain"):
                sql.upgrade_grade_commander(username, upgrade(grade, 0.4, 1000), p_letter, p_number)
                time.sleep(0.75) & st.rerun()

        colsu2.metric(f"🚀 Armada Expansion", fleet_size, delta=5)
        if colsu2.button(
                f"⬆️ Upgrade\n\n{upgrade_fleet(fleet_size)}$",
                disabled=True if money < upgrade_fleet(fleet_size) else False):
            sql.upgrade_fleet_size(username, upgrade_fleet(fleet_size))
            time.sleep(0.75) & st.rerun()

        colsu3.metric(f"🧭 Astral Navigator", grade_navigation, delta="-2.5% $ | -2 min" if grade_navigation < 10 else "Max", help='Hello')
        if grade_navigation < 10:
            if colsu3.button(
                    f"⬆️ Upgrade\n\n{upgrade(grade_navigation, 0.3, 500)}$",
                    disabled=True if money < upgrade(grade_navigation, 0.3, 500) and grade_navigation < 10 else False,
                    key="navigation"):
                sql.upgrade_navigation(username, upgrade(grade_navigation, 0.3, 500), navigation_price_bonus, navigation_time_bonus)
                time.sleep(0.75) & st.rerun()

        colsu4, colsu5, colsu6 = st.columns(3, gap="small")

        colsu4.metric(f"💥 Stellar Strike", grade_damage, delta="+2.5%" if grade_damage < 10 else "MAX")
        if grade_damage < 10:
            if colsu4.button(
                    f"⬆️ Upgrade\n\n{upgrade(grade_damage, 0.3, 1000)}$",
                    disabled=True if money < upgrade(grade_damage, 0.3, 1000) and grade_damage < 10 else False, key="damage"):
                sql.upgrade_damage(username, upgrade(grade_damage, 0.3, 1000), damage_bonus)
                time.sleep(0.75) & st.rerun()

        colsu5.metric(f"🛡️ Cosmic Fortitude", grade_resistance, delta="-2.5%" if grade_resistance < 10 else "MAX")
        if grade_resistance < 10:
            if colsu5.button(
                    f"⬆️ Upgrade\n\n{upgrade(grade_resistance, 0.3, 1000)}$",
                    disabled=True if money < upgrade(grade_resistance, 0.3, 1000) and grade_resistance < 10 else False, key="resistance"):
                sql.upgrade_resistance(username, upgrade(grade_resistance, 0.3, 1000), resistance_bonus)
                time.sleep(0.75) & st.rerun()

        colsu6.metric(f"🪶 Celestial Agility", grade_agility, delta="+9%" if grade_agility < 10 else "MAX")
        if colsu6.button(
                f"⬆️ Upgrade\n\n{upgrade(grade_agility, 0.3, 250)}$",
                disabled=True if money < upgrade(grade_agility, 0.3, 250) and grade_agility < 10 else False, key="agility"):
            sql.upgrade_agility(username, upgrade(grade_agility, 0.3, 250), agility_bonus)
            time.sleep(0.75) & st.rerun()

        colsu7, colsu8, colsu9 = st.columns(3, gap="small")

        colsu7.metric(f"🛒 Interstellar Commerce", grade_commerce, delta="-5%" if grade_commerce < 10 else "MAX")
        if colsu7.button(
                f"⬆️ Upgrade\n\n{upgrade(grade_commerce, 0.4, 500)}$",
                disabled=True if money < upgrade(grade_commerce, 0.4, 500) and grade_commerce < 10 else False,
                key="commerce"):
            sql.upgrade_commerce(username, upgrade(grade_commerce, 0.4, 500), commerce_bonus)
            time.sleep(0.75) & st.rerun()

        colsu8.metric(f"💎 Treasure Hunter", grade_treasure, delta="M:5%|R:2.5%|A:1%" if grade_treasure < 10 else "MAX")
        if colsu8.button(
                f"⬆️ Upgrade\n\n{upgrade(grade_treasure, 0.3, 1500)}$",
                disabled=True if money < upgrade(grade_treasure, 0.3, 1500) and grade_treasure < 10 else False,
                key="treasure"):
            sql.upgrade_treasure(username, upgrade(grade_treasure, 0.3, 1500), treasure_money_bonus,
                                 treasure_resource_bonus, treasure_artifact_bonus)
            time.sleep(0.75) & st.rerun()

        colsu9.metric(f"⚡ Token Accelerator", grade_token, delta=1 if grade_token < 10 else "MAX")
        if colsu9.button(
                f"⬆️ Upgrade\n\n{upgrade(grade_token, 0.3, 250)}$",
                disabled=True if money < upgrade(grade_token, 0.3, 250) and grade_token < 10 else False,
                key="token"):
            sql.upgrade_token(username, upgrade(grade_token, 0.3, 250), token_bonus)
            time.sleep(0.75) & st.rerun()
