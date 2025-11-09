from labyrinth_game.constants import ROOMS

def describe_current_room(game_state):
    room_name = game_state['current_room']
    room_data = ROOMS[room_name]
    
    print(f'== {room_name.upper()} ==')
    print(room_data['description'])
    
    if room_data['items']:
        print("Заметные предметы:", ", ".join(room_data['items']))
    
    print("Выходы:", ", ".join(room_data['exits'].keys()))
    
    if room_data['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")
        
def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
    
def solve_puzzle(game_state):
    current_room = game_state['current_room']
    puzzle = ROOMS[current_room]['puzzle']
    
    if puzzle is None:
        print("Загадок здесь нет.")
        return
    
    question, correct_answer = puzzle
    print(question)
    user_answer = input("Ваш ответ: ").strip()
    
    if user_answer == correct_answer:
        print("Ваш ответ верный!")
        ROOMS[current_room]['puzzle'] = None
    else:
        print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state):
    if game_state['current_room'] != 'treasure_room':
        print("Здесь нет сундука с сокровищем.")
        return

    room = ROOMS['treasure_room']

    if 'treasure_chest' not in room['items']:
        print("Сундук уже открыт.")
        return

    if 'rusty_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return

    print("Сундук заперт. Можно попробовать ввести код.")
    choice = input("Ввести код? (да/нет): ").strip().lower()

    if choice in ('да', 'д', 'yes', 'y'):
        if room['puzzle'] is None:
            print("Загадка отсутствует. Невозможно открыть сундук.")
            return

        code = input("Введите код: ").strip()
        correct_code = room['puzzle'][1]

        if code == correct_code:
            print("Код верный! Сундук открывается с лёгким щелчком.")
            room['items'].remove('treasure_chest')
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
        else:
            print("Код неверный. Замок не поддаётся.")
    else:
        print("Вы отступаете от сундука.")