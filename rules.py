from utils import *
import time

# ----------- GAME RULES ----------- #

def find_claimevens(board):
    """Finds all the claimable evens on a board. Can be used to determine a winner or draw.

    Required: 2 squares directly above each other. Both squares must be empty. The upper square must be even.
    
    Returns:
        List with all the claimevens.
        Claimeven represented with (row, col) of the lower (odd) square.
    """
    claimevens = []
    for row in range(0, len(board), 2): # Steps of 2 to reach only even rows
        for col in range(len(board[0])):
            if board[row][col] == '.':
                claimevens.append((row, col))

    return claimevens

def find_baseinverses(board):
    """Finds all the baseinverses on a board.

    Required: 2 directly playable squares.
    
    Returns:
        List with all the tuples that contain both squares
    """
    baseinverses = []
    playable_actions = possible_actions(board)

    # Try all different combinations of directly playable squares.
    for square1 in playable_actions:
        for square2 in playable_actions:
            if square1 != square2 and is_true_threat((square1, square2)):
                # Note threats are only checked if coords are viable.
                # Checking whether the threat is real with current board state could benefit the algorithm.
                inverted_baseinverse = (square2, square1)
                if inverted_baseinverse not in baseinverses: # Avoid duplicates
                    baseinverses.append((square1, square2))

    return baseinverses

def find_verticals(board):
    """Finds all the verticals on a board. Function that replaces the claimeven when necessary.

    Required: 2 squares directly above each other. Both squares must be empty. The upper square must be odd.
    
    Returns:
        List with all the verticals.
        Vertical represented with (row, col) of the lower (even) square.
    """
    verticals = []
    for row in range(1, len(board)-1, 2): # Steps of 2 to reach only odd rows
        for col in range(len(board[0])):
            if board[row][col] == '.':
                verticals.append((row, col))
    return verticals

def find_low_inverses(verticals):
    """Finds all the low_inverses on a board. Returns all combinations made by 2 verticals that are possible threats.
    
    Required:
        2 different columns, each with 2 squares lying above each other.
        All for squares must be empty.
        Both columns, the upper square is odd (as in verticals).
    
    Returns:
        List with tuples of low_inverses that are possible threats.
    """
    low_inverses = []

    # Try all different combinations of verticals.
    for vertical1 in verticals:
        for vertical2 in verticals:
            if vertical1 != vertical2 and is_true_threat((vertical1, vertical2)):
                inverted_low_inverse = (vertical2, vertical1)
                if inverted_low_inverse not in low_inverses: # Avoid duplicates
                    low_inverses.append((vertical1, vertical2))
    return low_inverses

def find_high_inverses(board):
    """Finds all the high_inverses on a board. Could be seen as combinations of Claimeven + Lowinverse (with claimeven at the top).
    
    Required:
        Two different columns, each with 3 squares lying directly above each other.
        All six squares are empty.
        In both columns the upper square is even
    
    Returns:
        List with tuples of high_inverses that are possible threats.
        Inside each tuple, 2 coords that represent lowest square of the group in each column.
    """
    columns = [] # List of columns that have 3 squares above each other (with even top square)
    for row in range(1, len(board)-2, 2):
        for col in range(len(board[0])):
            # If lower square of the highinverse is empty
            if board[row][col] == '.' and col not in columns:
                columns.append(col)

    high_inverses = []
    for i in range(len(columns)):
        col1 = columns[i]
        for col2 in columns[i+1:]:
            for row_col1 in range(1, len(board)-2, 2):
                for row_col2 in range(1, len(board)-2, 2):
                    if board[row_col1][col1] == '.' and board[row_col2][col2] == '.' and is_true_threat(((row_col1, col1), (row_col2, col2))):
                        inverted_highinverse = ((row_col2, col2), (row_col1, col1))
                        if inverted_highinverse not in high_inverses: # Avoid duplicates
                            high_inverses.append(((row_col1, col1), (row_col2, col2)))
    return high_inverses

def find_after_evens(board, player):
    """Finds all the after evens on a board.

    Required: 
        A group which can be completed by the controller of the Zugzwang, using only the even
        squares of a set of Claimevens. This group is called the Aftereven group. 
        The columns in which the empty squares lie are called the Aftereven columns.
    
    Returns:
        A list of all afterevens. Each afterevne is represented by a list of tuples with coords (row, col) for the 4 squares.
    """
    if player == "X":
        opponent = "O"
    else:
        opponent = "X"
    
    afterevens = []
    for row in range(1, len(board), 2):
        for col in range(len(board[0])-3):
            if ((board[row][col] == '.' or board[row][col] == opponent) 
            and (board[row][col+1] == '.' or board[row][col+1] == opponent) 
            and (board[row][col+2] == '.' or board[row][col+2] == opponent) 
            and (board[row][col+3] == '.' or board[row][col+3] == opponent)):
                afterevens.append([(row, col), (row, col+1), (row, col+2), (row, col+3)])

    return afterevens

