# ----------- HELPER FUNCTIONS ----------- #

from copy import deepcopy

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

def intersection(lst1, lst2):
    intersection = [value for value in lst1 if value in lst2]
    return tuple(intersection)

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
                            groups.append(((i,j),(i+1,j),(i+2,j),(i+3,j)))
    
    # Check for horizontal
    for i in range(6):
        for j in range(4):
            if board[i][j] == player or board[i][j]== ".":
                if board[i][j+1] == player or board[i][j+1]== ".":
                    if board[i][j+2] == player or board[i][j+2]== ".":
                        if board[i][j+3] == player or board[i][j+3]== ".":
                            groups.append(((i,j),(i,j+1),(i,j+2),(i,j+3)))

    # Check for diagonal right
    for i in range(3):
        for j in range(4):
            if board[i][j] == player or board[i][j]== ".":
                if board[i+1][j+1] == player or board[i+1][j+1]== ".":
                    if board[i+2][j+2] == player or board[i+2][j+2]== ".":
                        if board[i+3][j+3] == player or board[i+3][j+3]== ".":
                            groups.append(((i,j),(i+1,j+1),(i+2,j+2),(i+3,j+3)))
    # Check for diagonal left
    for i in range(3):
        for j in range(3,7):
            if board[i][j] == player or board[i][j]== ".":
                if board[i+1][j-1] == player or board[i+1][j-1]== ".":
                    if board[i+2][j-2] == player or board[i+2][j-2]== ".":
                        if board[i+3][j-3] == player or board[i+3][j-3]== ".":
                            groups.append(((i,j),(i+1,j-1),(i+2,j-2),(i+3,j-3)))
    return groups

def find_strong_threat(board, player):
    # Finds threats with 3 of the player's pieces and 1 empty space
    opponent_threats = find_threats(board, player)
    playable_actions = possible_actions(board)
    for threat in opponent_threats:
        tokens = 0
        empty_squares = 0
        for square in threat:
            if board[square[0]][square[1]] == player:
                tokens += 1
            if board[square[0]][square[1]] == '.' and square in playable_actions:
                empty_squares += 1
        if tokens == 3 and empty_squares == 1:
            return True

    return False

def stop_threat(board, player):
    # Finds threats with 3 of the player's pieces and 1 empty space
    opponent_threats = find_threats(board, player)
    playable_actions = possible_actions(board)
    for threat in opponent_threats:
        tokens = 0
        empty_squares = 0
        for square in threat:
            if board[square[0]][square[1]] == player:
                tokens += 1
            if board[square[0]][square[1]] == '.' and square in playable_actions:
                empty_squares += 1
                empty_square = square
        if tokens == 3 and empty_squares == 1:
            return empty_square
    return None

# ----------- HELPER FUNCTIONS FOR EVALUATION FUNCTION ----------- #
def node_with_least_number_of_neighbors(node_graph, problems, disallowed_solutions):

    most_difficult_node = None
    num_neighbors_of_most_difficult = len(node_graph) + 1  # Set to an arbitrary high number.

    # Find the Problem in problems with the fewest neighbors in node_graph.
    # Only allowed_solutions are counted.
    for problem in problems:
        if problem in node_graph:
            num_nodes = sum(1 for d in node_graph[problem] if d) - len(disallowed_solutions)
            if num_nodes < num_neighbors_of_most_difficult:
                most_difficult_node = problem
                num_neighbors_of_most_difficult = num_nodes

    # If we didn't find a most_difficult_node, then that means there isn't a single Problem in both
    # problems and node_graph.
    if most_difficult_node is not None:
        return most_difficult_node

    print("No problem in problems and node_graph")



def cols_to_squares(squares):
    """Converts an iterable of Squares into a dictionary of Squares keyed by the column they belong in.
    Args:
        squares (iterable<Square>): an iterable of Square objects.
    Returns:
        col_to_squares_dict (Map<int, Set<Square>>): a dictionary of columns to Squares in that column.
    """
    col_to_squares_dict = {}
    for square in squares:
        if square[1] not in col_to_squares_dict:
            col_to_squares_dict[square[1]] = set()
        col_to_squares_dict[square[1]].add(square)
    return col_to_squares_dict

def compare( board, new_board):
  for i in range(len(board)):
    for j in range(len(board[0])):
      if board[i][j] != new_board[i][j]:
        return j


def compare2(board, new_board, player):
  for i in range(len(board)):
    for j in range(len(board[0])):
      if board[i][j] != new_board[i][j] and board[i][j] != player:
        return (i, j)