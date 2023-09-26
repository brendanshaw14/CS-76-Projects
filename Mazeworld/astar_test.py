from astar_search import * 
from MazeworldProblem import * 


maze2 = Maze("Mazeworld/mazes/maze2.maz")
maze3 = Maze("Mazeworld/mazes/maze3.maz")
maze4 = Maze("Mazeworld/mazes/maze4.maz")
maze5 = Maze("Mazeworld/mazes/maze5.maz")
maze6 = Maze("Mazeworld/mazes/maze6.maz")
maze2_problem = MazeworldProblem(maze2, [(2, 2)])
maze4_problem = MazeworldProblem(maze4, [(1, 4), (1, 3), (1, 2)])
maze5_problem = MazeworldProblem(maze5, [(1, 11)])
maze6_problem = MazeworldProblem(maze6, [(6, 0), (6, 1)])
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

# solution5 = astar_search(maze5_problem, manhattan_heuristic, test_path)
# print(solution5)
# maze5_problem.animate_path(test_path)

# print(astar_search(maze4_problem, manhattan_heuristic, test_path))
# maze4_problem.animate_path(astar_search(maze4_problem, manhattan_heuristic, test_path).path)

# print(maze6)
# print(astar_search(maze6_problem, manhattan_heuristic, test_path))
# print(maze6)

print(maze4)
print(astar_search(maze4_problem, manhattan_heuristic, test_path))
maze4_problem.animate_path(test_path)
# print(manhattan_heuristic(maze4_problem, (0, 1, 4, 1, 3, 1, 2)))