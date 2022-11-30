initial_board = [
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."]]

other_board = [
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", "O", ".", ".", ".", ".", "."], 
    [".", "O", ".", ".", ".", ".", "."]]

#ee
def square_to_groups(board,player):
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
    print(len(groups))

    square_to_group={}
    for group in groups:
        for coord in group:
            square_to_group[coord] = group
    print(square_to_group)
    return square_to_group


square_to_groups=square_to_groups(initial_board,"X")

# Convert each application of each rule into a Solution.
solutions=set()
group_to_solution={}
       
#Claimeven
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
claimevens=find_claimevens(initial_board)

def from_claimeven(claimeven,square_to_groups):
    rule="claimeven"
    groups= claimeven[0] # claimeven.upper
    if groups:
        return{"squares":claimeven,"groups":groups,"rule":rule}
    
for claimeven in claimevens:
    solution=from_claimeven(claimeven,square_to_groups)
    if solution:
        solutions.add(solution)
        if solution["groups"] not in group_to_solution:
            group_to_solution[solution["groups"]]=set()
        group_to_solution[solution["groups"]].add(solution)
    

#BaseInverse

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

baseinverses=find_baseinverses(initial_board)

def find_baseinverse_groups(baseinverses,square_to_groups):
    """Finds all the baseinverses on a board.

    Required: 2 directly playable squares.
    
    Returns:
        List with all the tuples that contain both squares
    """
    for baseinverse in baseinverses:
        square1=baseinverse[0]
        square2=baseinverse[1]
        groups1, groups2 = square_to_groups[square1], square_to_groups[square2]
        groups_intersection = groups1.intersection(groups2)
        if groups_intersection:
            squares= frozenset([square1, square2])
            return{"squares":squares,"groups":groups_intersection,"rule":"baseinverse"}


for baseinverse in baseinverses:
    solution=find_baseinverse_groups(baseinverse,square_to_groups)
    if solution:
        solutions.add(solution)
        if solution["groups"] not in group_to_solution:
            group_to_solution[solution["groups"]]=set()
        group_to_solution[solution["groups"]].add(solution) #add solution to group_to_solution



#Vertical
def find_verticals(board, player):
    """Finds all the verticals on a board. Function that replaces the claimeven when necessary.

    Required: 2 squares directly above each other. Both squares must be empty. The upper square must be odd.
    
    Returns:
        List with all the verticals.
        Vertical represented with (row, col) of the lower (even) square.
    """
    verticals = []
    for row in range(1, len(board)-1, 2): # Steps of 2 to reach only odd rows
        for col in range(len(board[0])):
            if board[row][col] == '.' or board[row][col] == player:
                verticals.append((row, col))
    return verticals

verticals=find_verticals(initial_board,"X")

def from_vertical(vertical,square_to_groups):
    rule="vertical"
    upper_groups=vertical[0] # vertical.upper
    lower_groups=vertical[1] # vertical.lower
    groups_intersection = upper_groups.intersection(lower_groups)
    if groups_intersection:
        return{"squares":vertical,"groups":groups_intersection,"rule":rule}

for vertical in verticals:
    solution=from_vertical(vertical,square_to_groups)
    if solution:
        solutions.add(solution)
        if solution["groups"] not in group_to_solution:
            group_to_solution[solution["groups"]]=set()
        group_to_solution[solution["groups"]].add(solution)

#Aftereven
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

afterevens=find_after_evens(initial_board,"X")