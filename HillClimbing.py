
def heuristic(state):
    conflicts = 0

    for i in range(4):
        for j in range(i + 1, 4):
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1

    return conflicts


def hill_climbing(state):

    while True:
        current_h = heuristic(state)

        print("\nCurrent State:", state)
        print("Current Heuristic:", current_h)

        neighbours = []

        # Generate exactly 6 neighbours by swapping positions
        for i in range(4):
            for j in range(i + 1, 4):
                new_state = state[:]

                new_state[i], new_state[j] = new_state[j], new_state[i]

                h = heuristic(new_state)

                neighbours.append((new_state, h))

        print("\nAll 6 Neighbours:")

        for k, (neighbour, h) in enumerate(neighbours, 1):
            print(k, ":", neighbour, " Heuristic =", h)

        # Find the best neighbour
        best_state, best_h = min(neighbours, key=lambda x: x[1])

        print("\nBest Neighbour:", best_state)
        print("Best Heuristic:", best_h)

        # Check local minimum
        if best_h >= current_h:
            print("\nLOCAL MINIMUM REACHED!")
            print("Final State:", state)
            print("Final Heuristic:", current_h)
            break

        # Move to best neighbour
        state = best_state


# User input
print("Enter 4 queen positions (1 to 4):")

state = []

for i in range(4):
    pos = int(input("Enter position for queen " + str(i + 1) + ": "))
    state.append(pos)

if sorted(state) != [1, 2, 3, 4]:
    print("Invalid input! Enter each number from 1 to 4 only once.")
else:
    hill_climbing(state)
