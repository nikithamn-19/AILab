import random

board = [" " for _ in range(9)]


def print_board():
    print()
    print(board[0] + " | " + board[1] + " | " + board[2])
    print("--+---+--")
    print(board[3] + " | " + board[4] + " | " + board[5])
    print("--+---+--")
    print(board[6] + " | " + board[7] + " | " + board[8])
    print()


def check_winner(player):
    winning_positions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    for position in winning_positions:
        if all(board[i] == player for i in position):
            return True

    return False


def is_board_full():
    return " " not in board


# Simple AI
def bot_move():
    empty_positions = []

    for i in range(9):
        if board[i] == " ":
            empty_positions.append(i)

    if empty_positions:
        move = random.choice(empty_positions)
        board[move] = "O"


def tic_tac_toe():

    print("===== TIC TAC TOE =====")
    print("You = X")
    print("Bot = O")

    while True:

        # Player's turn
        print_board()

        try:
            position = int(input("Enter position (1-9): ")) - 1
        except ValueError:
            print("Please enter a number.")
            continue

        if position < 0 or position > 8 or board[position] != " ":
            print("Invalid move! Try again.")
            continue

        board[position] = "X"

        # Check player win
        if check_winner("X"):
            print_board()
            print("🎉 You win!")
            break

        # Check draw
        if is_board_full():
            print_board()
            print("It's a draw!")
            break

        # Bot's turn
        bot_move()

        print("Bot made a move.")

        # Check bot win
        if check_winner("O"):
            print_board()
            print("Bot wins!")
            break

        # Check draw
        if is_board_full():
            print_board()
            print("It's a draw!")
            break


tic_tac_toe()