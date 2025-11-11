#!/usr/bin/env python3
from labyrinth_game.constants import COMMANDS, ROOMS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(command, game_state):
    cmd = command.strip().lower().split()
    if not cmd:
        return

    directions = ["north", "south", "east", "west"]

    if cmd[0] in directions:
        move_player(game_state, cmd[0])
        return

    if cmd[0] == "go" and len(cmd) > 1 and cmd[1] in directions:
        move_player(game_state, cmd[1])
        return

    if cmd[0] == "solve":
        if game_state["player"]["current_room"] == "treasure_room":
            attempt_open_treasure(game_state)
        else:
            solve_puzzle(game_state)
        return

    if cmd[0] == "take" and len(cmd) > 1:
        take_item(game_state, " ".join(cmd[1:]))
        return

    if cmd[0] == "use" and len(cmd) > 1:
        use_item(game_state, " ".join(cmd[1:]))
        return

    if cmd[0] == "inventory":
        show_inventory(game_state)
        return

    if cmd[0] == "look":
        describe_current_room(game_state)
        return

    if cmd[0] == "help":
        show_help(COMMANDS)
        return

    if cmd[0] == "quit":
        print("Выход из игры.")
        game_state["game_over"] = True
        return

    print("Неизвестная команда. Введите 'help' для справки.")


def main():
    print("Добро пожаловать в Лабиринт сокровищ!")

    game_state = {
        "player": {
            "inventory": [],
            "current_room": "entrance"
        },
        "steps": 0,
        "game_over": False,
        "rooms": ROOMS
    }

    describe_current_room(game_state)

    while not game_state['game_over']:
        command = get_input()
        process_command(command, game_state)

if __name__ == "__main__":
    main()
