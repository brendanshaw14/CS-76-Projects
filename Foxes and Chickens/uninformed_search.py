
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
        print(current)
        num_nodes_visited += 1

        # if this is the goal node, backchain 
        if current.state == search_problem.goal_state: 
            solution.path = backchain(current)
            solution.nodes_visited = num_nodes_visited
            return solution

        # otherwise, get its unvisited successors and add them to the queue
        else: 
            queued = "Queued: "
            for state in search_problem.get_successors(current.state): 
                # check if already visited
                if state not in visited_states:
                    visited_states.add(current.state)
                    queued += str(state) + ", "
                    queue.append(SearchNode(state, current))
            print(queued)
    solution.nodes_visited = num_nodes_visited
    return solution

# Backchain function for BFS to reconstruct the path
def backchain(goal):
    path = []
    current_node = goal

    # Start from the goal node and follow parent references
    while current_node is not None:
        path.append(str(current_node))
        current_node = current_node.parent

    # Reverse the path to get it in the correct order and return it
    path.reverse()
    return path

## Don't forget that your dfs function should be recursive and do path checking,
##  rather than memoizing (no visited set!) to be memory efficient

## We pass the solution along to each new recursive call to dfs_search
##  so that statistics like number of nodes visited or recursion depth
##  might be recorded
def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")
    #increment the nodes visited and add it to the path
    print(str(solution))
    print("adding " + str(node))
    solution.nodes_visited += 1
    solution.path.append(node.state)

    # base case: when the node is the goal_state
    if node.state == search_problem.goal_state:
        return solution

    # if depth limit reached: return the solution with an empty path
    if len(solution.path) == depth_limit:
        solution.path = []
        return solution

    # regular case: node isn't goal state
    for successor in search_problem.get_successors(node.state):
        if successor not in solution.path:
            new_node = SearchNode(successor)
            return dfs_search(search_problem, depth_limit, new_node, solution)



#def ids_search(search_problem, depth_limit=100):
    ## you write this part
