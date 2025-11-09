#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room 
from labyrinth_game.player_actions import get_input

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
        # Пока не обрабатываем команду — просто выходим при "quit"
        if command == "quit":
            break
   
if __name__ == "__main__":
    main()
