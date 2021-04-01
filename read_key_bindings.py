import json

data = {}

data["keybindings"] = []
data["mouse_settings"] = []
data["scoreboard"] = []
data["player_name"] = []
data["settings"] = []


def getValue(type, asked_key):
    if asked_key == "*":
        return saved_data[type]
    for keys in saved_data[type]:
        for key in keys:
            if key == asked_key:
                return keys[key]


def updateValue(type, asked_key, value):
    for keys in saved_data[type]:
        for key in keys:
            if key == asked_key:
                keys[key] = value
                return keys[key]


def saveValues():
    with open('data.txt', 'w') as outfile:
        json.dump(saved_data, outfile)
        print("Saved")


def getDefaultValues():
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
        "hints": True
    })

    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)
        print("Saved")


with open('data.txt') as json_file:
    saved_data = json.load(json_file)
    try:
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
    except:
        getDefaultValues()
