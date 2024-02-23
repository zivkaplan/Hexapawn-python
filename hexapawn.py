from os import system
from random import randrange
import platform

from consts import COMPUNTER_MOVES_MAP, OPENING_BOARD


def clear_screen():
    cmd = "clear"
    if platform.system() == "Windows":
        cmd = "cls"

    system(cmd)


def print_board(board):
    clear_screen()
    for i in board.keys():
        if i % 3 == 0:
            print(board[i])
            if i < 9:
                print("----------")
        else:
            print(board[i] + " |", end=" ")


def board_to_tuple(board):
    current_board = []
    for i in board.keys():
        if board[i] != " ":
            current_board.append(i)
    return tuple(current_board)


def possible_board_moves(board_tuple, moves_map):
    return moves_map[board_tuple]


def is_space_free(board, pos):
    return board[pos] == " "


def checkmate(board, letter):
    return available_soldiers(board, letter) == []


def is_not_stuck(board, soldier, letter):
    if letter == "X":
        steps = -3
        opponet = "O"
    else:
        steps = 3
        opponet = "X"

    if (is_space_free(board, soldier + (steps))) \
            or (soldier == 8 and (4 or 6) in team_places(board, opponet)) \
            or ((soldier == 6 or soldier == 4) and 2 in team_places(board, opponet)) \
            or ((soldier == 7 or soldier == 9) and 5 in team_places(board, opponet)) \
            or (soldier == 5 and (1 or 3) in team_places(board, opponet)):
        return True
    return False


def available_soldiers(board, letter):
    return [i for i in board.keys() if board[i] == letter and is_not_stuck(board, i, letter)]


def team_places(board, letter):
    return [i for i in board.keys() if board[i] == letter]


def player_soldier_pick(board):
    player_available_soldiers = available_soldiers(board, "X")
    while True:
        print(f"Your availble soldiers are {player_available_soldiers}")
        pick_up = input("please type the position (1-9) of the soldier you would like to move:\n")
        try:
            pick_up = int(pick_up)
            if pick_up in available_soldiers(board, "X"):
                remove_soldier(board, pick_up)
                return pick_up
                break
            else:
                print("You chose an invalid spot, try again.")
        except:
            print("Please type a number.")


def player_soldier_placing(board, pick_up):
    while True:
        move = input("please type position (1-9) to place the soldier:\n")
        try:
            move = int(move)
            if 1 <= move <= 9:
                if (move == pick_up - 3 and is_space_free(board, move)) \
                        or (move == 5 and pick_up in [7, 9] and move in team_places(board, "O")) \
                        or (move % 2 == 0 and (move == pick_up - 2 or move == pick_up - 4) \
                            and (move in team_places(board, "O"))) \
                        or ((move == 1 or move == 3) and pick_up == 5 and move in team_places(board, "O")):
                    place_soldier(board, move, 'X')
                    break
                else:
                    print("This space isn't a valid move!")
            else:
                print("Please type a number within the range!")
        except:
            print("Please type a number.")


def check_computer_move(board, pick_up, move):
    if board[pick_up] == "O" and board[move] != "O":
        return True
    return False


def computer_move(board, pick_up, move):
    current_move = []
    remove_soldier(board, pick_up)
    place_soldier(board, move, 'O')
    current_move.append(pick_up)
    current_move.append(move)
    return current_move


def computer_choice(board, board_tuple, moves_map):
    moves_options = possible_board_moves(board_tuple, moves_map)
    while True:
        chosen_move = select_random(moves_options)
        is_move_valid = check_computer_move(board, chosen_move[0], chosen_move[1])
        if is_move_valid:
            current_move = computer_move(board, chosen_move[0], chosen_move[1])
            break
    return current_move


def select_random(lst):
    random_choice = randrange(0, len(lst))
    return lst[random_choice]


def place_soldier(board, pos, letter):
    board[pos] = letter


def is_winner(board, letter):
    if letter == "X":
        return board[1] == letter or board[2] == letter or board[3] == letter
    else:  # letter is "O"
        return board[7] == letter or board[8] == letter or board[9] == letter


def remove_soldier(board, pos):
    board[pos] = " "


def delete_losing_moves(available_moves, board_keys, moves):
    for board in board_keys:
        for move in moves:
            if move in available_moves[board]:
                available_moves[board].remove(move)
    return available_moves


def write_moves_to_file(learned_dictionary):
    str_dictionary_for_export = ""
    for i in learned_dictionary.keys():
        str_dictionary_for_export = str_dictionary_for_export + str(i) + " : " + str(learned_dictionary[i]) + "\n"
    with open("learned_comuter_moves.txt", "w") as f1:
        f1.write(str_dictionary_for_export)


def play_again():
    while True:
        answer = input("Would you like to play again? - (Y\\N) \n")
        if answer.lower() == "y":
            return True
        if answer.lower() == "n":
            return False
        else:
            print("invalid output")


def main():
    moves_map = COMPUNTER_MOVES_MAP
    pc_game_moves = []
    board_situations = []
    playing = True
    while playing:
        board = OPENING_BOARD.copy()
        pc_chosen_move = []
        print_board(board)
        while True:
            picked_soldier = player_soldier_pick(board)
            player_soldier_placing(board, picked_soldier)
            current_board = board_to_tuple(board)
            print_board(board)
            if is_winner(board, "X") or checkmate(board, "O"):
                print("You have won")
                improved_moves_map = delete_losing_moves(moves_map, board_situations, pc_game_moves)
                write_moves_to_file(improved_moves_map)
                break

            board_situations.append(current_board)
            pc_chosen_move = computer_choice(board, current_board, moves_map)
            pc_game_moves.append(pc_chosen_move)
            print_board(board)
            if is_winner(board, "O") or checkmate(board, "X"):
                print("Computer has won")
                break

        playing = play_again()
        clear_screen()


if __name__ == '__main__':
    main()
