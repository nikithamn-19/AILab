def dls(state, goal, path, visited, depth_limit):

    # Goal test
    if state == goal:
        return path

    # Depth limit reached
    if depth_limit == 0:
        return None

    # Find blank position
    zero = state.index(0)
    row = zero // 3
    col = zero % 3

    moves = []

    if row > 0:
        moves.append(("UP", zero - 3))

    if row < 2:
        moves.append(("DOWN", zero + 3))

    if col > 0:
        moves.append(("LEFT", zero - 1))

    if col < 2:
        moves.append(("RIGHT", zero + 1))

    # Try each possible move
    for direction, move in moves:

        new = list(state)

        # Swap blank with tile
        new[zero], new[move] = new[move], new[zero]

        new = tuple(new)

        # Avoid cycles in current path
        if new not in visited:

            visited.add(new)

            result = dls(
                new,
                goal,
                path + [(direction, new)],
                visited,
                depth_limit - 1
            )

            if result is not None:
                return result

            # Backtrack
            visited.remove(new)

    return None


# ---------- IDS ----------

def ids(start, goal):

    depth = 0

    while True:

        visited = {start}

        result = dls(
            start,
            goal,
            [],
            visited,
            depth
        )

        if result is not None:
            return result, depth

        depth += 1


# ---------- USER INPUT ----------

print("Enter the 8-puzzle matrix (0 for blank):")

matrix = []

for i in range(3):
    row = list(map(int, input().split()))
    matrix.append(row)


# Convert matrix into tuple
start = tuple(num for row in matrix for num in row)


# ---------- GOAL STATE ----------

goal = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
)


# ---------- SOLVE USING IDS ----------

solution, solution_depth = ids(start, goal)


# ---------- OUTPUT ----------

if solution is not None:

    print("\nSolution found at depth:", solution_depth)
    print("Number of moves:", len(solution))

    for direction, state in solution:

        print("\nMove:", direction)

        for i in range(0, 9, 3):
            print(state[i:i+3])

else:
    print("No solution")