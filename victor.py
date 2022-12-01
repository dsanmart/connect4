from utils import *
from rules import *
import json
import random
import time



# ----------- IMPLEMENTATION ----------- #

def find_all_solutions(board, player):
    """Finds all solutions of the opponent on the board.

    Returns:
        List with all solutions. Each solution represented as {squares = [(row, col), ...], groups = [(square1, square2, square3, square4), ...], rule = "rule_name"}
    """
    
    # Find all rules
    claimevens = find_claimevens(board)
    baseinverses = find_baseinverses(board)
    verticals = find_verticals(board)
    low_inverses = find_low_inverses(verticals)
    high_inverses = find_high_inverses(board)
    afterevens = find_after_evens(board, player)
    baseclaims = find_base_claims(board)
    befores = find_befores(board)
    special_befores = find_special_befores(board, befores)

    # Dictionary with all squares from the board with the threats from the current player that they belong to.
    square_to_groups = find_square_to_groups(board, player)

    solutions = []
    group_to_solutions = {}

    # Find all solutions for all rules
    for claimeven in claimevens:
        solution = from_claimeven(claimeven, square_to_groups) # get the solution for each claimeven
        if solution:
            solutions.append(solution)
            # Add all solutions to group_to_solutions
            for group in solution["groups"]:
                if group not in group_to_solutions: # check if the group is already in the dictionary
                    group_to_solutions[group] = []
                group_to_solutions[group].append(solution) # group_to_solutions--> Dict: key=group, value={squares,groups,rule}

    for baseinverse in baseinverses:
        solution = from_baseinverse(baseinverse, square_to_groups)
        if solution:
            solutions.append(solution)
            # Add all solutions to group_to_solutions
            for group in solution["groups"]:
                if group not in group_to_solutions:
                    group_to_solutions[group]=[]
                group_to_solutions[group].append(solution)

    for vertical in verticals:
        solution = from_vertical(vertical,square_to_groups)
        if solution:
            solutions.append(solution)
            for group in solution["groups"]:
                if group not in group_to_solutions:
                    group_to_solutions[group]=[]
                group_to_solutions[group].append(solution)
        
    for before in befores:
        solution = from_before(board, before, square_to_groups)
        if solution:
            solutions.append(solution)
            for group in solution["groups"]:
                if group not in group_to_solutions:
                    group_to_solutions[group]=[]
                group_to_solutions[group].append(solution)


    return solutions, group_to_solutions






# -------- HELPER FUNCTIONS FOR IMPLEMENTATION -------- #

def find_square_to_groups(board, player):
    """Returns:
        Dictionary with all squares as keys and all threats that contain that square as values.
        Format: {(row, col): [(square1, square2, square3, square4), ...]}
    """
    square_to_group={}
    threats = find_threats(board, player)
    for group in threats:
        for coord in group:
            if coord not in square_to_group:
                square_to_group[coord] = []
            square_to_group[coord].append(group)
    return square_to_group

def from_claimeven(claimeven, square_to_groups):
    """Converts a claimeven into a Solution.
    Returns:
    - Squares: upper an lower square
    - Groups: groups that contain the upper and lower square
    - Rules: rules that apply to the groups
    return format: {"squares": ((upper_square, lower_square)), "groups": [(square1, square2, square3, square4)], "rule": rule}
    """

    rule="claimeven"
    upper_square = (claimeven[0]+1, claimeven[1])
    lower_square = claimeven
    groups = square_to_groups[upper_square] # Find threats on the upper square
    if groups: # Must solve a group in order to be converted into a solution
        return {"squares": ((upper_square, lower_square)), "groups": groups, "rule":rule}

def from_baseinverse(baseinverse, square_to_groups):
    """Converts a Baseinverse into a Solution if there is one.
    Returns:
        solution = {"squares": ((square1, square2)), "groups": [(square1, square2, square3, square4)], "rule": rule}
    """
    square1=baseinverse[0]
    square2=baseinverse[1]
    
    if square1 in square_to_groups and square2 in square_to_groups:
        groups1, groups2 = square_to_groups[square1], square_to_groups[square2]
        groups_intersection = intersection(groups1, groups2)
        if groups_intersection:
            return {"squares": (square1, square2), "groups": groups_intersection, "rule": "baseinverse"}

def from_vertical(vertical,square_to_groups):
    '''Converts a vertical to a solution.
    Args: vertical: tuple with the coordinates of the lower square
    square_to_groups: dictionary with the groups of each square
    Returns: dictionary with the solution 
    Return format: {"squares": ((upper_row, upper_col), (lower_row, lower_col)), "groups": groups_intersection, "rule":"vertical"'''

    if vertical in square_to_groups and (vertical[0]+1, vertical[1]) in square_to_groups:
        upper_groups = square_to_groups[vertical] # Lower vertical square
        lower_groups = square_to_groups[(vertical[0]+1,vertical[1])] # Upper vertical square
        groups_intersection = intersection(upper_groups,lower_groups)
        if groups_intersection:
            return {"squares": ((vertical[0]+1,vertical[1]), vertical), "groups":groups_intersection,"rule":"vertical"}

def from_before(board, before, square_to_groups):
    """Converts before into a Solution.

    Required:
        Solves at least one new potential threat.
        This new potential threat must contain all successors of the empty squares in the before group.

    Args:
        before: {"group": (square1, square2, square3, square4), 
            "verticals": [((upper_row, upper_col), (lower_row, lower_col)), ...], 
            "claimeven": [((upper_row, upper_col), (lower_row, lower_col)), ...]}
    """
    # Find all empty square in the before group
    empty_squares_of_before = []
    for square in before["group"]:
        if board[square[0]][square[1]] == ".":
            empty_squares_of_before.append(square)
    
    # Find all successors of the empty squares in the before group
    empty_square_successors = []
    for square in empty_squares_of_before:
        empty_square_successors.append((square[0] + 1, square[1]))
    
    # Find all threats that contain all successors of the empty squares in the before group
    if empty_square_successors[0] in square_to_groups:
        threats = square_to_groups[empty_square_successors[0]]
        for square in empty_square_successors[1:]:
            if square not in square_to_groups:
                return None
            threats = set(threats).intersection(set(square_to_groups[square]))
    else:
        return None

    # If there is at least one threat containing all direct successors of the empty squares in the before group:
    if threats:
        squares = [empty_squares_of_before]

        for vertical in before["verticals"]:
            squares.append(vertical[0]) # Add upper square of vertical
            squares.append(vertical[1]) # Add lower square of vertical
            vertical_solution = from_vertical(vertical[1], square_to_groups)
            if vertical_solution:
                threats.update(vertical_solution["groups"])
        
        for claimeven in before["claimevens"]:
            squares.append(claimeven[0]) # Add upper square of claimeven
            squares.append(claimeven[1]) # Add lower square of claimeven
            claimeven_solution = from_claimeven(claimeven[1], square_to_groups)
            if claimeven_solution:
                threats.update(claimeven_solution["groups"])

        return {"squares": squares, "groups": threats, "rule": "before"}




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

    test_diagram = diagram6_10

    print("Board:")
    for row in board_flip(test_diagram):
        print(row)

    solutions, groups = find_all_solutions(test_diagram, "X")
    print(len(solutions), len(groups))
    #