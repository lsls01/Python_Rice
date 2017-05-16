"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    '''
    This function takes a current board and the next player to move. The
    function should play a game starting with the given player by making
    random moves, alternating between players. The function will also modifies
    the board and returns when the game is over
    '''
    
    winner = board.check_win()
    
    while winner == None:
        # empty_tiles will get a list of tuples
        empty_tiles = board.get_empty_squares()
        next_move = empty_tiles[random.randrange(len(empty_tiles))]
        board.move(next_move[0], next_move[1], player)
        player = provided.switch_player(player)
        winner = board.check_win()
    return
    
def mc_update_scores(scores, board, player):
    '''
    This function takes a grid scores with the same dimensions as the board, and
    score the completed board and update the scores grid. It returns nothing.
    '''
    winner = board.check_win()
    if winner in [None, provided.DRAW]:
        return
        
    if winner == player:
        cur_score = SCORE_CURRENT
        opp_score = (-1) * SCORE_OTHER
    else:
        cur_score = (-1) * SCORE_CURRENT
        opp_score = SCORE_OTHER
    
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            state = board.square(row, col)
            if state == provided.EMPTY:
                pass
            elif state == player:
                scores[row][col] += cur_score
            else:
                scores[row][col] += opp_score

def get_best_move(board, scores):
    '''
    This function takes a current board and grid of scores and returns the
    square with the maximum score
    '''
    empty_tiles = board.get_empty_squares()
    if len(empty_tiles) == 0:
        return
    
    values = [scores[square[0]][square[1]] for square in empty_tiles]
    max_value = max(values)
    
    moves = []
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if ((row, col) in empty_tiles) and scores[row][col] == max_value:
                moves.append((row, col))
    
    random_move = random.choice(moves)
    return random_move
def mc_move(board, player, trials):
    '''
    This function takes a current board, which player the machine player is,
    and the number of trials to run. Return a move for the machine player in
    the form of a (row, column) tuple.
    '''
    scores = [[0 for dummy_row in range(board.get_dim())] for dummy_col in range(board.get_dim())]
    for dummy in range(trials):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
    
    return get_best_move(board, scores)

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
