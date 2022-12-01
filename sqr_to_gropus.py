from copy import copy, deepcopy

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
                            groups.append(tuple([(i,j),(i+1,j),(i+2,j),(i+3,j)]))
    
    # Check for horizontal
    for i in range(6):
        for j in range(4):
            if board[i][j] == player or board[i][j]== ".":
                if board[i][j+1] == player or board[i][j+1]== ".":
                    if board[i][j+2] == player or board[i][j+2]== ".":
                        if board[i][j+3] == player or board[i][j+3]== ".":
                            groups.append(tuple([(i,j),(i,j+1),(i,j+2),(i,j+3)]))

    # Check for diagonal right
    for i in range(3):
        for j in range(4):
            if board[i][j] == player or board[i][j]== ".":
                if board[i+1][j+1] == player or board[i+1][j+1]== ".":
                    if board[i+2][j+2] == player or board[i+2][j+2]== ".":
                        if board[i+3][j+3] == player or board[i+3][j+3]== ".":
                            groups.append(tuple([(i,j),(i+1,j+1),(i+2,j+2),(i+3,j+3)]))
    # Check for diagonal left
    for i in range(3):
        for j in range(3,7):
            if board[i][j] == player or board[i][j]== ".":
                if board[i+1][j-1] == player or board[i+1][j-1]== ".":
                    if board[i+2][j-2] == player or board[i+2][j-2]== ".":
                        if board[i+3][j-3] == player or board[i+3][j-3]== ".":
                            groups.append(tuple([(i,j),(i+1,j-1),(i+2,j-2),(i+3,j-3)]))
    print(len(groups))

    square_to_group={}
    for group in groups:
        for coord in group:
            if coord not in square_to_group:
                square_to_group[coord] = []
            square_to_group[coord].append(group)
    print("s",square_to_group)
    return square_to_group


square_to_groups=square_to_groups(initial_board,"X")
#print(square_to_groups)

# Convert each application of each rule into a Solution.
solutions=[]
group_to_solution={}
       
def board_flip(board):
    """Returns a new board with the board flipped vertically.
    This allows accessing the lower row as the first item in the list."""

    new_board = deepcopy(board)
    new_board.reverse()
    return new_board
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
claimevens=find_claimevens(board_flip(initial_board))
print("claimevenes list",claimevens)

def from_claimeven(claimeven,square_to_groups):
    '''Arguments: claimeven, square_to_groups
    Returns:
    -Squares: upper an lower square
    -Groups: groups that contain the upper and lower square
    - Rules: rules that apply to the groups'''

    rule="claimeven"
    groups= square_to_groups[claimeven] 
    if groups:
        return{"squares":[claimeven,(claimeven[0]-1, claimeven[1])],"groups": groups,"rule":rule} #output
    
for claimeven in claimevens:
    solution=from_claimeven(claimeven,square_to_groups)# get the solution for each claimeven
    if solution:
        solutions.append(solution)
        for group in solution["groups"]:
            if group not in group_to_solution:# check if the group is already in the dictionary
                group_to_solution[group]=[]
            group_to_solution[group].append(solution) # group_to_solutons--> Dict: key=group, value={squares,groups,rule}
print("-------------------")
print("Claimeven",group_to_solution)

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
print("-------------------")
print("BaseInverses", board_flip(baseinverses))

# intersection(list1,list2)--> returns the common elements of list1 and list2
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return tuple(lst3)

def from_baseinverse(baseinverses,square_to_groups):
    """Finds all the baseinverses on a board.

    Required: 2 directly playable squares.
    
    Returns:
        List with all the tuples that contain both squares

    """

    for baseinverse in baseinverses:
        square1=baseinverse[0]
        square2=baseinverse[1]
        if square1 in square_to_groups and square2 in square_to_groups:
            groups1, groups2 = square_to_groups[square1], square_to_groups[square2]
            groups_intersection = intersection(groups1, groups2)
            if groups_intersection:
                squares= (square1, square2)
                return{"squares":squares,"groups":groups_intersection,"rule":"baseinverse"}


for baseinverse in baseinverses:
    solution=from_baseinverse(baseinverse,square_to_groups)#normally None
    print("solution",solution)
    if solution:
        solutions.append(solution)
        if solution["groups"] not in group_to_solution:
            group_to_solution[solution["groups"]]=[]
        group_to_solution[solution["groups"]].append(solution) #add solution to group_to_solution

print("-------------------")
from_baseinverse(baseinverses,square_to_groups)
print("BaseInverse",group_to_solution)

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
print("-------------------")
print("Verticals", board_flip(verticals))

def from_vertical(vertical,square_to_groups):
    '''Args: vertial: tuple with the coordinates of the lower square
    square_to_groups: dictionary with the groups of each square
    Returns: dictionary with the solution '''
    rule="vertical"
    if vertical in square_to_groups and (vertical[0]+1,vertical[1]) in square_to_groups:
        upper_groups=square_to_groups[vertical] # vertical.lower
        lower_groups=square_to_groups[(vertical[0]+1,vertical[1])] # vertical.upper
        groups_intersection = intersection(upper_groups,lower_groups)
        if groups_intersection:
            return{"squares":vertical,"groups":groups_intersection,"rule":rule}

for vertical in verticals:
    solution=from_vertical(vertical,square_to_groups)
    if solution:
        solutions.append(solution)
        if solution["groups"] not in group_to_solution:
            group_to_solution[solution["groups"]]=[]
        group_to_solution[solution["groups"]].append(solution)


print("-------------------")

print("Vertical",group_to_solution)

#AfterEven


