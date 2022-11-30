from functools import reduce
from copy import copy, deepcopy
import json
import random
import time

class Game:
    def __init__(self, state, status, player):
        self.state = state
        self.status = status
        self.player = player

    def is_waiting(self):
        return self.status == 'waiting'

    def is_end(self):
        return self.status == 'complete'
    
    def get_board(self):
        return json.loads(self.state)

    def get_winner(self):
        return None

    def actions(self):
        return []

    def print(self):
        print(self.state)


class ConnectFour(Game):
    def __init__(self, state, status, player):
        Game.__init__(self, state, status, player)

    def actions(self):
        return [] # this should return the possible actions

    def get_winner(self):
        return '.' # this should return the actual winner

    def other_player(self):
        if self.player == 'O': return 'X'
        if self.player == 'X': return 'O'

    def print_game(self):
        print(self.state)


# ----------- HELPER FUNCTIONS ----------- #

def update_board(board, col, player):
    """Updates a board with a new move.
    
    Args:
        board: a list of lists representing the board
        col: the column to place the piece
        player: the player making the move
    
    Returns:
        A new board with the move made."""

    new_board = deepcopy(board)
    for i in range(5, -1, -1):
        if new_board[i][col] == '.':
            new_board[i][col] = player
        return new_board
    return None

def board_flip(board):
    """Returns a new board with the board flipped vertically.
    This allows accessing the lower row as the first item in the list."""

    new_board = deepcopy(board)
    new_board.reverse()
    return new_board

def possible_actions(board):
    """Returns a list of all directly playable actions (row, col) on a board."""
    actions = []
    for col in range(len(board[0])):
        for row in range(len(board)):
            if board[row][col] == '.':
                actions.append((row,col))
                break
    # playable_cols = [x[1] for x in actions]
    return actions

def is_true_threat(threat):
    """Checks if the threat coordinates are true.
    
    Args:
        threat: a tuple of 2 tuples representing the threat coordinates of the start and end of the threat.
    """
    threat_start = threat[0]
    threat_end = threat[1]

    # Filter out squares further than 3 positions apart.
    row_diff = threat_start[0] - threat_end[0]
    if abs(row_diff) > 3:
        return False
    col_diff = threat_start[1] - threat_end[1]
    if abs(col_diff) > 3:
        return False
    
    # If the two squares are in the same row or column, it is possible for them to be connected.
    # The two squares can be connected diagonally only if row_diff and col_diff are the same.
    if row_diff == 0 or col_diff == 0:
        return True
    if abs(row_diff) == abs(col_diff):
        return True
    return False

def find_threats(board, player):
    groups = []
    # first we need to find the possible groups in the board
    
    # Check for vertical
    for i in range(3):
        for j in range(7):
            if board[i][j] == player or board[i][j]== ".":
                if board[i+1][j] == player or board[i+1][j]== ".":
                    if board[i+2][j] == player or board[i+2][j]== ".":
                        if board[i+3][j] == player or board[i+3][j]== ".":
                            groups.append([(i,j),(i+1,j),(i+2,j),(i+3,j)])
    
    # Check for horizontal
    for i in range(6):
        for j in range(4):
            if board[i][j] == player or board[i][j]== ".":
                if board[i][j+1] == player or board[i][j+1]== ".":
                    if board[i][j+2] == player or board[i][j+2]== ".":
                        if board[i][j+3] == player or board[i][j+3]== ".":
                            groups.append([(i,j),(i,j+1),(i,j+2),(i,j+3)])

    # Check for diagonal right
    for i in range(3):
        for j in range(4):
            if board[i][j] == player or board[i][j]== ".":
                if board[i+1][j+1] == player or board[i+1][j+1]== ".":
                    if board[i+2][j+2] == player or board[i+2][j+2]== ".":
                        if board[i+3][j+3] == player or board[i+3][j+3]== ".":
                            groups.append([(i,j),(i+1,j+1),(i+2,j+2),(i+3,j+3)])
    # Check for diagonal left
    for i in range(3):
        for j in range(3,7):
            if board[i][j] == player or board[i][j]== ".":
                if board[i+1][j-1] == player or board[i+1][j-1]== ".":
                    if board[i+2][j-2] == player or board[i+2][j-2]== ".":
                        if board[i+3][j-3] == player or board[i+3][j-3]== ".":
                            groups.append([(i,j),(i+1,j-1),(i+2,j-2),(i+3,j-3)])
    return groups

def square_to_groups(board, player):
    square_to_group={}
    threats = find_threats(board, player)
    for group in threats:
        for coord in group:
            square_to_group[coord] = group

    return square_to_group


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

def find_after_evens(board, player="O"):
    """Finds all the after evens on a board.
    The controller of the Zugzwang (black) will always play claimeven to reach the et even group.
    For this function to work, the game should comply with it's basic rules: first player must be "X" (white).

    Required: 
        A group which can be completed by the controller of the Zugzwang, using only the even
        squares of a set of Claimevens. This group is called the Aftereven group. 
        The columns in which the empty squares lie are called the Aftereven columns.
    
    Returns:
        A list of all afterevens. Each afterevne is represented by a list of tuples with coords (row, col) for the 4 squares.
    """
    afterevens = []
    for row in range(1, len(board), 2):
        for col in range(len(board[0])-3):
            if ((board[row][col] == '.' or board[row][col] == player) 
            and (board[row][col+1] == '.' or board[row][col+1] == player) 
            and (board[row][col+2] == '.' or board[row][col+2] == player) 
            and (board[row][col+3] == '.' or board[row][col+3] == player)):
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

def find_befores(board, player="X"):
    """Returns all the befores on a board. These are combinations of claimevens and verticals.

    Required:
        A group without tokens from the opponent called before group.
        All empty squares in the before group should not lie in the upper row of the board.

    Returns:
        List with all befores. Each before group represented as (square1, square2, square3, square4)
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
            befores.append(threat)
    return befores

# Helper function for special before
def is_true_special_before(board, external_playable_square, before):
    """Function to check requirements for a special before.
        Directly playable square is not in the same column as any empty square of the Before.
    """
    for square in before:
        if board[square[0]][square[1]] == ".": # If square is empty
            if external_playable_square[1] == square[1]: # If in same column
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
        for before_group in befores:
            playable_squares_in_before_group = []
            for square in before_group:
                if (square in external_playable_actions) and (square not in special_befores):
                    playable_squares_in_before_group.append(square)
            if len(playable_squares_in_before_group) >= 1:
                if is_true_special_before(board, external_action, before_group):
                    special_befores.append((external_action, before_group))
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

test_diagram = diagram6_10

print("Board:")
for row in board_flip(test_diagram):
    print(row)
print("Possible actions: ", possible_actions(test_diagram))

start = time.time()
claimevens = find_claimevens(test_diagram)
baseinverses = find_baseinverses(test_diagram)
verticals = find_verticals(test_diagram)
low_inverses = find_low_inverses(verticals)
high_inverses = find_high_inverses(test_diagram)
afterevens = find_after_evens(test_diagram)
baseclaims = find_base_claims(test_diagram)
befores = find_befores(test_diagram)
special_befores = find_special_befores(test_diagram, befores)
end = time.time()

print("Seconds taken: ", end - start)
print("Claimevens: ", claimevens)
print("Baseinverses: ", baseinverses)
print("Verticals: ", verticals)
print("Low_inverses: ", low_inverses)
print("High_inverses: ", high_inverses)
print("Afterevens: ", afterevens)
print("Baseclaims: ", baseclaims)
print("Befores: ", befores)
print("Special_befores: ", special_befores)