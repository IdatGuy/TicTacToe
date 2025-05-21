import random
import os
import argparse

parser = argparse.ArgumentParser(description="Play Tic Tac Toe")
parser.add_argument('--hard', action='store_true', help="Enable hard mode")

args = parser.parse_args()
HARD_MODE = args.hard

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    for i in range(len(board)):
        print(" | ".join(board[i]))
        if i < len(board) - 1:
            print("-" * 9)

def player_order():
    #ditermine player order
    player_1 = random.choice(["Player", "Computer"])
    player_2 = "Computer" if player_1 == "Player" else "Player"
    # Assign symbols
    symbols = {
        player_1: "X",
        player_2: "O"
    }
    return player_1, player_2, symbols

def get_player_move(board):
    while True:
        try:
            move = input("Enter your move (row,col): ")
            row_str, col_str = move.split(",")
            row = int(row_str.strip()) - 1
            col = int(col_str.strip()) - 1

            # Check if in bounds
            if row not in range(3) or col not in range(3):
                print("Move out of bounds. Please enter numbers between 1 and 3.")
                continue

            # Check if spot is empty
            if board[row][col] != " ":
                print("That spot is already taken. Try again.")
                continue

            return row, col
        except ValueError:
            print("Invalid input format. Use row,col like 1,2.")

def get_computer_move(board, symbol):
    empty_cells = [
        (row, col)
        for row in range(3)
        for col in range(3)
        if board[row][col] == " "
    ]
    if HARD_MODE:
        #Impliment hard mode
        #look for a win then block
        for symbol in [symbols["Computer"], symbols["Player"]]:    
            for row, col in empty_cells:
                board[row][col] = symbol
                if check_winner(board):
                    board[row][col] = " "
                    return row, col
                else:
                    board[row][col] = " "
        #look for a corner
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for row, col in corners:
            if board[row][col] == " ":
                return row, col
        
        if not empty_cells:
            return None  # no moves left
        
    else:
        if not empty_cells:
            return None  # no moves left

    return random.choice(empty_cells)

def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return row[0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]

    return None  # No winner yet

winner = None
while winner is None:
    clear_terminal()
    board = [[" " for _ in range(3)] for _ in range(3)]
    player_1, player_2, symbols = player_order()
    for turn in range(9):
        current_player = player_1 if turn % 2 == 0 else player_2
        symbol = symbols[current_player]
        if turn == 0:
            print(f"{player_1} goes first and will be X.")
            #computer move
        if current_player == "Computer":
            row, col = get_computer_move(board, symbol)
            board[row][col] = symbols[current_player]
        else:
            #player move
            print_board(board)
            row, col = get_player_move(board)
            board[row][col] = symbols[current_player]
            clear_terminal()

        winner_symbol = check_winner(board)
        if winner_symbol:
            winner = player_1 if symbols[player_1] == winner_symbol else player_2
            clear_terminal()
            print_board(board)
            print(f"{winner} is the winner!")
            break
        if all(cell != " " for row in board for cell in row):
            winner = "tie"
            print("It's a tie!")
            break