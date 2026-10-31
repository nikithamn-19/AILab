
import random
import math

def heuristic(board):
    conflicts = 0

    for i in range(8):
        for j in range(i + 1, 8):
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1

    return conflicts


def simulated_annealing(board):
    temperature = 100
    cooling = 0.99

    while temperature > 0.01:
        h = heuristic(board)

        if h == 0:
            return board

        i, j = random.sample(range(8), 2)

        new_board = board[:]
        new_board[i], new_board[j] = new_board[j], new_board[i]

        new_h = heuristic(new_board)

        if new_h < h:
            board = new_board
        else:
            probability = math.exp((h - new_h) / temperature)

            if random.random() < probability:
                board = new_board

        temperature *= cooling

    if heuristic(board) == 0:
        return board

    return None


# User input
board = list(map(int, input("Enter 8 queen positions: ").split()))

if len(board) != 8 or sorted(board) != list(range(1, 9)):
    print("Enter 8 unique numbers from 1 to 8")
else:
    result = simulated_annealing(board)

    if result:
        print("\nSolution Found!")
        print("Queen Positions:", result)

        for r in range(1, 9):
            for c in range(8):
                if result[c] == r:
                    print(" Q ", end="")
                else:
                    print(" . ", end="")
            print()

        print("Heuristic:", heuristic(result))
    else:
        print("\nSolution not found. Try again.")
