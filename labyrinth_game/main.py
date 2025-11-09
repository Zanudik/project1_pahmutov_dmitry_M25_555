#!/usr/bin/env python3
from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, show_help
from labyrinth_game.player_actions import get_input, move_player, take_item, show_inventory, use_item

def process_command(game_state, command):
    parts = command.split()
    if not parts:
        return
    cmd = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else []
    
    match cmd:
        case "go":
            if args:
                move_player(game_state, args[0])
        case "take":
            if args:
                take_item(game_state, args[0])
        case "use":
            if args:
                use_item(game_state, args[0])
        case "look":
            describe_current_room(game_state)
        case "inventory":
            show_inventory(game_state)
        case "quit" | "exit":
            game_state['game_over'] = True
        case "help":
            show_help()
        case "solve":
            if game_state['current_room'] == "treasure_room":
                from labyrinth_game.utils import attempt_open_treasure
                attempt_open_treasure(game_state)
            else:
                from labyrinth_game.utils import solve_puzzle
                solve_puzzle(game_state)
        case _:
            print("Неизвестная команда. Введите 'help' для справки.")

def main():
    
    print("Добро пожаловать в Лабиринт сокровищ!")
    
    game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
    }
    
    describe_current_room(game_state)
    
    while not game_state['game_over']:
        command = get_input()
        process_command(game_state, command)
   
if __name__ == "__main__":
    main()
