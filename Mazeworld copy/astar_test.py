from astar_search import * 
from MazeworldProblem import * 
from SensorlessProblem import * 

# Author: Brendan Shaw, 2023
# CS76 Artificial Intelligence
# Test file for the mazeworld lab
# 
# 

# make a bunch of mazes
maze2 = Maze("Mazeworld/mazes/maze2.maz")
maze3 = Maze("Mazeworld/mazes/maze3.maz")
maze4 = Maze("Mazeworld/mazes/maze4.maz")
maze5 = Maze("Mazeworld/mazes/maze5.maz")
maze6 = Maze("Mazeworld/mazes/maze6.maz")

# initialize a bunch of maze problems
maze2_problem = MazeworldProblem(maze2, [(2, 2)])
maze4_problem = MazeworldProblem(maze4, [(1, 4), (1, 3), (1, 2)])
maze5_problem = MazeworldProblem(maze5, [(38, 38)])
maze6_problem = MazeworldProblem(maze6, [(6, 0), (6, 1)])

# this was used in testing- I didn't take it out cause it doesn't hurt anything and stores the path of all the nodes visited, even not on the path
test_path = []

# test a*: some mazes have multiple goals
print(astar_search(maze2_problem, assigned_manhattan_heuristic, test_path))
print(astar_search(maze4_problem, assigned_manhattan_heuristic, test_path))
print(astar_search(maze5_problem, assigned_manhattan_heuristic, test_path))
print(astar_search(maze6_problem, assigned_manhattan_heuristic, test_path))


# initialize the blind maze problems
blind_maze2_problem = SensorlessProblem(maze2, [])
blind_maze4_problem = SensorlessProblem(maze4, [])
blind_maze6_problem = SensorlessProblem(maze6, [])

print(astar_search(blind_maze2_problem, state_size_heuristic, test_path))
print(astar_search(blind_maze4_problem, state_size_heuristic, test_path))
print(astar_search(blind_maze6_problem, state_size_heuristic, test_path))

## ANIMATE PATHS: UNCOMMENT THESE (individually) TO WATCH ANY OF THE SOLUTIONS IN REAL TIME. 
# maze2_problem.animate_path(astar_search(maze2_problem, assigned_manhattan_heuristic, test_path).path)
# maze4_problem.animate_path(astar_search(maze4_problem, assigned_manhattan_heuristic, test_path).path)
# maze5_problem.animate_path(astar_search(maze5_problem, assigned_manhattan_heuristic, test_path).path)
# maze6_problem.animate_path(astar_search(maze2_problem, assigned_manhattan_heuristic, test_path).path)

