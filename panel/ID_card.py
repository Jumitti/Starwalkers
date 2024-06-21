import json

import pandas as pd
import streamlit as st

from starwalkers import sql
from starwalkers.func import get_d_sym, get_cost


def display_stars(grade):
    full_star = '⭐'  # Emoji pour étoile pleine
    empty_star = '☆'  # Emoji pour étoile vide
    max_stars = 5  # Nombre maximum d'étoiles à afficher

    stars = full_star * grade + empty_star * (max_stars - grade)
    return stars


def ID_card(username, display="community_info"):
    user_info = sql.get_user(username)
    if user_info:
        st.header(f"🧑🏽‍🚀 Captain {user_info[0]}'s ID Card {display_stars(user_info[11])}")

        st.subheader("Resources")
        colres1, colres2, colres3, colres4 = st.columns(4, gap="small")
        colres1.metric(f"💲 Money", f"{user_info[2]}$")
        colres2.metric(f"💵 Money earned", f"{user_info[9]}$")
        colres3.metric(f"🏷️ Money spent", f"{user_info[10]}$")
        colres4.metric(f"🪙 Trade token", f"{user_info[14]}")
        colres4.progress(user_info[15])
        colres4.write(user_info[15])

        st.subheader("Space Fleet")
        with st.expander(f"🚀 Space fleet capacity: {user_info[5]} ships", expanded=True):
            ship_data = []
            value_list = []
            if len(user_info[3]) > 2:
                for ship in json.loads(user_info[3]):
                    ship_data.append(
                        {"Ship": ship, "Value": get_d_sym(get_cost(ship)).replace('$', '💲'),
                         "Sell": get_cost(ship)})
                    if get_d_sym(get_cost(ship)) not in value_list and display == "player_info":
                        value_list.append(get_d_sym(get_cost(ship)))
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
        colbattle1.metric(f"🏆 Win", f"{user_info[6]}")
        colbattle2.metric(f"💥 Loose", f"{user_info[7]}")
        colbattle3.metric(f"⚖️ Win/Loss Ratio", f"{user_info[8]}")

        return df, value_list
