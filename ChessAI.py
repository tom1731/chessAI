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
depth = 1

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
    opponent_min_max_score = checkmate_score
    best_player_move = None
    random.shuffle(valid_moves)
    for player_move in valid_moves:
        gs.make_move(player_move)
        opponents_move = gs.get_valid_moves()
        if gs.stale_mate:
            opponent_max_score = stalemate_score
        elif gs.check_mate:
            opponent_max_score = -check_mate
        else:
            opponent_max_score = -checkmate_score
            for opponents_move in opponents_move:
                gs.make_move(opponents_move)
                gs.get_valid_moves()
                if gs.check_mate:
                    score = checkmate_score
                elif gs.stale_mate:
                    score = stalemate_score
                else:
                    score = -turn_multiplayer * score_material(gs.board)
                if score > opponent_max_score:
                    opponent_max_score = score
                gs.undo_move()
        if opponent_max_score < opponent_min_max_score :
            opponent_min_max_score = opponent_max_score
            best_player_move = player_move
        gs.undo_move()
    return best_player_move

'''
helper methode to make first recursive call
'''
def find_best_move_min_max(gs, valid_moves):
    global next_move
    next_move = None
    find_move_min_max(gs, valid_moves, depth, gs.white_to_move)
    return next_move

def find_move_min_max(gs, valid_moves, depth, white_to_move):
    global next_move
    if depth == 0:
        return score_material(gs.board)

    if white_to_move:
        max_score = -checkmate_score
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_min_max(gs, next_moves, depth-1, False)
            if score > max_score:
                max_score = score
                if depth == depth:
                    next_move = move
            gs.undo_move()
        return max_score

    else:
        min_score = checkmate_score
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_min_max(gs, next_moves, depth-1, True)
            if score < min_score:
                min_score = score
                if depth == depth:
                    next_move = move
            gs.undo_move()
        return min_score

'''
A positive score is good for white, negative is good for black
'''
def score_board(gs):
    if gs.check_mate:
        if gs.white_to_move:
            return -check_mate # black wins
        else:
            return check_mate # white wins
    elif gs.stale_mate:
        return stale_mate

    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_score[square[1]]
            elif square[0] == 'b':
                score -= piece_score[square[1]]

    return score

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
