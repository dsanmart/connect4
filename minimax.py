from copy import deepcopy
from utils import find_strong_threat

# ----------- HELPER FUNCTIONS ----------- #
def board_flip(board):
    """Returns a new board with the board flipped vertically.
    This allows accessing the lower row as the first item in the list."""
    new_board =deepcopy(board)
    #print((list(new_board)))
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

def possible_actions(board):# board_flip(board)
    """Returns a list of all directly playable actions (row, col) on a board."""
    actions = []
    for col in range(len(board[0])):
        for row in range(len(board)):
            if board[row][col] == '.':
                actions.append((row,col))
                break
    # playable_cols = [x[1] for x in actions]
    return actions # [(0,1), (1,2)....]

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

def other_player(player):
  if player == "X":
    other_player = "O"
  else:
    other_player = "X"
  return other_player


# ----------- MINIMAX ----------- #

def heuristic(board, player):
    if player == "X":
        oppponent = "O"
    else:
        oppponent = "X"
    score = 0
    if check_win(board, player): # If the player wins, return a high score
        score += 40
    if check_win(board, oppponent): # if the opponent wins, the score is -100
        score -= 40
    if find_strong_threat(board, oppponent):
        score -= 17
    if find_strong_threat(board, player):
        score += 17

    return score

def minimax(board, player,is_maximizing, tree_depth, alpha, beta):
    if tree_depth == 0 or is_end(board):
        return heuristic(board, player), board

    if is_maximizing:
        max_score = -1000
        best_move = None
        for move in fill_possible_actions(board, possible_actions(board), player):
            score = minimax(move, player,False, tree_depth-1, alpha, beta)[0] # To reduce memory usage we only get the score [0] when calling this recursive function (not the best_move)
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
        for move in fill_possible_actions(board, possible_actions(board), other_player(player)):
            score = minimax(move,other_player(player) ,True, tree_depth - 1, alpha, beta)[0] # To reduce memory usage we only get the score [0] when calling this recursive function (not the best_move)
            min_score = max(min_score, score)
            if min_score == score:
                best_move = move
            beta = min(beta, score)
            if beta <= alpha:
                break
        return min_score, best_move

