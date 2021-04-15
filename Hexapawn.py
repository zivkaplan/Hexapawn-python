from os import system
from random import randrange

def load_moves():
	while True:
		file_path = input("type the path of the computer moves file:\n")
		dict_of_boards = {}
		try:
			with open(file_path, "r") as f1:
				content = f1.read().splitlines()
				for i in content:
					item = i.split(" : ")
					dict_of_boards[eval(item[0])] = eval(item[1])
				return dict_of_boards

		except:
			print("Error loading file. try again.")



def print_board(board):
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

def possible_board_moves(board_tuple, moves_dictionary):
	return moves_dictionary[board_tuple]


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
	
	if (is_space_free(board, soldier + (steps)))\
		or (soldier == 8 and (4 or 6) in team_places(board, opponet))\
			or ((soldier == 6 or soldier == 4) and 2 in team_places(board, opponet))\
				or ((soldier == 7 or soldier == 9) and 5 in team_places(board, opponet))\
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
				if (move == pick_up - 3 and is_space_free(board, move))\
					or (move == 5 and pick_up in [7, 9] and move in team_places(board, "O"))\
						or (move % 2 == 0 and (move == pick_up - 2 or move == pick_up - 4)\
							and (move in team_places(board, "O")))\
								or ((move == 1 or move == 3) and pick_up == 5 and move in team_places(board, "O")):
					place_soldier(board, move, 'X')
					break
				else:
					print("This space isn't a valid move!")
			else:
				print("Please type a number within the range!")
		except:
			print("Please type a number.")


def check_computer_move(board, pick_up,move):
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


def computer_choice(board, board_tuple, moves_dictionary):
	moves_options = possible_board_moves(board_tuple, moves_dictionary)
	while True:
		chosen_move = select_random(moves_options)
		is_move_valid = check_computer_move(board, chosen_move[0], chosen_move[1])
		if is_move_valid:
			current_move = computer_move(board, chosen_move[0], chosen_move[1])
			break
	return current_move

def select_random(lst):
	random_choice = randrange(0,len(lst))
	return lst[random_choice]


def place_soldier(board, pos, letter):
	board[pos] = letter


def is_winner(board, letter):
	if letter == "X":
		return board[1] == letter or board[2] == letter or board[3] == letter
	else: #letter is "O"
		return board[7] == letter or board[8] == letter or board[9] == letter


def remove_soldier(board, pos):
	board[pos] = " "

def delete_losing_moves(learned_moves, board_keys, moves):
	for i in range(len(board_keys) - 1):
		learned_moves[board_keys[i]].remove(moves[i])
	return learned_moves


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
	moves_dictionary = load_moves()
	AI_moves = moves_dictionary.copy()
	computers_this_game_moves = []
	board_situations = []
	playing = True
	while playing:
		board = {
			1: "O",
			2: "O",
			3: "O",
			4: " ",
			5: " ",
			6: " ",
			7: "X",
			8: "X",
			9: "X"
			}      
		computer_moves_in_turn = []
		system("cls")
		print_board(board)
		while True:
			picked_soldier = player_soldier_pick(board)
			player_soldier_placing(board, picked_soldier)
			temp_board = board_to_tuple(board)
			board_situations.append(temp_board)
			system("cls")
			print_board(board)
			if is_winner(board, "X") or checkmate(board, "O"):
				print("You have won")
				improved_moves_dictionary = delete_losing_moves(AI_moves, board_situations, computers_this_game_moves)
				write_moves_to_file(improved_moves_dictionary)
				break

			computer_moves_in_turn = computer_choice(board, temp_board, AI_moves)
			computers_this_game_moves.append(computer_moves_in_turn)
			system("cls")
			print_board(board)
			if is_winner(board, "O") or checkmate(board, "X"):
				print("Computer has won")
				break

		playing = play_again()
		system('cls')


if __name__ == '__main__':
	main()