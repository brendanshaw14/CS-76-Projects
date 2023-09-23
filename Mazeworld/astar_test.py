from astar_search import * 
from MazeworldProblem import * 


maze2 = Maze("Mazeworld/maze2.maz")
maze3 = Maze("Mazeworld/maze3.maz")
maze2_problem = MazeworldProblem(maze2, [(2, 2)])

print(astar_search(maze2_problem, manhattan_heuristic))

"""
(0, 1, 0)
1 0
1 0 1 1
1 0 1 -1
1 0 2 0
1 0 0 0
[(0, 1, 1)]
"""