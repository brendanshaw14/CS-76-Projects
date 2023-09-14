# By Brendan Shaw, 2023- Adapted from Dartmouth COSC76 Course Materials by Devin Balcom

from FoxesProblem import FoxesProblem
from uninformed_search import bfs_search
# from uninformed_search import bfs_search, dfs_search, ids_search

# Create a few test problems:
problem331 = FoxesProblem((3, 3, 1))
problem541 = FoxesProblem((5, 4, 1))
problem551 = FoxesProblem((5, 5, 1))

# Run the searches.
#  Each of the search algorithms should return a SearchSolution object,
#  even if the goal was not found. If goal not found, len() of the path
#  in the solution object should be 0.

print(bfs_search(problem331))
# print(dfs_search(problem331))
# print(ids_search(problem331))

# print(bfs_search(problem551))
# print(dfs_search(problem551))
# print(ids_search(problem551))

# print(bfs_search(problem541))
# print(dfs_search(problem541))
# print(ids_search(problem541))
