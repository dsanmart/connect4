from victor import evaluate
from utils import board_flip, compare, compare2, find_strong_threat
from minimax2 import minimax

initial_board = board_flip([
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."], 
    [".", ".", ".", ".", ".", ".", "."]])

def play(previous_board, board, player):
    board = board_flip(board)
    previous_board = board_flip(previous_board)
    if board == initial_board:
        return 3
    solutions = evaluate(previous_board, player)
    if len(solutions) == 0: # If victor is sleeping, play minimax
        _, next_move_board = minimax(board, player, True, 8, -1000, 1000)
        return compare(board,next_move_board)
    else: # If victor is awake, play victor
        square_to_play = {}
        #print("Solutions", len(solutions))
        for solution in solutions:
            if solution["rule"] == "before":
                square_to_play = before_plays(solution, square_to_play)
        for solution in solutions:
            if solution["rule"] == "vertical":
                square_to_play = claimeven_plays(solution, square_to_play)
        for solution in solutions:
            if solution["rule"] == "claimeven":
                square_to_play = claimeven_plays(solution, square_to_play)
        for solution in solutions:
            if solution["rule"] == "baseinverse":
                square_to_play = baseinverse_plays(solution, square_to_play)
        
        opponent_move = compare2(previous_board, board, player)
        #print("Opponent move", opponent_move)
        if player == 'X':
            opponent = 'O'
        else:
            opponent = 'X'
        if find_strong_threat(board, player) or find_strong_threat(board, opponent):
            print("Victor lets minimax handle strong threat")
            _, next_move_board = minimax(board, player, True, 8, -1000, 1000)
            return compare(board,next_move_board)
        elif opponent_move in square_to_play.keys():
            print("Victor plays", square_to_play[opponent_move][1])
            return square_to_play[opponent_move][1]
        else:
            print("Victor sleeps", opponent_move)
            _, next_move_board = minimax(board, player, True, 8, -1000, 1000)
            return compare(board,next_move_board)

def baseinverse_plays(solution, square_to_play):
    squares = solution["squares"]
    square_to_play[squares[0]] = squares[1]
    square_to_play[squares[1]] = squares[0]

    return square_to_play

def claimeven_plays(solution, square_to_play):
    squares = solution["squares"]
    square_to_play[squares[1]] = squares[0]
    return square_to_play

def before_plays(solution, square_to_play):
    vertical_squares = solution["verticals"]
    claimeven_squares = solution["claimevens"]
    for square in vertical_squares:
        square_to_play[square[1]] = square[0]
    for square in claimeven_squares:
        square_to_play[square[1]] = square[0]
    return square_to_play




    
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

    # Diagram backtracks and finds multiple eurekas
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

    test_diagram = diagram6_10
    player = "X"
    print("Board:")
    for row in board_flip(test_diagram):
        print(row)
    print("Player:", player)
    play(test_diagram, player)
