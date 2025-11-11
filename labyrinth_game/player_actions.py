from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import random_event, attempt_open_treasure


def show_inventory(game_state):
    inventory = game_state["player"]["inventory"]
    if inventory:
        print("Инвентарь:", ", ".join(inventory))
    else:
        print("Инвентарь пуст.")

def get_input(prompt="> "):
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction):
    current_room = game_state["player"]["current_room"]
    rooms = game_state["rooms"]

    if direction not in rooms[current_room]["exits"]:
        print("В этом направлении нет выхода.")
        return

    next_room = rooms[current_room]["exits"][direction]

    if next_room == "treasure_room" and "rusty_key" \
        not in game_state["player"]["inventory"]:
        print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        return

    game_state["player"]["current_room"] = next_room
    game_state["steps"] += 1

    print(f"Вы переместились в {next_room}.")
    print(rooms[next_room]["description"])
    if rooms[next_room]["items"]:
        print("Заметные предметы:", ", ".join(rooms[next_room]["items"]))
    print("Выходы:", ", ".join(rooms[next_room]["exits"].keys()))

    random_event(game_state)

def take_item(game_state, item_name):
    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    room = ROOMS[game_state["player"]["current_room"]]
    items = room['items']

    if item_name in items:
        game_state["player"]["inventory"].append(item_name)
        room['items'].remove(item_name)
        print("Вы подняли:", item_name)
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    if item_name in game_state["player"]["inventory"]:
        match item_name:
            case "torch":
                print("Факел освещает путь. Стало светлее!")
            case "sword":
                print("Вы чувствуете себя увереннее.")
            case "bronze_box":
                print("Вы открыли бронзовую шкатулку.")
                if 'rusty_key' not in game_state["player"]["inventory"]:
                    game_state["player"]["inventory"].append('rusty_key')
            case "rusty_key":
                current_room = game_state["player"]["current_room"]
                if current_room == "treasure_room":
                    attempt_open_treasure(game_state)
                else:
                    print("Вы не можете использовать этот ключ здесь.")
            case _:
                print("Неизвестно как использовать.")
    else:
        print("У вас нет такого предмета.")

