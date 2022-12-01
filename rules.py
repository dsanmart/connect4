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



if __name__ == "__main__":
    test_diagram = diagram6_10
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
    print("Special_befores: ", special_befores)