import json
import random
import sys
import time

import pandas as pd
import streamlit as st

from starwalkers import sql
from starwalkers.func import roll, get_d_sym, get_cost, upgrade_fleet
from panel import ID_card, shop

import logging


def community(username):
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

    st.header("👨🏼‍🚀 Community")
    usernames = sql.get_user()
    default_user = username if username in sql.get_user() else usernames[0]
    colcom1, colcom2 = st.columns([2, 1], gap="small")
    selected_username = colcom1.selectbox('👨🏽‍🚀 See a Captain', usernames, placeholder="Choose a captain")
    if selected_username:
        colcom2.markdown("")
        colcom2.markdown("")
        if colcom2.toggle(f"{selected_username} ID card"):
            ID_card.ID_card(selected_username)

            colsm1, colsm2 = st.columns([2, 1], gap="small")
            send_money = colsm1.slider("💸 Send money", step=1, min_value=0,
                                       max_value=money if money > 0 else 1,
                                       disabled=True if money < 1 or selected_username == username else False)

            colsm2.markdown("")
            if colsm2.button(f"Send {send_money}$ to {selected_username}",
                             disabled=True if money < 1 or selected_username == username or trade_token < 1 else False):
                sql.update_money(selected_username, send_money, context="receiver")
                sql.update_money(username, send_money, context="sender")
                st.toast(f"💸 {send_money}$ sends to {selected_username}")
                time.sleep(0.75) & st.rerun()