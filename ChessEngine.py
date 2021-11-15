class GameState():
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', 'bR', '--', 'wR', '--', '--', '--', '--'],
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

    '''
    Takes a move as a parameter and executes it (not work with castling, pawn prootion and en-passant)
    '''
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = '--'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    '''
    All moves considering checks
    '''
    def get_valid_moves(self):
        return self.get_all_possible_moves()

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
        if self.white_to_move: # white pawn move
            if self.board[row-1][col] == '--': # 1 square pawn move
                moves.append(Move((row, col), (row-1, col), self.board))
                if row == 6 and self.board[row-2][col] == '--': # 2 square pawn move
                    moves.append(Move((row, col), (row-2, col), self.board))
            if col-1 >= 0:  # ennemy piece to capture to the left
                if self.board[row-1][col-1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col-1), self.board))
            if col+1 <= 7:  # ennemy piece to capture to the right
                if self.board[row-1][col+1][0] == 'b':
                    moves.append(Move((row, col), (row-1, col+1), self.board))

        else:  # black pawn move
            if self.board[row+1][col] == '--':  # 1 square pawn move
                moves.append(Move((row, col), (row+1, col), self.board))
                if row == 1 and self.board[row+2][col] == '--': # 2 square pawn move
                    moves.append(Move((row, col), (row+2, col), self.board))
            if col-1 >= 0:  # ennemy piece to capture to the left
                if self.board[row+1][col-1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col-1), self.board))
            if col+1 <= 7:  # ennemy piece to capture to the right
                if self.board[row+1][col+1][0] == 'w':
                    moves.append(Move((row, col), (row+1, col+1), self.board))

    '''
    Get all the rook moves for the pawn located at row, col and add these moves to the list
    '''
    def get_rook_moves(self, row, col, moves):
        if self.white_to_move: # white rook move
            end_col = col # horizontal move
            while end_col-1 >= 0:
                end_col -= 1
                if self.board[row][end_col] == '--': # left move
                    moves.append(Move((row, col), (row, end_col), self.board))
                elif self.board[row][end_col][0] == 'b': # left capture
                    moves.append(Move((row, col), (row, end_col), self.board))
                    break
                else: break
            end_col = col
            while end_col+1 <= 7:
                end_col += 1
                if self.board[row][end_col] == '--': # right move
                    moves.append(Move((row, col), (row, end_col), self.board))
                elif self.board[row][end_col][0] == 'b': # right capture
                    moves.append(Move((row, col), (row, end_col), self.board))
                    break
                else: break
            end_row = row # vertical move
            while end_row-1 >= 0:
                end_row -= 1
                if self.board[end_row][col] == '--': # up move
                    moves.append(Move((row, col), (end_row, col), self.board))
                elif self.board[end_row][col][0] == 'b': # up capture
                    moves.append(Move((row, col), (end_row, col), self.board))
                    break
                else: break
            end_row = row
            while end_row+1 <= 7:
                end_row += 1
                if self.board[end_row][col] == '--': # down move
                    moves.append(Move((row, col), (end_row, col), self.board))
                elif self.board[end_row][col][0] == 'b': # down capture
                    moves.append(Move((row, col), (end_row, col), self.board))
                    break
                else: break

        else: # black rook move
            end_col = col # horizontal move
            while end_col-1 >= 0:
                end_col -= 1
                if self.board[row][end_col] == '--': # left move
                    moves.append(Move((row, col), (row, end_col), self.board))
                elif self.board[row][end_col][0] == 'w': # left capture
                    moves.append(Move((row, col), (row, end_col), self.board))
                    break
                else: break
            end_col = col
            while end_col+1 <= 7:
                end_col += 1
                if self.board[row][end_col] == '--': # right move
                    moves.append(Move((row, col), (row, end_col), self.board))
                elif self.board[row][end_col][0] == 'w': # right capture
                    moves.append(Move((row, col), (row, end_col), self.board))
                    break
                else: break
            end_row = row # vertical move
            while end_row-1 >= 0:
                end_row -= 1
                if self.board[end_row][col] == '--': # up move
                    moves.append(Move((row, col), (end_row, col), self.board))
                elif self.board[end_row][col][0] == 'w': # up capture
                    moves.append(Move((row, col), (end_row, col), self.board))
                    break
                else: break
            end_row = row
            while end_row+1 <= 7:
                end_row += 1
                if self.board[end_row][col] == '--': # down move
                    moves.append(Move((row, col), (end_row, col), self.board))
                elif self.board[end_row][col][0] == 'w': # down capture
                    moves.append(Move((row, col), (end_row, col), self.board))
                    break
                else: break



    '''
    Get all the knight moves for the pawn located at row, col and add these moves to the list
    '''
    def get_knight_moves(self, row, col, moves):
        pass

    '''
    Get all the bishop moves for the pawn located at row, col and add these moves to the list
    '''
    def get_bishop_moves(self, row, col, moves):
        pass

    '''
    Get all the queen moves for the pawn located at row, col and add these moves to the list
    '''
    def get_queen_moves(self, row, col, moves):
        pass

    '''
    Get all the king moves for the pawn located at row, col and add these moves to the list
    '''
    def get_king_moves(self, row, col, moves):
        pass

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
