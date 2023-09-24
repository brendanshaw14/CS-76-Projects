from SearchSolution import SearchSolution
from heapq import heappush, heappop

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost


    def priority(self):
        return self.heuristic + self.transition_cost


    def __str__(self):
        return "State: " + str(self.state)

    # comparison operator, needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn, test_path):
    # I'll get you started:
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem, search_problem.start_state))
    test_path.append(start_node.state)
    frontier = []
    heappush(frontier, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    # this holds states that have been visited with their costs
    visited_cost = {}
    visited_cost[start_node.state] = 0

    # loop: while there are still items in the frontier:
    while frontier: 
        print(str(visited_cost))
        # get the next node
        print("Frontier: ")
        for node in frontier:
            print(node.state, end=" ")
        print()
        current_node = heappop(frontier)
        solution.nodes_visited += 1
        test_path.append(current_node.state)
        visited_cost[current_node.state] = current_node.transition_cost

        # update the problem, if necessary
        search_problem.update(current_node.state)

        # if it is the solution, backchain:
        if search_problem.goal_test(current_node.state):
            solution.path = backchain(current_node)
            return solution

        # get the successor states
        successors = search_problem.get_successors(current_node.state)
        print("Current " + str(current_node))
        print("Successors: " + str(successors))
        # loop through each successor 
        for successor in successors:        
            # calcuate the new cost
            new_cost = current_node.transition_cost + 1
            # if visited 
            if successor in visited_cost and visited_cost[successor] <= new_cost:
                continue
            else:
                new_node = AstarNode(successor, heuristic_fn(search_problem, successor), current_node, new_cost) 
                heappush(frontier, new_node)

    # if the frontier is empty, return the empty solution
    solution.path = []
    return solution

if __name__ == "__main__":
    new_node = AstarNode((3, 3), 5)
    print(new_node)