def find_base_claims(board):
    """Returns the baseclaim of the board.

    Required:
        Three directly playable squares and the square above the second playable square.
        The non-playable (fourth) square must be even.
    
    Returns:
        List with all baseclaims. Each baseclaim group represented as (square1, square2, square3, square4)
    """
    baseclaims = []
    playable_actions = possible_actions(board)

    # Try all different combinations of directly playable squares.
    for i in range(len(playable_actions)):
        square1 = playable_actions[i]
        for j in range(len(playable_actions[i+1:])):
            square2 = playable_actions[j]
            for square3 in playable_actions[j+1:]:
                if square1 != square2 and square1 != square3 and square2 != square3:
                    square4 = (square2[0]+1, square2[1])
                    if square4[0]%2 == 1: # If in even row
                        if is_true_threat((square1, square4)) and is_true_threat((square2, square3)):
                            baseclaims.append((square1, square2, square3, square4))
                        if is_true_threat((square3, square4)) and is_true_threat((square2, square1)):
                            baseclaims.append((square3, square2, square1, square4))
    return baseclaims

# Helper function for find_befores
def is_true_befores(board, threat):
    for square in threat:
        # If square is empty and in upper row
        if board[square[0]][square[1]] == '.' and square[0] == 5: 
            return False
    return True

def add_before_variations(board, group, empty_squares, verticals, claimevens):
    """Adds all Before variations with group as the Before group to befores.
    This is a Recursive Backtracking algorithm.    """
    # Base Case.

    if len(empty_squares) == 0:
        #if len(verticals) > 0:
            # Only add the Before if there is at least one Vertical; otherwise, an Aftereven is better.
        before = {"group": group, "verticals": verticals, "claimevens": claimevens}
        return before

    if len(empty_squares) > 0:
        # Recursive Case.
        square = empty_squares.pop()  # Remove a square from empty_squares.
        square_below = (square[0]-1, square[1])
        square_above = (square[0]+1, square[1])

        # Depending on whether square is odd or even, we try to create a Vertical or Claimeven respectively.
        if square[0] % 2 == 0:  # square is odd.
            if square_below[0] >= 0 and board[square_below[0]][square_below[1]] == '.': # If square below exists and is empty:
                # Create a Vertical with square as the upper square.
                vertical = (square, square_below) # (upper, lower)
                # Choose.
                verticals.append(vertical)
                # Recurse.
                return add_before_variations(board, group, empty_squares, verticals, claimevens)


        else:  # square is even.
            # Since square is even, we are guaranteed that square_below is valid
            # because board must have an even number of rows.
            if square_below[0] >= 0 and board[square_below[0]][square_below[1]] == '.':
                # Create a Claimeven with square as the upper square.
                claimeven = (square, square_below)
                # Choose.
                claimevens.append(claimeven)
                # Recurse.
                return add_before_variations(board, group, empty_squares, verticals, claimevens)
            else:
                # If it's even but vertical is not allowed, we create a Vertical with even square as the lower square.
                if square_above[0] <= 5: # If the upper square is in the board
                    vertical = (square_above, square)
                    # Choose.
                    verticals.append(vertical)
                    # Recurse.
                    return add_before_variations(board, group, empty_squares, verticals, claimevens)

    empty_squares.append(square)

def find_befores(board, player="X"):
    """Returns all the befores on a board. These are combinations of claimevens and verticals.

    Required:
        A group without tokens from the opponent called before group.
        All empty squares in the before group should not lie in the upper row of the board.

    Returns:
        List with all befores. Each before group represented as a dictionary with keys "group", "verticals" and "claimevens".
        before: {"group": (square1, square2, square3, square4), 
            "verticals": [((upper_row, upper_col), (lower_row, lower_col)), ...], 
            "claimeven": [((upper_row, upper_col), (lower_row, lower_col)), ...]}
    """
    if player == "X":
        opponent = "O"
    else:
        opponent = "X"
    
    opponent_threats = find_threats(board, opponent)

    befores = []
    for threat in opponent_threats:
        # If vertical, skip it
        if (threat[0][0] - threat[1][0]) != 0 and (threat[0][1] - threat[1][1]) == 0:
            continue
        if is_true_befores(board, threat):
            # Find all empty square in the threat (before group)
            empty_squares_of_threat = []
            for square in threat:
                if board[square[0]][square[1]] == ".":
                    empty_squares_of_threat.append(square)
            # Find all verticals and claimevens in the threat
            before = add_before_variations(board, threat, empty_squares_of_threat, [], [])
            if before:
                befores.append(before)
    return befores

