from utils import *
from rules import *
from combination import combination_allowed
from solution import find_all_solutions, find_all_win_conditions


def find_chosen_set(node_graph, problems, disallowed_solutions, used_solutions, num_not_solutions):
    """Finds a set of Solutions that solves all Problems.
    Args:
        node_graph: a Dictionary of groups or Solutions to all Solutions they are connected to.
        problems: a set of groups that need to be solved.
        solutions: a set of Solutions available to solve problems.
        used_solutions: a set of Solutions that have already been used to solve problems outside problems.
    Returns:
        chosen_set: a set of Solutions that solves all Problems, if it exists...
    """
    # If there are no more Problems, we have found a set of Solutions.
    if len(problems) == 0:
        print("Eureka!")
        return used_solutions.copy()
    if len(problems) <= num_not_solutions:
        print("Eureka2!")
        return used_solutions.copy()
    #print("Problems", len(problems))
    # Recursive case
    #print(len(problems), num_not_solutions)
    most_difficult_node = node_with_least_number_of_neighbors(node_graph, problems, disallowed_solutions)
    most_difficult_node_usable_solutions = node_graph[most_difficult_node]
    for solution in disallowed_solutions:
        if solution in most_difficult_node_usable_solutions:
            most_difficult_node_usable_solutions.remove(solution)
    
    for solution in most_difficult_node_usable_solutions:
        # Choose
        #print(solution["rule"])
        used_solutions.append(solution)
        hashable_solution = (solution["rule"], tuple(solution["groups"]), tuple(solution["squares"]))
        # New disallowed solutions
        new_disallowed_solutions = []
        for disallowed_solution in disallowed_solutions:
            new_disallowed_solutions.append(disallowed_solution)
        new_disallowed_solutions.append(node_graph[hashable_solution])

        # Recurse
        for solved_problem in solution["groups"]:
            if solved_problem in problems:
                problems.remove(solved_problem)
        chosen_set = find_chosen_set(
            node_graph,
            problems,
            new_disallowed_solutions,
            used_solutions,
            num_not_solutions)
        
        #print("backtrack")
        # Unchoose with backtracking
        used_solutions.remove(solution)

        if chosen_set is not None:
            return chosen_set




def evaluate(board, player):
    """Evaluate the board for the AI player."""
    player_groups = set(find_threats(board, player))
    all_solutions, group_to_solutions = find_all_solutions(board, player)
    solved_groups = [group for group in group_to_solutions]
    
    if player == "O":
        node_graph = create_node_graph(all_solutions)
        #print(len(node_graph), len(all_solutions))
        return find_chosen_set(
             node_graph=node_graph,
             problems=player_groups,
             disallowed_solutions=[],
             used_solutions=[],
             num_not_solutions=len(player_groups)-len(solved_groups))
    else:
        #print("Solved threats", len(solved_groups))
        #print("Number of threats", len(player_groups))
        node_graph = create_node_graph(all_solutions)
        #print(len(node_graph), len(all_solutions))
        return find_chosen_set(
             node_graph=node_graph,
             problems=player_groups,
             disallowed_solutions=[],
             used_solutions=[],
             num_not_solutions=len(player_groups)-len(solved_groups))


def create_node_graph(solutions):
    """Creates a graph connecting Problems and Solutions.
    Required:
        Every Problem is connected to all Solutions that solve it.
        No Problem is connected to another Problem.
        Every Solution is connected to all Solutions that cannot be combined with it.
    Args:
        solutions: an iterable of Solutions.
    Returns:
        node_graph: a Dictionary of groups or Solutions to all Solutions they are connected to.
            Every Solution will at least be connected to itself.
    """
    node_graph = {}

    for solution in solutions:
        # Connect solution to all Problems it solves.
        for group in solution["groups"]:
            if group not in node_graph:
                node_graph[group] = []
            node_graph[group].append(solution)

        # TBD - Combination.py to Connect all Solutions that cannot work with solution to solution.
        hashable_sol = (solution["rule"], tuple(solution["groups"]), tuple(solution["squares"]))
        node_graph[hashable_sol] = []
        for other in solutions:
            if not combination_allowed(solution, other):
                node_graph[hashable_sol].append(other)
    return node_graph



# ----------- TESTING ----------- #

if __name__ == "__main__":
    initial_board = board_flip([
        [".", ".", ".", ".", ".", ".", "."], 
        [".", ".", ".", ".", ".", ".", "."], 
        [".", ".", ".", ".", ".", ".", "."], 
        [".", ".", ".", ".", ".", ".", "."], 
        [".", ".", ".", ".", ".", ".", "."], 
        [".", ".", ".", ".", ".", ".", "."]])

    diagram6_1 = board_flip([
        [".", ".", ".", "X", ".", ".", "."], 
        [".", ".", ".", "O", ".", ".", "."], 
        [".", ".", ".", "X", ".", ".", "."], 
        [".", ".", ".", "O", ".", ".", "."], 
        [".", ".", ".", "X", ".", ".", "."], 
        [".", ".", "X", "O", "O", ".", "."]])

    diagram6_5 = board_flip([
        [".", ".", ".", ".", ".", ".", "."], 
        [".", ".", ".", ".", ".", ".", "."], 
        [".", "X", "O", "O", "O", ".", "."], 
        [".", "O", "X", "X", "X", ".", "."], 
        ["O", "X", "X", "O", "O", ".", "."], 
        ["O", "X", "X", "X", "O", ".", "."]])

    diagram6_10 = board_flip([
        [".", ".", ".", ".", ".", ".", "."], 
        [".", ".", "O", ".", ".", ".", "."], 
        [".", ".", "X", ".", ".", ".", "."], 
        [".", ".", "O", ".", ".", ".", "."], 
        [".", ".", "X", "O", ".", ".", "."], 
        [".", ".", "X", "X", "O", ".", "."]])
    
    diagram8_1 = board_flip([
        [".", ".", ".", ".", ".", ".", "."], 
        [".", ".", ".", ".", ".", ".", "."], 
        [".", ".", ".", "O", "X", ".", "."], 
        [".", "X", "X", "X", "O", ".", "."], 
        [".", "X", "O", "O", "O", ".", "."], 
        ["X", "O", "X", "X", "O", ".", "."]])

    test_diagram = diagram8_1
    player = "O"
    print("Board:")
    for row in board_flip(test_diagram):
        print(row)
    evaluated_solutions = evaluate(test_diagram, player)
    print("Solutions:", evaluated_solutions)
    print("Solutions:", len(evaluated_solutions))