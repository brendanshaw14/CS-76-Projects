# By Brendan Shaw, 2023- Adapted from Dartmouth COSC76 Course Materials by Devin Balcom

from FoxesProblem import FoxesProblem
from uninformed_search import bfs_search, dfs_search, ids_search
# from uninformed_search import bfs_search, dfs_search, ids_search

def visualize_solution(search_problem, path):
    if path and len(path) > 0:
        # loop through states in the path
        for state in path:
            # calculate all the values
            left_foxes = "F" * state[0]
            left_chickens = "C" * state[1]
            right_foxes = "F" * (search_problem.start_state[0] - state[0])
            right_chickens = "C" * (search_problem.start_state[1] - state[1])
            left_boats = "B" if state[2] == 1 else " "
            right_boats = "B" if search_problem.start_state[2] - state[2] == 1 else " "

            # Pad with spaces as needed for consistent width
            left_foxes = left_foxes.ljust(3)
            left_chickens = left_chickens.ljust(3)
            right_foxes = right_foxes.ljust(3)
            right_chickens = right_chickens.ljust(3)

            print(left_foxes + left_chickens + left_boats + "|" + right_foxes + right_chickens + right_boats)
            print("-" * (2 * (search_problem.start_state[0] + search_problem.start_state[1]) + 4))
            print("\n")
    else:
        print("No solution to visualize")


# Create a few test problems:
problem331 = FoxesProblem((3, 3, 1))
problem451 = FoxesProblem((4, 5, 1))
problem551 = FoxesProblem((5, 5, 1))

print(bfs_search(problem331))
print(dfs_search(problem331))
print(ids_search(problem331))

print(bfs_search(problem551))
print(dfs_search(problem551))
print(ids_search(problem551))

print(bfs_search(problem451))
print(dfs_search(problem451))
print(ids_search(problem451))

visualize_solution(problem331, bfs_search(problem331).path)
visualize_solution(problem451, bfs_search(problem451).path)