# Helper function for special before
def is_true_special_before(board, external_playable_square, before_group):
    """Function to check requirements for a special before.
        Directly playable square is not in the same column as any square of the Beforegroup.
    """
    empty_squares = []
    for square in before_group:
        if board[square[0]][square[1]] == ".":
            empty_squares.append(square)
    for square in empty_squares:
        # If in same column or not a possible threat
        if external_playable_square[1] == square[1] or not is_true_threat((external_playable_square, (square[0]+1, square[1]))):
            return False
    return True


def find_special_befores(board, befores):
    """Returns all the special befores on a board. This is a special version of the before.

    Required:
        A group without tokens from the opponent called Specialbefore group.
        A directly playable square in another column.
        All empty squares in the Specialbefore group should not lie in the upper row of the board.
        One empty square of the Beforegroup must be playable.
    
    Returns:
        List with all special befores. Each special before group represented as (directly playable square in another column, before_group)
    """
    external_playable_actions = possible_actions(board)
    special_befores = []
    for external_action in external_playable_actions:
        for before in befores:
            before_group = before["group"]
            playable_squares_in_before_group = [] # List of playable squares in the before group
            for square in before_group:
                if square == external_action:
                    playable_squares_in_before_group.append(square)
            for internal_playable_square in playable_squares_in_before_group:
                for external_action in external_playable_actions:
                    if is_true_special_before(board, external_action, before_group):
                        special_befores.append({"squares":before_group, "external_playable_square": external_action, "internal_playable_square": internal_playable_square})
    return special_befores








# ----------- WINNER RULES ----------- #
def find_odd_threats(board):
    """Returns all the odd threats on a board.
    odd_threat = {"group": (square1, square2, square3, square4), "empty_odd_square": empty_square, "directly_playable": playable_square}
    """
    playable_actions = possible_actions(board)
    
    odd_threats = []
    for threat in find_threats(board, player="X"): 
        # Find all empty square in the threat
        empty_squares_of_threat = []
        for square in threat:
            if board[square[0]][square[1]] == ".":
                empty_squares_of_threat.append(square)
        
        # If there is only 1 empty square in the group, the square is not directly playable, and it is an odd square:
        if (len(empty_squares_of_threat) == 1 and
             empty_squares_of_threat[0] not in playable_actions and 
             empty_squares_of_threat[0][0] % 2 == 0): # If only left square in threat and is in odd row
            empty_square = empty_squares_of_threat[0]
            for square in playable_actions:
                if square[1] == empty_square[1]: # If in same column
                    playable_square = square

            odd_threat = {"group": threat, "empty_odd_square": empty_square, "directly_playable": playable_square}
            odd_threats.append(odd_threat)
    return odd_threats


# Helper function for threat combinations
def create_threat_combination(even_threat, odd_threat, playable_actions):
    """Returns a threat combination if it is valid. Otherwise returns None.
    Returnned threat combination format:
        {"even_threat": even_threat, 
        "odd_threat": odd_threat, 
        "shared_square": shared_square,
        "even_squre": even_threat["even_square"],
        "odd_square": odd_unshared_square,
        "directly_playable_square_shared_col": directly_playable_square_shared_col,
        "directly_playable_square_stacked_col": directly_playable_square_stacked_col, 
        "threat_combination_type": threat_combination_type}
    """
    odd_unshared_square = None
    if even_threat["odd_square"] == odd_threat["odd_square1"]:
        odd_unshared_square = odd_threat["odd_square2"]
    if even_threat["odd_square"] == odd_threat["odd_square2"]:
        odd_unshared_square = odd_threat["odd_square1"]
    
    shared_square = even_threat["odd_square"]
    if odd_unshared_square is None:
        return None
    if even_threat["even_square"][1] != odd_unshared_square[1]:
        return None
    # If the shared square is directly playable, return None.
    if shared_square in playable_actions:
        return None

    if even_threat["even_square"][0] - odd_unshared_square[0] == 1:
        threat_combination_type = "EvenAboveOdd"
    elif even_threat["even_square"][0] - odd_unshared_square[0] == -1:
        if even_threat["even_square"] in playable_actions:
            threat_combination_type = "OddAboveDirectlyPlayableEven"
        else:
            threat_combination_type = "OddAboveNotDirectlyPlayableEven"
    else:
        return None

    directly_playable_square_shared_col = None
    directly_playable_square_stacked_col = None
    for square in playable_actions:
        if square[1] == even_threat["odd_square"][1]:
            directly_playable_square_shared_col = square
        if square[1] == odd_unshared_square[1]:
            directly_playable_square_stacked_col = square

    return {"even_threat": even_threat, 
        "odd_threat": odd_threat, 
        "shared_square": shared_square,
        "even_squre": even_threat["even_square"],
        "odd_square": odd_unshared_square,
        "directly_playable_square_shared_col": directly_playable_square_shared_col,
        "directly_playable_square_stacked_col": directly_playable_square_stacked_col, 
        "threat_combination_type": threat_combination_type}

