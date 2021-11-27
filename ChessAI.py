import random

piece_score = {
    'K': 0,
    'Q': 9,
    'R': 5,
    'B': 3,
    'N': 3,
    'p': 1
    }

checkmate_score = 1000
stalemate_score = 0

'''
picks and return a random move
'''
def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves)-1)]

'''
find the best move based on material alone
'''
def find_best_move(gs, valid_moves):
    turn_multiplayer = 1 if gs.white_to_move else -1

    opponent_min_max_score = -checkmate_score
    best_move = None
    for player_move in valid_moves:
        gs.make_move(player_move)
        opponents_move = gs.get_valid_moves()
        for opponents_move in opponents_move:
            gs.make_move(opponents_move)
            if gs.check_mate:
                score = -checkmate_score
            elif gs.stale_mate:
                score = 0
            else:
                score = -turn_multiplayer * score_material(gs.board)
            if score > max_score:
                max_score = score
                best_move = player_move
            gs.undo_move()
        gs.undo_move()
    return best_move


'''
score the board based on material
'''
def score_material(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]

    return score
