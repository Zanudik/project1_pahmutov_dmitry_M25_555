from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room

def show_inventory(game_state):
    inventory = game_state['player_inventory']
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
    room = ROOMS[game_state['current_room']]
    
    if direction in room['exits']:
        game_state['current_room'] = room['exits'][direction]
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    room = ROOMS[game_state['current_room']]
    items = room['items']
    
    if item_name in items:
        game_state['player_inventory'].append(item_name)
        room['items'].remove(item_name)
        print("Вы подняли:", item_name)
    else:
        print("Такого предмета здесь нет.")
        
def use_item(game_state, item_name):
    if item_name in game_state['player_inventory']:
        match item_name:
            case "torch":
                print("Факел освещает путь. Стало светлее!")
            case "sword":
                print("Вы чувствуете себя увереннее.")
            case "bronze box":
                print("Вы открыли бронзовую шкатулку.")
                if 'rusty_key' not in game_state['player_inventory']:
                    game_state['player_inventory'].append('rusty_key')
            case _:
                print("Неизвестно как использовать.") 
    else:
        print("У вас нет такого предмета.")