def find_threat_combinations(board):
    """Returns all the threat combinations for white if they exist. If there is multiple combinations, picks one at random.
    """
    white_threats = find_threats(board, player="X")

    even_threats = []
    odd_threats = []
    for threat in white_threats:
        empty_squares_of_threat = []
        for square in threat:
            if board[square[0]][square[1]] == ".":
                empty_squares_of_threat.append(square)
            
        if len(empty_squares_of_threat) != 2:
            continue
            
        square1, square2 = empty_squares_of_threat[0], empty_squares_of_threat[1]
        if square1[0] % 2 == 0 and square2[0] % 2 == 0: # If odd threat
            odd_threats.append({"threat": threat, "odd_square1": square1, "odd_square2": square2})
        elif square1[0] % 2 == 1 and square2[0] % 2 == 0: # If even threat with square1 as the even square
            even_threats.append({"threat": threat, "odd_square": square2, "even_square": square1})
        elif square1[0] % 2 == 0 and square2[0] % 2 == 1: # If even threat with square1 as the odd square
            even_threats.append({"threat": threat, "odd_square": square1, "even_square": square2})
            
    threat_combinations = []
    playable_actions = possible_actions(board)
    for even_threat in even_threats:
        for odd_threat in odd_threats:
            threat_combination = create_threat_combination(even_threat, odd_threat, playable_actions)


    return threat_combinations


# ----------- TESTING ----------- #

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

diagram8_1 = board_flip([
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", "O", "X", ".", "."], 
    [".", "X", "X", "X", "O", ".", "."], 
    [".", "X", "O", "O", "O", ".", "."], 
    ["X", "O", "X", "X", "O", ".", "."]])

diagram8_3 = board_flip([
    [".", ".", ".", "O", "O", ".", "."], 
    [".", ".", ".", "X", "X", ".", "."], 
    [".", ".", ".", "O", "O", ".", "."], 
    [".", ".", ".", "X", "X", ".", "."], 
    [".", ".", ".", "O", "X", ".", "."], 
    [".", ".", ".", "X", "O", ".", "X"]])

if __name__ == "__main__":
    test_diagram = diagram8_3
    player = "X"
    print("Board:")
    for row in board_flip(test_diagram):
        print(row)
    print("Player:", player)
    print("Possible actions: ", possible_actions(test_diagram))

    start = time.time()
    claimevens = find_claimevens(test_diagram)
    baseinverses = find_baseinverses(test_diagram)
    verticals = find_verticals(test_diagram)
    low_inverses = find_low_inverses(verticals)
    high_inverses = find_high_inverses(test_diagram)
    afterevens = find_after_evens(test_diagram, player)
    baseclaims = find_base_claims(test_diagram)
    befores = find_befores(test_diagram, player)
    special_befores = find_special_befores(test_diagram, befores)
    odd_threats = find_odd_threats(test_diagram)
    threat_combinations = find_threat_combinations(test_diagram)
    end = time.time()

#    print("Seconds taken: ", end - start)
#    print("Claimevens: ", claimevens)
#    print("Baseinverses: ", baseinverses)
#    print("Verticals: ", verticals)
#    print("Low_inverses: ", low_inverses)
#    print("High_inverses: ", high_inverses)
#    print("Afterevens: ", afterevens)
#    print("Baseclaims: ", baseclaims)
#    print("Befores: ", befores)
#    print("Special_befores: ", special_befores)
    print("Odd_threats: ", odd_threats)
    print("Threat_combinations: ", threat_combinations)