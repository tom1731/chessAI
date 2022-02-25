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
    [4, 3, 1, 1, 1, 1, 3, 4],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [4, 3, 1, 1, 1, 1, 3, 4]
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
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 2, 2, 2, 2, 1, 1],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [4, 3, 4, 4, 4, 4, 3, 4]
    ]

white_pawn_scores = [
    [8, 8, 8, 8, 8, 8, 8, 8],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [1, 1, 1, 5, 5, 1, 1, 1],
    [1, 1, 1, 4, 4, 1, 1, 1],
    [1, 1, 1, 4, 4, 1, 1, 1],
    [1, 1, 1, 2, 2, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
    ]

black_pawn_scores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 2, 2, 1, 1, 1],
    [1, 1, 1, 4, 4, 1, 1, 1],
    [1, 1, 1, 4, 4, 1, 1, 1],
    [1, 1, 1, 5, 5, 1, 1, 1],
    [5, 5, 5, 5, 5, 5, 5, 5],
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


'''
picks and return a random move
'''
def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves)-1)]


'''
helper methode to make first recursive call
'''
def find_best_move(gs, valid_moves, depth_game, return_queue):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    find_move_negamax_alpha_beta(gs, valid_moves, depth_game, depth_game, -checkmate_score, checkmate_score, 1 if gs.white_to_move else -1)
    return_queue.put(next_move)


def find_move_negamax_alpha_beta(gs, valid_moves, depth, depth_game, alpha, beta, turn_multiplayer):
    global next_move
    if depth == 0:
        return turn_multiplayer * score_board(gs)

    # move ordering - implement later
    max_score = -checkmate_score
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_negamax_alpha_beta(gs, next_moves, depth-1, depth_game, -beta, -alpha, -turn_multiplayer)
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
    elif gs.draw:
        return stalemate_score

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

    if gs.white_to_move:
        if gs.current_castling_right.wks or gs.current_castling_right.wqs:
            score += 1
        elif gs.white_castle_move:
            score += 1.9
    else:
        if gs.current_castling_right.bks or gs.current_castling_right.bqs:
            score -= 1
        elif gs.black_castle_move:
            score -= 1.9

    return score
