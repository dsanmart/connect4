from copy import deepcopy
  



# ----------- HELPER FUNCTIONS ----------- #
def board_flip(board):
    """Returns a new board with the board flipped vertically.
    This allows accessing the lower row as the first item in the list."""

    new_board = deepcopy(board)
    new_board.reverse()
    return new_board

def is_end(board):
    for col in range(len(board[0])):
        if board[-1][col] == ".":
            return False
    return True


def check_win(board, player):
    #check rows
    for row in board:
        if player*4 in "".join(row):
            return True

    #check cols
    for col in list(zip(*board)):
        if player*4 in "".join(col):
            return True

    #check diagonals
    for i in range(3):
        for j in range(4):
            if board[i][j]==player and board[i+1][j+1]==player and board[i+2][j+2]==player and board[i+3][j+3]==player:
                return True

    for i in range(3):
        for j in range(3,7):
            if board[i][j]==player and board[i+1][j-1]==player and board[i+2][j-2]==player and board[i+3][j-3]==player:
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

def fill_possible_actions(board, possible_actions, player):
    """Returns a new board with the possible actions filled in.
    
    Args:
        board (list): The original board to fill in.
        possible_actions (list): A list of possible actions (row, col).
        player (str): The player to fill in the actions with.
    """
    boards = []
    for row, col in possible_actions:
        new_board = deepcopy(board)
        new_board[row][col] = player
        boards.append(new_board)
    return boards


# ----------- MINIMAX ----------- #

def heuristic(board, player):
    if check_win(board, "X"):
        return 100
    elif check_win(board, "O"):
        return -100
    else:
        return 0

def minimax(board, player, tree_depth, alpha, beta):
    if tree_depth == 0 or is_end(board):
        return heuristic(board, player), board

    if player == "X":
        max_score = -1000
        best_move = None
        for move in fill_possible_actions(board, possible_actions(board), "X"):
            score = minimax(move, player, tree_depth-1, alpha, beta)[0] # To reduce memory usage we only get the score [0] when calling this recursive function (not the best_move)
            max_score = max(max_score, score)
            if max_score == score:
                best_move = move
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return max_score, best_move
    else:
        min_score = 1000
        best_move = None
        for move in fill_possible_actions(board, possible_actions(board), "O"):
            score = minimax(move, player, tree_depth - 1, alpha, beta)[0] # To reduce memory usage we only get the score [0] when calling this recursive function (not the best_move)
            min_score = max(min_score, score)
            if min_score == score:
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                break
        return min_score, best_move



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

complete_board = board_flip([
    ["X", "X", "X", "X", "X", "X", "X"], 
    [".", ".", ".", "O", ".", ".", "."], 
    [".", ".", ".", "X", ".", ".", "."], 
    [".", ".", ".", "O", ".", ".", "."], 
    [".", ".", ".", "X", ".", ".", "."], 
    [".", ".", "X", "O", "O", ".", "."]])

diagram_win = board_flip([
    [".", ".", ".", "X", ".", ".", "."], 
    [".", ".", ".", "O", ".", ".", "."], 
    [".", ".", ".", "X", ".", ".", "O"], 
    [".", ".", ".", "O", ".", "X", "O"], 
    [".", ".", ".", "X", "O", "X", "O"], 
    [".", ".", "X", "O", "O", "X", "X"]])


test_diagram = diagram6_1

print("Initial Board:")
for row in board_flip(test_diagram):
    print(row)

next_move_score, next_move_board = minimax(test_diagram, "X", 7, -1000, 1000)

print("Next Move:")
print("Score", next_move_score)
for row in board_flip(next_move_board):
    print(row)