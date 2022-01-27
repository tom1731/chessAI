import numpy as np

class GameState():
    def __init__(self):
        self.board = np.array([
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
            ])

        self.move_functions = {
            'p': self.get_pawn_moves,
            'R': self.get_rook_moves,
            'N': self.get_knight_moves,
            'B': self.get_bishop_moves,
            'Q': self.get_queen_moves,
            'K': self.get_king_moves
            }

        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.in_check_log = []
        self.check_mate = False
        self.draw = False
        self.end_text = ''
        self.enpassant_possible = () # coordinates for the square where en passant capture is possible
        self.enpassant_possible_log = [self.enpassant_possible]
        self.current_castling_right = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.current_castling_right.wks,
                                               self.current_castling_right.bks,
                                               self.current_castling_right.wqs,
                                               self.current_castling_right.bqs)]
        self.game_state_log = [(str(self.board),
                                self.white_to_move,
                                self.enpassant_possible,
                                self.current_castling_right.wks,
                                self.current_castling_right.bks,
                                self.current_castling_right.wqs,
                                self.current_castling_right.bqs)]
        self.count_move = 0
        self.count_move_log = []
        self.white_castle_move = False
        self.black_castle_move = False


    '''
    Takes a move as a parameter and executes it
    '''
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = '--'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        # update the king location if moved
        if move.piece_moved == 'wK':
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_location = (move.end_row, move.end_col)

        # pawn promotion
        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q'

        # enpassant move
        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = '--'
        # update enpassant_possible variable
        if move.end_col-1 >= 0 and move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2 and self.board[move.end_row][move.end_col-1][1] == 'p':
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.end_col)
        elif move.end_col+1 <= 7 and move.piece_moved[1] == 'p' and abs(move.start_row - move.end_row) == 2 and self.board[move.end_row][move.end_col+1][1] == 'p':
                self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.end_col)
        else:
            self.enpassant_possible = ()

        self.enpassant_possible_log.append(self.enpassant_possible)

        # castle move
        if move.is_castle_move:
            if not self.white_to_move:
                self.white_castle_move = True
            else:
                self.black_castle_move = True

            if move.end_col - move.start_col == 2: # kingside castle move
                self.board[move.end_row][move.end_col-1] = self.board[move.end_row][move.end_col+1] # move the rook
                self.board[move.end_row][move.end_col+1] = '--' # erase old rook
            else: # queenside castle move
                self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-2] # move the rook
                self.board[move.end_row][move.end_col-2] = '--' # erase old rook

        # update castling rights - whenever it is a rook or a king move
        self.update_castle_rights(move)
        self.castle_rights_log.append(CastleRights(self.current_castling_right.wks,
                                                   self.current_castling_right.bks,
                                                   self.current_castling_right.wqs,
                                                   self.current_castling_right.bqs))

        # update game_state_log
        self.game_state_log.append((str(self.board),
                                  self.white_to_move,
                                  self.enpassant_possible,
                                  self.current_castling_right.wks,
                                  self.current_castling_right.bks,
                                  self.current_castling_right.wqs,
                                  self.current_castling_right.bqs))

        # update in_check_log
        self.in_check_log.append(self.in_check())

        # 50 move rule
        if move.piece_moved[1] != 'p' and move.piece_captured == '--':
            self.count_move += 1/2
        else:
            self.count_move = 0
        self.count_move_log.append(self.count_move)


    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move
            # update the king's position if needed
            if move.piece_moved == 'wK':
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_location = (move.start_row, move.start_col)
            # undo enpassant move
            if move.is_enpassant_move:
                self.board[move.end_row][move.end_col] = '--'
                self.board[move.start_row][move.end_col] = move.piece_captured

            self.enpassant_possible_log.pop()
            self.enpassant_possible = self.enpassant_possible_log[-1]
            # undo castling rights
            self.castle_rights_log.pop()
            new_rights = self.castle_rights_log[-1]
            self.current_castling_right = CastleRights(new_rights.wks, new_rights.bks, new_rights.wqs, new_rights.bqs)
            # undo castle move
            if move.is_castle_move:
                if self.white_to_move:
                    self.white_castle_move = False
                else:
                    self.black_castle_move = False
                if move.end_col - move.start_col == 2: # kingside
                    self.board[move.end_row][move.end_col+1] = self.board[move.end_row][move.end_col-1]
                    self.board[move.end_row][move.end_col-1] = '--'
                else: # queenside
                    self.board[move.end_row][move.end_col-2] = self.board[move.end_row][move.end_col+1]
                    self.board[move.end_row][move.end_col+1] = '--'
            # undo game_state_log
            self.game_state_log.pop()
            # undo in_check_log
            self.in_check_log.pop()
            # undo 50 move rule
            self.count_move_log.pop()
            if len(self.count_move_log) > 0:
                self.count_move = self.count_move_log[-1]

            self.check_mate = False
            self.draw = False


    '''
    Determine when the game end
    '''
    def end_game(self, moves):
        # checkmate and stalemate
        if len(moves) == 0:
            if self.in_check:
                self.check_mate = True
                self.end_text = 'Black wins by Checkmate' if self.white_to_move else 'White wins by Checkmate'
            else:
                self.draw = True
                self.end_text = 'Stalemate'

        # 3 times repetitive rule
        for i in self.game_state_log:
            if self.game_state_log.count(i) == 3:
                self.draw = True
                self.end_text = 'Draw by threefold repetition rule'

        # 50 moves rule
        if self.count_move == 50:
            self.draw = True
            self.end_text = 'Draw by 50 moves rule'

        # Insufficient material
        unique, counts = np.unique(self.board, return_counts=True)
        pieces_alive = dict(zip(unique, counts))
        insufficient_material = False

        if pieces_alive.keys() == {'--', 'wK', 'bK'}:
            insufficient_material = True

        if pieces_alive.keys() == {'--', 'wN', 'wK', 'bK'} and pieces_alive['wN'] <= 2:
            insufficient_material = True
        if pieces_alive.keys() == {'--', 'bN', 'wK', 'bK'} and pieces_alive['bN'] <= 2:
            insufficient_material = True
        if pieces_alive.keys() == {'--', 'wN', 'wK', 'bN', 'bK'} and pieces_alive['wN'] == 1 and pieces_alive['bN'] == 1:
            insufficient_material = True

        if pieces_alive.keys() == {'--', 'wB', 'wK', 'bK'} and pieces_alive['wB'] == 1:
            insufficient_material = True
        if pieces_alive.keys() == {'--', 'bB', 'wK', 'bK'} and pieces_alive['bB'] == 1:
            insufficient_material = True
        if pieces_alive.keys() == {'--', 'wB', 'wK', 'bB', 'bK'} and pieces_alive['wB'] == 1 and pieces_alive['bB'] == 1:
            insufficient_material = True

        if pieces_alive.keys() == {'--', 'wB', 'wK', 'bN', 'bK'} and pieces_alive['wB'] == 1 and pieces_alive['bN'] == 1:
            insufficient_material = True

        if pieces_alive.keys() == {'--', 'wN', 'wK', 'bB', 'bK'} and pieces_alive['wN'] == 1 and pieces_alive['bB'] == 1:
            insufficient_material = True


        if insufficient_material:
            self.draw = True
            self.end_text = 'Draw by insufficient material'


    '''
    update the castle rights given the move
    '''
    def update_castle_rights(self, move):
        if move.piece_moved == 'wK':
            self.current_castling_right.wks = False
            self.current_castling_right.wqs = False
        elif move.piece_moved == 'bK':
            self.current_castling_right.bks = False
            self.current_castling_right.bqs = False
        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0: # left rook
                    self.current_castling_right.wqs = False
                elif move.start_col == 7: # right rook
                    self.current_castling_right.wks = False
        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0: # left rook
                    self.current_castling_right.bqs = False
                elif move.start_col == 7: # right rook
                    self.current_castling_right.bks = False
        # if a rook is captured
        if move.piece_captured == 'wR':
            if move.end_row == 7:
                if move.end_col == 0:
                    self.current_castling_right.wqs = False
                elif move.end_col == 7:
                    self.current_castling_right.wks = False
        elif move.piece_captured == 'bR':
            if move.end_row == 0:
                if move.end_col == 0:
                    self.current_castling_right.bqs = False
                elif move.end_col == 7:
                    self.current_castling_right.bks = False


    '''
    All moves considering checks
    '''
    def get_valid_moves(self):
        temp_enpassant_possible = self.enpassant_possible
        temp_castle_rights = CastleRights(self.current_castling_right.wks,
                                          self.current_castling_right.bks,
                                          self.current_castling_right.wqs,
                                          self.current_castling_right.bqs)

        # 1. generate all possible moves
        moves = self.get_all_possible_moves()
        # 2. for each move, make the move
        for i in range(len(moves)-1, -1, -1):
            self.make_move(moves[i])
            # 3. generate all opponent's moves
            # 4. for each of your opponent's moves, see if they attack your king
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i]) # 5. if they do attack your king, not a valid move
            self.white_to_move = not self.white_to_move
            self.undo_move()

        self.end_game(moves)

        if self.white_to_move:
            self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
        else:
            self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)

        self.enpassant_possible = temp_enpassant_possible
        self.current_castling_right = temp_castle_rights
        return moves


    '''
    determine if the current player is in check
    '''
    def in_check(self):
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])


    '''
    determine if the enemy can attack the sqaure(row, col)
    '''
    def square_under_attack(self, row, col):
        self.white_to_move = not self.white_to_move
        opp_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opp_moves:
            if move.end_row == row and move.end_col == col: # square is under attack
                return True
        return False


    '''
    All moves without considering checks
    '''
    def get_all_possible_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[row][col][1]
                    self.move_functions[piece](row, col, moves) # calls the appropriate move function based on piece type
        return moves


    '''
    Get pawn moves given starting row and column, append the new moves to the list 'moves'
    '''
    def get_pawn_moves(self, row, col, moves):
        if self.white_to_move:
            direction = -1
            enemy_color = 'b'
            never_moved = 6
        else:
            direction = 1
            enemy_color = 'w'
            never_moved = 1

        if self.board[row + direction][col] == '--': # 1 square pawn move
            moves.append(Move((row, col), (row + direction, col), self.board))
            if row == never_moved and self.board[row + 2*direction][col] == '--': # 2 square pawn move
                moves.append(Move((row, col), (row + 2*direction, col), self.board))
        # captures
        if col-1 >= 0:
            if self.board[row + direction][col-1][0] == enemy_color: # enemy piece capture to the left
                moves.append(Move((row, col), (row + direction, col-1), self.board))
            elif (row + direction, col-1) == self.enpassant_possible:
                moves.append(Move((row, col), (row + direction, col-1), self.board, is_enpassant_move = True))

        if col+1 <= 7:
            if self.board[row + direction][col+1][0] == enemy_color: # enemy piece capture to the right
                moves.append(Move((row, col), (row + direction, col+1), self.board))
            elif (row + direction, col+1) == self.enpassant_possible:
                moves.append(Move((row, col), (row + direction, col+1), self.board, is_enpassant_move = True))


    '''
    Get rook moves given starting row and column, append the new moves to the list 'moves'
    '''
    def get_rook_moves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # up, left, down, right
        ally_color = 'w' if self.white_to_move else 'b'
        for d in directions:
            end_row = row
            end_col = col
            while 0 <= end_row + d[0] < 8 and 0 <= end_col + d[1] < 8:
                end_row += d[0]
                end_col += d[1]
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                    if end_piece != '--':
                        break
                else: break


    '''
    Get knight moves given starting row and column, append the new moves to the list 'moves'
    '''
    def get_knight_moves(self, row, col, moves):
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)) # up-left, up-right, left-up, left-down, right-up, right-down, down-left, down-right
        ally_color = 'w' if self.white_to_move else 'b'
        for d in directions:
            end_row = row + d[0]
            end_col = col + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if self.board[end_row][end_col][0] != ally_color:
                    moves.append(Move((row, col), (end_row, end_col), self.board))


    '''
    Get bishop moves given starting row and column, append the new moves to the list 'moves'
    '''
    def get_bishop_moves(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # up-left, up-right, down-left, down-right
        ally_color = 'w' if self.white_to_move else 'b'
        for d in directions:
            end_row = row
            end_col = col
            while 0 <= end_row + d[0] < 8 and 0 <= end_col + d[1] < 8:
                end_row += d[0]
                end_col += d[1]
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                    if end_piece != '--':
                        break
                else: break


    '''
    Get queen moves given starting row and column, append the new moves to the list 'moves'
    '''
    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)


    '''
    Get king moves given starting row and column, append the new moves to the list 'moves'
    '''
    def get_king_moves(self, row, col, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1))
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row = row + directions[i][0]
            end_col = col + directions[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((row, col), (end_row, end_col), self.board))


    '''
    Generate all valid castle moves for the king at (row, col) and add them to the list of moves
    '''
    def get_castle_moves(self, row, col, moves):
        if self.square_under_attack(row, col):
            return # can't castle while we are in check
        if (self.white_to_move and self.current_castling_right.wks) or (not self.white_to_move and self.current_castling_right.bks):
            self.get_king_side_castle_moves(row, col, moves)
        if (self.white_to_move and self.current_castling_right.wqs) or (not self.white_to_move and self.current_castling_right.bqs):
            self.get_queen_side_castle_moves(row, col, moves)

    def get_king_side_castle_moves(self, row, col, moves):
        if self.board[row][col+1] == '--' and self.board[row][col+2] == '--':
            if not self.square_under_attack(row, col+1) and not self.square_under_attack(row, col+2):
                moves.append(Move((row, col), (row, col+2), self.board, is_castle_move=True))

    def get_queen_side_castle_moves(self, row, col, moves):
        if self.board[row][col-1] == '--' and self.board[row][col-2] == '--' and self.board[row][col-3] == '--' and \
         not self.square_under_attack(row, col-1) and not self.square_under_attack(row, col-2):
                moves.append(Move((row, col), (row, col-2), self.board, is_castle_move=True))


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    rows_to_ranks = {7: '1', 6: '2', 5: '3', 4: '4',
                     3: '5', 2: '6', 1: '7', 0: '8'}

    cols_to_files = {0: 'a', 1: 'b', 2: 'c', 3: 'd',
                     4: 'e', 5: 'f', 6: 'g', 7: 'h'}


    def __init__(self, start_square, end_square, board, is_enpassant_move=False, is_castle_move=False):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # pawn promotion
        self.is_pawn_promotion = (self.piece_moved == 'wp' and self.end_row == 0) or (self.piece_moved == 'bp' and self.end_row == 7)
        # en passant
        self.is_enpassant_move = is_enpassant_move
        if is_enpassant_move:
            self.piece_captured = 'wp' if self.piece_moved == 'bp' else 'bp'
        # castle move
        self.is_castle_move = is_castle_move

        self.is_capture = self.piece_captured != '--'
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col


    # Overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False


    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)


    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]


    # overriding the str() function
    def __str__(self):
        # castle move
        if self.is_castle_move:
            return 'O-O' if self.end_col == 6 else 'O-O-O'

        end_square = self.get_rank_file(self.end_row, self.end_col)
        # pawn moves
        if self.piece_moved[1] == 'p':
            if self.is_capture:
                return self.cols_to_files[self.start_col] + 'x' + end_square
            else:
                return end_square

        # piece moves
        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += 'x'
        return move_string + end_square
