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

    st.header("🏪 Store")

    # Open case
    colopencase1, colopencase2 = st.columns([2, 1], gap="small")
    open_case = colopencase1.slider(
        "**📦 ➡ 🚀 Buy shuttles**",
        value=int(min(fleet_size - len(df), money / 10) / 2) if min(fleet_size - len(df), money / 10) > 0 else 1, step=1,
        min_value=0, max_value=int(min(fleet_size - len(df), money / 10) if min(fleet_size - len(df), money / 10) >= 1 else 1),
        disabled=True if money < 10 or len(df) >= fleet_size else False)

    colopencase2.markdown("")
    if colopencase2.button(f"Open {open_case} case(s) for {open_case * 10}$",
                           disabled=True if money < 10 or len(df) >= fleet_size else False):
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

        colsu1.metric(f"⭐ Grade", grade, delta=1 if grade < 5 else "MAX")
        if grade < 5:
            if colsu1.button(
                    f"⬆️ Upgrade\n\n{upgrade(grade)}$",
                    disabled=True if money < upgrade(grade) and grade < 5 else False):
                sql.upgrade_grade(username, upgrade(grade), p_letter, p_number)
                time.sleep(0.75) & st.rerun()

        colsu2.metric(f"🚀 Fleet size", fleet_size, delta=5)
        if colsu2.button(
                f"⬆️ Upgrade\n\n{upgrade_fleet(fleet_size)}$",
                disabled=True if money < upgrade_fleet(fleet_size) else False):
            sql.upgrade_fleet_size(username, upgrade_fleet(fleet_size))
            time.sleep(0.75) & st.rerun()
