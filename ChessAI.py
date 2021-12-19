import random

piece_score = {
    'K': 0,
    'Q': 9,
    'R': 5,
    'B': 3,
    'N': 3,
    'p': 1
    }

knight_scores = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
    ]

bishop_scores = [
    [4, 3, 2, 1, 1, 2, 3, 4],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [4, 3, 2, 1, 1, 2, 3, 4]
    ]

queen_scores = [
    [1, 1, 1, 3, 1, 1, 1, 1],
    [1, 2, 3, 3, 3, 1, 1, 1],
    [1, 4, 3, 3, 3, 4, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 4, 3, 3, 3, 4, 2, 1],
    [1, 1, 2, 3, 3, 1, 1, 1],
    [1, 1, 1, 3, 1, 1, 1, 1]
    ]

rook_scores = [
    [4, 3, 4, 4, 4, 4, 3, 4],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [1, 1, 2, 2, 2, 2, 1, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 1, 2, 2, 2, 2, 1, 1],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [4, 3, 4, 4, 4, 4, 3, 4]
    ]

white_pawn_scores = [
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [2, 3, 3, 5, 5, 3, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
    ]

black_pawn_scores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 3, 5, 5, 3, 3, 2],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8]
    ]

piece_position_scores = {
    'N': knight_scores,
    'Q': queen_scores,
    'B': bishop_scores,
    'R': rook_scores,
    'bp': black_pawn_scores,
    'wp': white_pawn_scores
    }

checkmate_score = 1000
stalemate_score = 0
depth_game = 4

'''
picks and return a random move
'''
def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves)-1)]

'''
helper methode to make first recursive call
'''
def find_best_move(gs, valid_moves, return_queue, nbProcess):

    print(f"Process {nbProcess}")

    global next_move
    next_move = None
    random.shuffle(valid_moves)
    score = find_move_negamax_alpha_beta(gs, valid_moves, depth_game, -checkmate_score, checkmate_score, 1 if gs.white_to_move else -1)

    print(f"Process {nbProcess} ended, best move : {next_move} with {abs(score)}")

    return_queue.put((next_move, abs(score)))

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
                if depth == depth_game:
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
                if depth == depth_game:
                    next_move = move
            gs.undo_move()
        return min_score

def find_move_negamax(gs, valid_moves, depth, turn_multiplayer):
    global next_move
    if depth == 0:
        return turn_multiplayer * score_board(gs)

    max_score = -checkmate_score
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_negamax(gs, next_moves, depth-1, -turn_multiplayer)
        if score > max_score:
            max_score = score
            if depth == depth_game:
                next_move = move
        gs.undo_move()
    return max_score

def find_move_negamax_alpha_beta(gs, valid_moves, depth, alpha, beta, turn_multiplayer):
    global next_move
    if depth == 0:
        return turn_multiplayer * score_board(gs)

    # move ordering - implement later
    max_score = -checkmate_score
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_negamax_alpha_beta(gs, next_moves, depth-1, -beta, -alpha, -turn_multiplayer)
        if score > max_score:
            max_score = score
            if depth == depth_game:
                next_move = move
        gs.undo_move()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break

    return max_score

'''
A positive score is good for white, negative is good for black
'''
def score_board(gs):
    if gs.check_mate:
        if gs.white_to_move:
            return -checkmate_score # black wins
        else:
            return checkmate_score # white wins
    elif gs.stale_mate:
        return stale_mate

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':
                piece_position_score = 0
                if square[1] != 'K':
                    if square[1] == 'p':
                        piece_position_score = piece_position_scores[square][row][col]
                    else:
                        piece_position_score = piece_position_scores[square[1]][row][col]

                if square[0] == 'w':
                    score += piece_score[square[1]] + piece_position_score * 0.1
                elif square[0] == 'b':
                    score -= piece_score[square[1]] + piece_position_score * 0.1

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
