import json

data = {}

data["keybindings"] = []
data["mouse_settings"] = []
data["scoreboard"] = []
data["player_name"] = []
data["settings"] = []


def get_value(type, asked_key):
    if asked_key == "*":
        return load_saved_data()[type]
    for keys in load_saved_data()[type]:
        for key in keys:
            if key == asked_key:
                return keys[key]


def update_value(type, asked_key, value):
    for keys in load_saved_data()[type]:
        for key in keys:
            if key == asked_key:
                keys[key] = value
                return keys[key]


def save_values():
    with open('data.txt', 'w') as outfile:
        json.dump(load_saved_data(), outfile)
        print("Data Saved")


def get_default_values():
    data = {}
    data["keybindings"] = []
    data['keybindings'].append({
        "forward": "w",
        "left": "a",
        "backwards": "s",
        "right": "d",
        "car": "f",
        "quit": "q",
        "escape": "esc"
    })

    data["mouse_settings"] = []
    data['mouse_settings'].append({
        "sensitivity": 1
    })

    data["scoreboard"] = []
    data['scoreboard'].append({
        "You": 0
    })

    data["player_name"] = []
    data['player_name'].append({
        "name": "You"
    })

    data["settings"] = []
    data['settings'].append({
        "hints": "on"
    })

    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)
        print("Saved")
    return data


def load_saved_data():
    try:
        with open('data.txt') as json_file:
            saved_data = json.load(json_file)
            for keys in saved_data['keybindings']:
                for key in keys:
                    data['keybindings'].append({key: keys[key]})
            for keys in saved_data['mouse_settings']:
                for key in keys:
                    data['mouse_settings'].append({key: keys[key]})
            for keys in saved_data['scoreboard']:
                for key in keys:
                    data['scoreboard'].append({key: keys[key]})

            for keys in saved_data['player_name']:
                for key in keys:
                    data['player_name'].append({key: keys[key]})
            for keys in saved_data['settings']:
                for key in keys:
                    data['settings'].append({key: keys[key]})
        return saved_data
    except:
        return get_default_values()

load_saved_data()
