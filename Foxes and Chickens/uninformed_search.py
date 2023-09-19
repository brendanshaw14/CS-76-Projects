
from collections import deque
from SearchSolution import SearchSolution

# you might find a SearchNode class useful to wrap state objects,
#  keep track of current depth for the dfs, and point to parent nodes
class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

    def __str__ (self):
        return "State: " + str(self.state) # + ", Parent: " + str(self.parent)


# you might write other helper functions, too. For example,
#  I like to separate out backchaining, and the dfs path checking functions

def bfs_search(search_problem):
    # initialize queue, add the start node
    queue = deque()
    queue.append(SearchNode(search_problem.start_state)) 

    # visted satates set to avoid revisits
    visited_states = set() 
    visited_states.add(search_problem.start_state) 

    # track how many nodes have been visited and initialize the solution
    solution = SearchSolution(search_problem, "breadth-first-search")
    num_nodes_visited = 0

    # begin the search
    while queue: 
        # get the next node in queue and increment num_nodes_visited
        current = queue.popleft()
        num_nodes_visited += 1

        # if this is the goal node, backchain 
        if current.state == search_problem.goal_state: 
            solution.path = backchain(current)
            solution.nodes_visited = num_nodes_visited
            return solution

        # otherwise, get its unvisited successors and add them to the queue
        else: 
            for state in search_problem.get_successors(current.state): 
                # check if already visited
                if state not in visited_states:
                    visited_states.add(current.state)
                    queue.append(SearchNode(state, current))
    solution.nodes_visited = num_nodes_visited
    return solution

# Backchain function for BFS to reconstruct the path
def backchain(goal):
    path = []
    current_node = goal

    # Start from the goal node and follow parent references
    while current_node is not None:
        path.append(current_node.state)
        current_node = current_node.parent

    # Reverse the path to get it in the correct order and return it
    path.reverse()
    return path


def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "depth-first search")

    # base case 1: when the node is the goal_state: add to the path
    if node.state == search_problem.goal_state:
        solution.nodes_visited += 1
        solution.path.append(node.state)
        return solution

    # base case 2: if depth limit reached or node is a leaf: go to the next branch at same depth, if existent, if not, go back up the tree
    successors = search_problem.get_successors(node.state)
    if len(solution.path) == depth_limit or len(successors) == 0:
        return solution

    # recursive case below: add the current node
    solution.nodes_visited += 1
    solution.path.append(node.state)

    # loop through its successors
    for successor in successors:
        #if the successor is not alreadyin the path, call dfs on it
        if successor not in solution.path:
            prev_length = len(solution.path)
            new_node = SearchNode(successor)
            dfs_search(search_problem, depth_limit, new_node, solution)

            # if the dfs call updates the solution to a path length larger than the current one, return it. 
            # otherwise, go to the next successor.
            if len(solution.path) == prev_length:
                continue
            else:
                return solution

    # if no successors returned longer paths, return the same path
    solution.path.pop()
    return solution


def ids_search(search_problem, depth_limit=100):
    # keep track of the nodes visited and the path
    num_nodes_visited = 0
    path = []
    # iteratively call the ids search
    for i in range(1, depth_limit + 1):
        # at each call, save the number of nodes visited
        dfs = dfs_search(search_problem, i)
        num_nodes_visited += dfs.nodes_visited

        # if there was a path returned, save it and stop the loop 
        if len(dfs.path) > 0: 
            path = dfs.path
            break

    # create the solution object and return it
    solution = SearchSolution(search_problem, "iterative-deepening search")
    solution.nodes_visited = num_nodes_visited
    solution.path = path
    return solution
