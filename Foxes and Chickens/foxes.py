# By Brendan Shaw, 2023- Adapted from Dartmouth COSC76 Course Materials by Devin Balcom

from FoxesProblem import FoxesProblem
from uninformed_search import bfs_search, dfs_search, ids_search
# from uninformed_search import bfs_search, dfs_search, ids_search

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
