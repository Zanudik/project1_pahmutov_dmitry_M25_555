import math

from labyrinth_game.constants import ROOMS

NUM_COMMANDS = 16
NUM_PSEUDO_RAND = 10

def describe_current_room(game_state):
    room_name = game_state["player"]["current_room"]
    room_data = ROOMS[room_name]

    print(f'== {room_name.upper()} ==')
    print(room_data['description'])

    if room_data['items']:
        print("Заметные предметы:", ", ".join(room_data['items']))

    print("Выходы:", ", ".join(room_data['exits'].keys()))

    if room_data['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def show_help(COMMANDS):
    print("\n Доступные команды:")
    for cmd, desc in COMMANDS.items():
        print(f"{cmd.ljust(NUM_COMMANDS)} — {desc}")

def solve_puzzle(game_state):
    current_room = game_state["player"]["current_room"]
    rooms = game_state["rooms"]
    puzzle = rooms[current_room].get("puzzle")
    if not puzzle:
        print("Здесь нет загадок.")
        return

    question, answer = puzzle
    user_input = input(question + "\n> ").strip().lower()

    valid_answers = [str(answer).lower()]
    if isinstance(answer, list):
        valid_answers.extend([str(a).lower() for a in answer])

    if user_input in valid_answers:
        print("Загадка решена!")
        if current_room == "trap_room" and "torch" \
            not in game_state["player"]["inventory"]:
            game_state["player"]["inventory"].append("torch")
            print("Вы нашли факел — теперь ловушки вам не страшны.")
        elif current_room == "hall" and "rusty_key" \
            not in game_state["player"]["inventory"]:
            game_state["player"]["inventory"].append("rusty_key")
            print("Вы получили предмет: ржавый ключ!")
        elif current_room == "library" and "ancient_book" \
            not in game_state["player"]["inventory"]:
            game_state["player"]["inventory"].append("ancient_book")
            print("Вы получили предмет: древняя книга!")
    else:
        print("Неверный ответ.")
        if current_room == "trap_room":
            trigger_trap(game_state)

def attempt_open_treasure(game_state):
    room = ROOMS['treasure_room']
    if 'treasure_chest' not in room['items']:
        print("Сундук уже открыт.")
        return

    if 'rusty_key' in game_state["player"]["inventory"]:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    choice = input("Сундук заперт. Ввести код? (да/нет): ").strip().lower()
    if choice in ('да', 'д', 'yes', 'y'):
        code = input("Введите код: ").strip()
        if code == str(room['puzzle'][1]):
            print("Код верный! Сундук открывается с лёгким щелчком.")
            room['items'].remove('treasure_chest')
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
        else:
            print("Код неверный. Замок не поддаётся.")
    else:
        print("Вы отступаете от сундука.")

def pseudo_random(seed, modulo):
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional = x - math.floor(x)
    return int(fractional * modulo)

def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state["player"]["inventory"]
    if inventory:
        index = pseudo_random(game_state["steps"], len(inventory))
        lost_item = inventory.pop(index)
        print(f"Вы потеряли предмет: {lost_item}!")
    else:
        danger = pseudo_random(game_state["steps"], NUM_PSEUDO_RAND)
        if danger < 3:
            print("Ловушка оказалась смертельной! Вы погибли.")
            game_state["game_over"] = True
        else:
            print("Вам чудом удалось уцелеть!")

def random_event(game_state):
    seed = game_state["steps"]
    current_room = game_state["player"]["current_room"]
    room_data = game_state["rooms"][current_room]

    if pseudo_random(seed, NUM_PSEUDO_RAND) != 0:
        return

    event_type = pseudo_random(seed + 1, 3)

    if event_type == 0:
        print("Вы нашли блестящую монетку на полу!")
        room_data["items"].append("coin")
    elif event_type == 1:
        print("Вы слышите странный шорох где-то рядом...")
        if "sword" in game_state["player"]["inventory"]:
            print("Вы вскидываете меч, и тень мгновенно исчезает!")
    elif event_type == 2:
        if "trap" in current_room and "torch" \
            not in game_state["player"]["inventory"]:
            print("Воздух вокруг сгущается — что-то не так!")
            trigger_trap(game_state)
