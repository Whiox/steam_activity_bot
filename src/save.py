import json

"""
save structure

{
    "recent": {
        name: hours
    }
    
    "games": [
        "game1": {
            name: hours
        }
        
        ...
        
        "gameX": {
            name: hours
        }
    ]
}
"""

DEFAULT_STRUCT = {
    "user": {
        "username": "None",
        "last_2_week": -1,
    },
    "recent": {},
    "games": []
}


def file_checker():
    """Check if a save file exists."""

    try:
        with open("save.json", "r", encoding='UTF-8') as file:
            pass
    except FileNotFoundError:
        with open("save.json", "w", encoding='UTF-8') as file:
            json.dump(DEFAULT_STRUCT, file)


def get_username() -> str:
    file_checker()

    with open("save.json", "r", encoding='UTF-8') as file:
        return json.load(file)["user"]["username"]


def get_last_2_week() -> int:
    file_checker()

    with open("save.json", "r", encoding='UTF-8') as file:
        return json.load(file)["user"]["last_2_week"]


def get_recent_game() -> dict:
    file_checker()

    with open("save.json", "r", encoding='UTF-8') as file:
        return json.load(file)['recent']


def get_games() -> list:
    file_checker()

    with open("save.json", "r", encoding='UTF-8') as file:
        return json.load(file)['games']


def update_username(username: str) -> None:
    file_checker()

    with open("save.json", "r", encoding='UTF-8') as file:
        data = json.load(file)

    data["user"]["username"] = username

    with open("save.json", "w", encoding='UTF-8') as file:
        json.dump(data, file)


def update_last_2_week(last_2_week: int) -> None:
    file_checker()

    with open("save.json", "r", encoding='UTF-8') as file:
        data = json.load(file)

    data["user"]["last_2_week"] = last_2_week

    with open("save.json", "w", encoding='UTF-8') as file:
        json.dump(data, file)


def update_recent_game(recent_game: dict) -> None:
    file_checker()

    with open("save.json", "r", encoding='UTF-8') as file:
        data = json.load(file)

    data["recent"] = recent_game

    with open("save.json", "w", encoding='UTF-8') as file:
        json.dump(data, file)


def update_games(games: list) -> None:
    file_checker()

    with open("save.json", "r", encoding='utf-8') as file:
        data = json.load(file)

    existing = {}
    for entry in data.get("games", []):
        for name, hours in entry.items():
            existing[name] = hours

    for entry in games:
        for name, hours in entry.items():
            existing[name] = hours

    data["games"] = [{name: hours} for name, hours in existing.items()]

    with open("save.json", "w", encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

