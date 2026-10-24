import heapq

goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)

def heuristic(state, choice):
    if choice == 1:
        return sum(1 for i in range(9)
                   if state[i] != 0 and state[i] != goal[i])

    distance = 0
    for i in range(9):
        tile = state[i]
        if tile != 0:
            r1, c1 = divmod(i, 3)
            r2, c2 = divmod(tile - 1, 3)
            distance += abs(r1 - r2) + abs(c1 - c2)

    return distance


def neighbors(state):
    result = []
    zero = state.index(0)
    r, c = divmod(zero, 3)

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc

        if 0 <= nr < 3 and 0 <= nc < 3:
            pos = nr * 3 + nc
            s = list(state)
            s[zero], s[pos] = s[pos], s[zero]
            result.append(tuple(s))

    return result


def astar(start, choice):
    pq = [(heuristic(start, choice), 0, start)]
    cost = {start: 0}
    parent = {start: None}

    while pq:
        f, g, state = heapq.heappop(pq)

        if g != cost[state]:
            continue

        if state == goal:
            path = []
            while state is not None:
                path.append(state)
                state = parent[state]

            print("\nSolution path:")
            for s in reversed(path):
                for i in range(0, 9, 3):
                    print(s[i:i+3])
                print()

            print("Total moves:", len(path) - 1)
            return

        for nxt in neighbors(state):
            new_g = g + 1

            if nxt not in cost or new_g < cost[nxt]:
                cost[nxt] = new_g
                parent[nxt] = state
                new_f = new_g + heuristic(nxt, choice)
                heapq.heappush(pq, (new_f, new_g, nxt))

    print("No solution found")


start = tuple(map(int, input("Enter 9 numbers (0 for blank): ").split()))

print("1. Misplaced Tiles")
print("2. Manhattan Distance")
while True:
    choice = int(input("Enter your choice: "))
    if choice==1 or choice==2:
        astar(start, choice)
    else:
        break