"""
Here is the printed output from the above tests: 

----
Mazeworld problem: 
##.#
#...
#A#.

Number of Robots: 1
Start State: (0, 1, 0)
Goal Locations: [(2, 2)]
Robot Locations[1, 0]
 ------------------------
attempted with search method Astar with heuristic assigned_manhattan_heuristic
number of nodes visited: 4
solution length: 4
cost: 3
path: [(0, 1, 0), (0, 1, 1), (0, 2, 1), (0, 2, 2)]

----
Mazeworld problem: 
##.##
#...#
#.#.#
#C..#
#B..#
#A###

Number of Robots: 3
Start State: (0, 1, 0, 1, 1, 1, 2)
Goal Locations: [(1, 4), (1, 3), (1, 2)]
Robot Locations[1, 0, 1, 1, 1, 2]
 ------------------------
attempted with search method Astar with heuristic assigned_manhattan_heuristic
number of nodes visited: 156
solution length: 16
cost: 10
path: [(0, 1, 0, 1, 1, 1, 2), (1, 1, 0, 1, 1, 1, 2), (2, 1, 0, 2, 1, 1, 2), (0, 1, 0, 2, 1, 1, 2), (1, 1, 1, 2, 1, 1, 2), (2, 1, 1, 2, 1, 1, 2), (0, 1, 1, 2, 1, 2, 2), (1, 1, 2, 2, 1, 2, 2), (2, 1, 2, 1, 1, 2, 2), (0, 1, 2, 1, 1, 2, 2), (1, 1, 3, 1, 1, 2, 2), (2, 1, 3, 1, 2, 2, 2), (0, 1, 3, 1, 2, 2, 2), (1, 1, 4, 1, 2, 2, 2), (2, 1, 4, 1, 3, 2, 2), (0, 1, 4, 1, 3, 1, 2)]

----
Mazeworld problem: 
########################################
#..#...................#...............#
#..#...##.##.....#.....#...............#
#..#...#...#.....#.....#...............#
#..#####...#######.....#...#.....#.....#
#..........#...........#...#.....#.....#
#....#######.....###########.....#.....#
#....#.....#...............#.....#.....#
#....#.....#.....#....#...########.....#
#....#.....#.....#....#...#............#
#....#######.....#######..#..#####.....#
#....#..............#.....#..#...#######
#.......#..######...#........#...#.....#
#####...#......##...##########...#..#..#
#....#..#.....##.####............#..#..#
#....#..#..............####.#.####..#..#
#....#..#..........#####.........#..#..#
#....#..#..........#....###.######..#..#
#....##########....#........#.......#..#
#.......#..........#........#.......#..#
#....######..#######........#...#####..#
#....#....#..#..............#...#......#
#..###....#..#....#....######...#####..#
#....#....#..#....#.................#..#
#.........#..#....#..#####....#####.#..#
#....######..#....#......#....#.....#..#
#.................###....#....#..##.#..#
#........................#....#........#
#.....####################....#........#
#...........#..........................#
#...........#........########..........#
#....................#.....#############
#........########....#.................#
#.......#.......#....#.....#####.......#
#.......#.......#....#.........#.......#
#.......#.......#....#.........#.......#
#.......#.......#....######....#.......#
#....#######....#..............#.......#
#A..............#..............#.......#
########################################

Number of Robots: 1
Start State: (0, 1, 1)
Goal Locations: [(38, 38)]
Robot Locations[1, 1]
 ------------------------
attempted with search method Astar with heuristic assigned_manhattan_heuristic
number of nodes visited: 1077
solution length: 95
cost: 94
path: [(0, 1, 1), (0, 1, 2), (0, 1, 3), (0, 1, 4), (0, 1, 5), (0, 1, 6), (0, 1, 7), (0, 1, 8), (0, 1, 9), (0, 1, 10), (0, 1, 11), (0, 1, 12), (0, 1, 13), (0, 2, 13), (0, 3, 13), (0, 4, 13), (0, 5, 13), (0, 6, 13), (0, 7, 13), (0, 8, 13), (0, 9, 13), (0, 10, 13), (0, 11, 13), (0, 11, 14), (0, 11, 15), (0, 11, 16), (0, 11, 17), (0, 11, 18), (0, 11, 19), (0, 11, 20), (0, 12, 20), (0, 13, 20), (0, 14, 20), (0, 15, 20), (0, 15, 21), (0, 15, 22), (0, 15, 23), (0, 15, 24), (0, 14, 24), (0, 13, 24), (0, 13, 25), (0, 13, 26), (0, 12, 26), (0, 11, 26), (0, 10, 26), (0, 10, 27), (0, 10, 28), (0, 11, 28), (0, 12, 28), (0, 12, 29), (0, 12, 30), (0, 12, 31), (0, 12, 32), (0, 13, 32), (0, 14, 32), (0, 15, 32), (0, 16, 32), (0, 17, 32), (0, 18, 32), (0, 19, 32), (0, 20, 32), (0, 21, 32), (0, 22, 32), (0, 23, 32), (0, 24, 32), (0, 25, 32), (0, 25, 31), (0, 25, 30), (0, 25, 29), (0, 25, 28), (0, 25, 27), (0, 26, 27), (0, 27, 27), (0, 27, 28), (0, 27, 29), (0, 27, 30), (0, 28, 30), (0, 29, 30), (0, 30, 30), (0, 31, 30), (0, 32, 30), (0, 33, 30), (0, 34, 30), (0, 34, 31), (0, 34, 32), (0, 34, 33), (0, 34, 34), (0, 34, 35), (0, 34, 36), (0, 34, 37), (0, 34, 38), (0, 35, 38), (0, 36, 38), (0, 37, 38), (0, 38, 38)]

----
Mazeworld problem: 
.......
.##....
..##...
....#..
..##...
B.#....
A...##.

Number of Robots: 2
Start State: (0, 0, 0, 0, 1)
Goal Locations: [(6, 0), (6, 1)]
Robot Locations[0, 0, 0, 1]
 ------------------------
attempted with search method Astar with heuristic assigned_manhattan_heuristic
number of nodes visited: 168
solution length: 29
cost: 16
path: [(0, 0, 0, 0, 1), (1, 1, 0, 0, 1), (0, 1, 0, 1, 1), (1, 2, 0, 1, 1), (0, 2, 0, 1, 1), (1, 3, 0, 1, 1), (0, 3, 0, 1, 1), (1, 3, 1, 1, 1), (0, 3, 1, 1, 1), (1, 4, 1, 1, 1), (0, 4, 1, 1, 1), (1, 5, 1, 1, 1), (0, 5, 1, 1, 1), (1, 6, 1, 1, 1), (0, 6, 1, 1, 1), (1, 6, 0, 1, 1), (0, 6, 0, 1, 0), (1, 6, 0, 1, 0), (0, 6, 0, 2, 0), (1, 6, 0, 2, 0), (0, 6, 0, 3, 0), (1, 6, 0, 3, 0), (0, 6, 0, 3, 1), (1, 6, 0, 3, 1), (0, 6, 0, 4, 1), (1, 6, 0, 4, 1), (0, 6, 0, 5, 1), (1, 6, 0, 5, 1), (0, 6, 0, 6, 1)]

----
Blind robot problem: 
Goal location: []
Start State: 
frozenset({(1, 0), (2, 1), (2, 2), (3, 1), (1, 1), (3, 0)})
attempted with search method Astar with heuristic state_size_heuristic
number of nodes visited: 17
solution length: 6
cost: 5
path: [frozenset({(1, 0), (2, 1), (2, 2), (3, 1), (1, 1), (3, 0)}), frozenset({(3, 1), (1, 1), (2, 2)}), frozenset({(1, 1), (2, 1), (2, 2)}), frozenset({(1, 0), (2, 1)}), frozenset({(1, 0), (1, 1)}), frozenset({(1, 1)})]

----
Blind robot problem: 
Goal location: []
Start State: 
frozenset({(2, 4), (1, 2), (2, 1), (3, 4), (3, 1), (1, 1), (1, 4), (3, 3), (2, 2), (1, 0), (3, 2), (2, 5), (1, 3)})
attempted with search method Astar with heuristic state_size_heuristic
number of nodes visited: 45
solution length: 9
cost: 8
path: [frozenset({(2, 4), (1, 2), (2, 1), (3, 4), (3, 1), (1, 1), (1, 4), (3, 3), (2, 2), (1, 0), (3, 2), (2, 5), (1, 3)}), frozenset({(2, 4), (1, 2), (2, 1), (3, 1), (1, 1), (3, 3), (1, 0), (3, 2), (1, 3)}), frozenset({(1, 0), (2, 4), (1, 2), (2, 1), (3, 1), (1, 1), (3, 2)}), frozenset({(1, 2), (2, 1), (2, 2), (1, 0), (1, 1), (1, 4)}), frozenset({(1, 0), (1, 1), (1, 3), (2, 1)}), frozenset({(1, 0), (1, 1), (1, 3)}), frozenset({(1, 0), (1, 2)}), frozenset({(1, 0), (1, 1)}), frozenset({(1, 0)})]

----
Blind robot problem: 
Goal location: []
Start State: 
frozenset({(3, 1), (5, 4), (4, 6), (5, 1), (0, 2), (0, 5), (1, 0), (1, 6), (1, 3), (6, 2), (6, 5), (4, 2), (3, 0), (4, 5), (3, 3), (5, 6), (3, 6), (5, 3), (0, 1), (1, 2), (0, 4), (6, 1), (6, 4), (4, 1), (3, 5), (5, 2), (4, 4), (5, 5), (0, 0), (1, 1), (0, 3), (2, 0), (1, 4), (0, 6), (2, 3), (2, 6), (6, 0), (6, 6), (6, 3)})
attempted with search method Astar with heuristic state_size_heuristic
number of nodes visited: 10650
solution length: 19
cost: 18
path: [frozenset({(3, 1), (5, 4), (4, 6), (5, 1), (0, 2), (0, 5), (1, 0), (1, 6), (1, 3), (6, 2), (6, 5), (4, 2), (3, 0), (4, 5), (3, 3), (5, 6), (3, 6), (5, 3), (0, 1), (1, 2), (0, 4), (6, 1), (6, 4), (4, 1), (3, 5), (5, 2), (4, 4), (5, 5), (0, 0), (1, 1), (0, 3), (2, 0), (1, 4), (0, 6), (2, 3), (2, 6), (6, 0), (6, 6), (6, 3)}), frozenset({(1, 2), (6, 1), (5, 4), (4, 6), (5, 1), (6, 4), (0, 5), (1, 0), (1, 6), (1, 3), (4, 1), (5, 2), (6, 2), (5, 5), (6, 0), (6, 5), (1, 1), (2, 0), (1, 4), (3, 0), (2, 3), (4, 5), (3, 3), (2, 6), (5, 6), (3, 6), (6, 6), (6, 3)}), frozenset({(1, 2), (6, 1), (4, 6), (5, 1), (6, 4), (0, 5), (6, 2), (5, 5), (6, 0), (6, 5), (1, 1), (2, 0), (1, 4), (3, 0), (2, 3), (3, 3), (2, 6), (5, 6), (3, 6), (6, 6), (6, 3)}), frozenset({(1, 2), (6, 1), (4, 6), (6, 4), (3, 6), (0, 5), (6, 2), (6, 5), (1, 1), (1, 4), (3, 0), (3, 3), (5, 6), (6, 0), (6, 6), (6, 3)}), frozenset({(6, 2), (1, 2), (6, 5), (3, 1), (6, 1), (4, 6), (6, 4), (1, 4), (0, 6), (3, 3), (5, 6), (3, 6), (6, 6), (6, 3), (1, 3)}), frozenset({(6, 2), (1, 2), (6, 5), (6, 1), (4, 6), (6, 4), (1, 4), (2, 3), (3, 3), (5, 6), (6, 6), (1, 6), (6, 3), (4, 1)}), frozenset({(6, 2), (1, 2), (6, 5), (6, 1), (6, 4), (1, 4), (5, 1), (3, 3), (2, 6), (5, 6), (6, 6), (6, 3)}), frozenset({(6, 2), (6, 5), (6, 4), (1, 4), (3, 3), (2, 6), (5, 6), (6, 6), (6, 3), (1, 3), (5, 2)}), frozenset({(6, 5), (5, 3), (6, 4), (1, 4), (3, 3), (2, 6), (5, 6), (6, 6), (6, 3)}), frozenset({(5, 5), (0, 4), (5, 4), (4, 6), (2, 3), (5, 6), (5, 3), (1, 6)}), frozenset({(2, 3), (5, 5), (5, 6), (0, 5), (1, 6), (5, 4), (4, 6)}), frozenset({(4, 4), (4, 5), (0, 5), (3, 6), (4, 6), (1, 3), (0, 6)}), frozenset({(4, 5), (3, 6), (4, 6), (1, 4), (0, 6)}), frozenset({(0, 4), (2, 6), (3, 6), (3, 5), (0, 6)}), frozenset({(2, 6), (0, 6), (0, 5), (3, 6)}), frozenset({(2, 6), (3, 6), (0, 6)}), frozenset({(1, 6), (2, 6), (0, 6)}), frozenset({(1, 6), (0, 6)}), frozenset({(0, 6)})]

"""