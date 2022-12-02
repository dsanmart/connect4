from utils import *
from rules import *

# ----------- RULES SOLUTIONS ----------- #

def find_all_solutions(board, player):
    """Finds all solutions the opponent can employ on the board.

    Returns:
        List with all solutions. Each solution represented as {squares = [(row, col), ...], groups = [(square1, square2, square3, square4), ...], rule = "rule_name"}
    """
    
    # Find all rules
    claimevens = find_claimevens(board)
    baseinverses = find_baseinverses(board)
    verticals = find_verticals(board)
    #afterevens = find_after_evens(board, player)
    #low_inverses = find_low_inverses(verticals)
    #high_inverses = find_high_inverses(board)
    #baseclaims = find_base_claims(board)
    befores = find_befores(board)
    #special_befores = find_special_befores(board, befores)

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






# -------- HELPER FUNCTIONS FOR RULES SOLUTIONS -------- #

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
    Return 
    {"squares": (empty_square_sucessor, empty_square_sucessor, empty_square_sucessor, upper, lower, upper, lower,...), "groups": threats, "rule": "before"}
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
            threats = set(threats).intersection(square_to_groups[square])
    else:
        return None

    # If there is at least one threat containing all direct successors of the empty squares in the before group:
    if threats:
        squares = empty_squares_of_before

        verticals = []
        for vertical in before["verticals"]:
            #squares.append(vertical[0]) # Add upper square of vertical
            #squares.append(vertical[1]) # Add lower square of vertical
            verticals.append(vertical)
            vertical_solution = from_vertical(vertical[1], square_to_groups)
            if vertical_solution:
                set(threats).update(vertical_solution["groups"])
        
        claimevens = []
        for claimeven in before["claimevens"]:
            #squares.append(claimeven[0]) # Add upper square of claimeven
            #squares.append(claimeven[1]) # Add lower square of claimeven
            claimevens.append(claimeven)
            claimeven_solution = from_claimeven(claimeven[1], square_to_groups)
            if claimeven_solution:
                set(threats).update(claimeven_solution["groups"])


        return {"squares": squares, "verticals": verticals, "claimevens": claimevens, "groups": threats, "rule": "before"}







# -------- SOLUTIONS FOR WINNER THREATS -------- #
def find_all_win_conditions(board, player):
    """Returns all win conditions for the opponent can employ on the board.
    Returns:
        List of solutions that are win conditions.
    """
    odd_threats = find_odd_threats(board)
    #threat_combinations = find_threat_combinations(board) # To be fixed

    solutions = []
    square_to_groups = find_square_to_groups(board, player)
    for odd_threat in odd_threats:
        solution = from_odd_threat(board, odd_threat, square_to_groups)
        solutions.append(solution)
    
    return solutions


def from_odd_threat(board, odd_threat, square_to_groups):
    """Converts an odd threat into a Solution.
    Returns:
        solution = {"squares": ((square1, square2)), "groups": [(square1, square2, square3, square4)], "rule": rule}
    """
    groups_solved = []
    
    # Find playable square from the group, if any.
    playable_squares = possible_actions(board)
    playable_group_square = None
    for square in odd_threat["group"]:
        if square in playable_squares:
            playable_group_square = square_to_groups[square]
    # Find the empty square from the group
    empty_group_square = None
    for square in odd_threat["group"]:
        if board[square[0]][square[1]] == ".":
            empty_group_square = square
    # Add Groups containing any odd Square up to the Odd Threat that are not directly playable.
    if playable_group_square:
        for row in range(odd_threat["empty_odd_square"][0], odd_threat["directly_playable"][0], 2):
            square = (row, odd_threat["empty_odd_square"][1])
            groups_solved.append(square)

    # Add Groups containing suares above the odd threat
    for row in range(5, odd_threat["empty_odd_square"][0], 1):
        square = (row, odd_threat["empty_odd_square"][1])
        groups_solved.append(square)
    
    return {"squares": [odd_threat["empty_odd_square"]], "groups": groups_solved, "rule": "odd_threat"}





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
    player = "X"
    print("Board:")
    for row in board_flip(test_diagram):
        print(row)

    solutions, groups = find_all_solutions(test_diagram, "X")
    print("rules solutions", len(solutions), len(groups))
    win_solutions = find_all_win_conditions(test_diagram, player)
    print("win solutions", len(win_solutions))
    print("win_solutions", win_solutions)