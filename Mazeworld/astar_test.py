from astar_search import * 
from MazeworldProblem import * 


maze2 = Maze("Mazeworld/maze2.maz")
maze3 = Maze("Mazeworld/maze3.maz")
maze4 = Maze("Mazeworld/maze4.maz")
maze5 = Maze("Mazeworld/maze5.maz")
maze2_problem = MazeworldProblem(maze2, [(2, 2)])
maze4_problem = MazeworldProblem(maze4, [(2, 5)])
maze5_problem = MazeworldProblem(maze5, [(1, 11)])
# print(maze2_problem)
# maze2_problem.update((0, 1, 1))
# print(maze2_problem)
# print(astar_search(maze2_problem, manhattan_heuristic))
test_path = []
# solution4 = astar_search(maze4_problem, manhattan_heuristic, test_path)
# maze4_problem.animate_path(test_path)
# solution = astar_search(maze2_problem, manhattan_heuristic, test_path)
# print(solution4)
# maze4_problem.animate_path(test_path)

solution5 = astar_search(maze5_problem, manhattan_heuristic, test_path)
print(solution5)
# maze5_problem.animate_path(test_path)


