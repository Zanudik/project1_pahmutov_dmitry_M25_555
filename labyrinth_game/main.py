#!/usr/bin/env python3
from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
)
from labyrinth_game.utils import describe_current_room, solve_puzzle


def process_command(command, game_state):
    cmd = command.strip().lower().split()

    if not cmd:
        return

    directions = ["north", "south", "east", "west"]
    if cmd[0] in directions:
        move_player(game_state, cmd[0])
        return

    if cmd[0] == "go" and len(cmd) > 1:
        move_player(game_state, cmd[1])
        return

    if cmd[0] == "solve":
        if game_state["player"]["current_room"] == "treasure_room":
            from labyrinth_game.utils import attempt_open_treasure
            attempt_open_treasure(game_state)
        else:
            solve_puzzle(game_state)
        return

    if cmd[0] == "help":
        from labyrinth_game.utils import show_help
        show_help(COMMANDS)
        return

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
