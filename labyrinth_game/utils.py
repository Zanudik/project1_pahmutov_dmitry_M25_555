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