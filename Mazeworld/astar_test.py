from astar_search import * 
from MazeworldProblem import * 


maze2 = Maze("Mazeworld/maze2.maz")
maze3 = Maze("Mazeworld/maze3.maz")
maze4 = Maze("Mazeworld/maze4.maz")
maze2_problem = MazeworldProblem(maze2, [(2, 2)])
maze4_problem = MazeworldProblem(maze4, [(2, 5)])
# print(maze2_problem)
# maze2_problem.update((0, 1, 1))
# print(maze2_problem)
# print(astar_search(maze2_problem, manhattan_heuristic))
# print(astar_search(maze4_problem, manhattan_heuristic))


