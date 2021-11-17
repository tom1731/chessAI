class GameState():
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
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
        self.in_check = False
        self.pins = []
        self.checks = []

    '''
    Takes a move as a parameter and executes it (not work with castling, pawn prootion and en-passant)
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

    '''
    All moves considering checks
    '''
    def get_valid_moves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1: # only 1 check, block check or move king
                moves = self.get_all_possible_moves()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col] # enemy piece causing the check
                valid_squares = [] # square that pieces can move to
                # if knight, must be capture or move king, other pieces can be blocked
                if piece_checking[1] == 'N':
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i) # check[2] and check[3] are the check directions
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col: # once you get to piece and check
                            break
                # get ri of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1): # go through backwards when you are removing from a list as iterating
                    if moves[i].piece_moved[1] != 'K': # move doesn't move king so it must block or capture
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares: # move doesn't block check or capture piece
                            moves.remove(moves[i])
            else: # double check, king has to move
                self.get_king_moves(king_row, king_col, moves)
        else: # not in check so all moves are fine
            moves = self.get_all_possible_moves()

        return moves

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
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''
    def get_pawn_moves(self, row, col, moves):
        if self.white_to_move:
            directions = -1
            enemy_color = 'b'
            never_moved = 6
        else:
            directions = 1
            enemy_color = 'w'
            never_moved = 1
        if self.board[row + directions][col] == '--': # 1 square pawn move
            moves.append(Move((row, col), (row + directions, col), self.board))
            if row == never_moved and self.board[row + 2*directions][col] == '--': # 2 square pawn move
                moves.append(Move((row, col), (row + 2*directions, col), self.board))
        if col-1 >= 0 and self.board[row + directions][col-1][0] == enemy_color: # enemy piece capture to the left
            moves.append(Move((row, col), (row + directions, col-1), self.board))
        if col+1 <= 7 and self.board[row + directions][col+1][0] == enemy_color: # enemy piece capture to the right
            moves.append(Move((row, col), (row + directions, col+1), self.board))

    '''
    Get all the rook moves for the pawn located at row, col and add these moves to the list
    '''
    def get_rook_moves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # up, left, down, right
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            end_row = row
            end_col = col
            while 0 <= end_row + d[0] < 8 and 0 <= end_col + d[1] < 8:
                end_row += d[0]
                end_col += d[1]
                if self.board[end_row][end_col] == '--': # move
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                elif self.board[end_row][end_col][0] == enemy_color: # capture
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                    break
                else: break

    '''
    Get all the knight moves for the pawn located at row, col and add these moves to the list
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
    Get all the bishop moves for the pawn located at row, col and add these moves to the list
    '''
    def get_bishop_moves(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # up-left, up-right, down-left, down-right
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            end_row = row
            end_col = col
            while 0 <= end_row + d[0] < 8 and 0 <= end_col + d[1] < 8:
                end_row += d[0]
                end_col += d[1]
                if self.board[end_row][end_col] == '--': # move
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                elif self.board[end_row][end_col][0] == enemy_color: # capture
                    moves.append(Move((row, col), (end_row, end_col), self.board))
                    break
                else: break

    '''
    Get all the queen moves for the pawn located at row, col and add these moves to the list
    '''
    def get_queen_moves(self, row, col, moves):
        self.get_rook_moves(row, col, moves)
        self.get_bishop_moves(row, col, moves)
    '''
    Get all the king moves for the pawn located at row, col and add these moves to the list
    '''
    def get_king_moves(self, row, col, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1)) # up-left, up-right, down-left, down-right, up, left, down, right
        ally_color = 'w' if self.white_to_move else 'b'
        for d in directions:
            end_row = row + d[0]
            end_col = col + d[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if self.board[end_row][end_col][0] != ally_color:
                    moves.append(Move((row, col), (end_row, end_col), self.board))

    def  check_for_pins_and_checks(self):
        pins = [] # squares where the allied pinned piece is and directions pinned from
        checks = [] # squares where enemy is applying a check
        in_check = False
        if self.white_to_move:
            enemy_color = 'b'
            ally_color = 'w'
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = 'w'
            ally_color = 'b'
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]
        # check outward from king for pins and checks, keep track on pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color:
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_color:
                        piece_type = end_piece[1]
                        if (0 <= j <= 3 and piece_type == 'R') or \
                                (4 <= j <= 7 and piece_type == 'B') or \
                                (i == 1 and piece_type == 'p' and ((enemy_color == 'w' and 6 <= j <= 7) or (enemy_color == 'b' and 4 <= j <= 5))) or \
                                (piece_type == 'Q') or (i == 1 and piece_type == 'K'):
                            if possible_pin == (): # no peice blocking, so check
                                in_check = True
                                check.append((end_row, end_col, d[0], d[1]))
                                break
                            else: # piece blocking, so pin
                                pins.append(possible_pin)
                                break
                        else: # enemy piece not applying check
                            break
                else: # off board
                    break
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[0]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N': # enemy knight attacking king
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))
        return in_check, pins, checks

class Move():
    rows_to_ranks = {7: '1', 6: '2', 5: '3', 4: '4',
                     3: '5', 2: '6', 1: '7', 0: '8'}

    cols_to_files = {0: 'a', 1: 'b', 2: 'c', 3: 'd',
                     4: 'e', 5: 'f', 6: 'g', 7: 'h'}


    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)
