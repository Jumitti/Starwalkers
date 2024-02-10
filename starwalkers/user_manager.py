import json

save_tree_choice = {}

def save_json(chat_id,
              username=None,
              money=None,
              user_case=None,
              ship_list=None,
              enemy_list=None,
              win=None,
              loose=None,
              language=None,
              fleet_size=None,
              godmode=None,
              money_win=None,
              money_spent=None,
              case_purchased=None,
              case_open=None):
    try:
        with open(f"user/{chat_id}.json", "r") as read_file:
            ID_info = json.load(read_file)
    except FileNotFoundError:
        ID_info = {}

    ID_info["ID_player"] = chat_id
    if username is not None:
        ID_info["username"] = username
    if money is not None:
        ID_info["money"] = money
    if user_case is not None:
        ID_info["user_case"] = user_case
    if ship_list is not None:
        ID_info["ship_list"] = ship_list
    if enemy_list is not None:
        ID_info["enemy_list"] = enemy_list
    if win is not None:
        ID_info["win"] = win
    if loose is not None:
        ID_info["loose"] = loose
    if ID_info['win'] > 0 and ID_info['loose'] > 0:
        ID_info['ratio_WL'] = ID_info['win'] / ID_info['loose']
    elif ID_info['win'] == 0 or ID_info['loose'] == 0:
        ID_info['ratio_WL'] = ID_info['win']
    if language is not None:
        ID_info["language"] = language
    if fleet_size is not None:
        ID_info["fleet_size"] = fleet_size
    if godmode is not None:
        ID_info["godmode"] = godmode
    if money_win is not None:
        ID_info["money_win"] = money_win
    if money_spent is not None:
        ID_info["money_spent"] = money_spent
    if case_purchased is not None:
        ID_info["case_purchased"] = case_purchased
    if case_open is not None:
        ID_info["case_open"] = case_open

    with open(f"user/{chat_id}.json", "w") as save_file:
        json.dump(ID_info, save_file, indent=2)


def load_json(chat_id):
    with open(f"user/{chat_id}.json", "r") as save_file:
        ID_info = json.load(save_file)
    return ID_info


def db_id_username(chat_id, username):
    try:
        with open(f"user/db_id_username.json", "r") as read_file:
            ID_info = json.load(read_file)
    except FileNotFoundError:
        ID_info = {}

    ID_info[f"{chat_id}"] = username
    with open(f"user/db_id_username.json", "w") as save_file:
        json.dump(ID_info, save_file, indent=2)


def load_db_id_username():
    with open("user/db_id_username.json", "r") as file:
        data = json.load(file)
    return data


def list_users():
    id_players = []
    for filename in os.listdir('user/'):
        if filename.endswith('.json'):
            with open(os.path.join('user/', filename)) as file:
                data = json.load(file)
                id_player = data.get('ID_player')
                if id_player is not None:
                    id_players.append(id_player)
    return id_players


def tree_choice(chat_id, branch=None, leaf=None, contact_captain=None):
    try:
        del save_tree_choice[chat_id]
    except KeyError:
        pass
    if branch is None:
        branch = 0
    if leaf is None:
        leaf = 0
    if contact_captain is None:
        contact_captain = 0

    save_tree_choice[chat_id] = {'branch': branch, 'leaf': leaf, 'contact_captain': contact_captain}

    branch = save_tree_choice[chat_id]['branch']
    leaf = save_tree_choice[chat_id]['leaf']

    return branch, leaf

