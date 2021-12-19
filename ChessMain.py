import pygame
import ChessEngine
import ChessAI
import Threads

board_width = board_height = 512
move_log_panel_width = 300
move_log_panel_height = board_height
dimension = 8
square_size = board_height // dimension
max_fps = 15
images = {}

'''
Initialize a global dictionnary of images.
'''
def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load('images/' + piece + '.png'), (square_size, square_size))

'''
The main driver for our code. This will handle user input and updating the graphics.
'''
def main():
    pygame.init()
    screen = pygame.display.set_mode((board_width + move_log_panel_width, board_height))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('white'))
    move_log_font = pygame.font.SysFont('Arial', 14, False, False)
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    animate = False

    load_images() #only do this once, before the while loop.
    running = True
    square_selected = ()
    player_clicks = []
    game_over = False
    player_one = False # white player, set False for AI, True for human
    player_two = False # black player, set False for AI, True for human
    ai_thinking = False
    move_undone = False

    move_finder_process = Threads.Threads()

    while running:
        human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                move_finder_process.kill()
                running = False
            # mouse handler
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    location = pygame.mouse.get_pos()
                    col = location[0] // square_size
                    row = location[1] // square_size
                    if square_selected == (row, col) or col >= 8:
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)
                    if len(player_clicks) == 2 and human_turn:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                        print(move.get_chess_notation())
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i])
                                move_made = True
                                animate = True # human animate
                                square_selected = ()
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected]
            # key handler
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z: # undo when 'z' is pressed
                    gs.undo_move()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

                if e.key == pygame.K_r: # reset the board when 'r' is pressed
                    gs = ChessEngine.GameState()
                    valid_moves = gs.get_valid_moves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

        # AI move finder
        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True

                print("Make Process")

                move_finder_process.start(gs, valid_moves)

            if not move_finder_process.is_alive():
                ai_move = move_finder_process.best_move()

                if ai_move == None:
                    ai_move = ChessAI.find_random_move(valid_moves)

                gs.make_move(ai_move)
                move_made = True
                animate = True # ai animate
                ai_thinking = False

        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock)
            valid_moves = gs.get_valid_moves()
            move_made = False
            animate = False
            move_undone = False

        draw_game_state(screen, gs, valid_moves, square_selected, move_log_font)

        if gs.check_mate or gs.stale_mate:
            game_over = True
            text = 'Stalemate' if gs.stale_mate else 'Black wins' if gs.white_to_move else 'White wins'
            draw_end_game_text(screen, text)

        clock.tick(max_fps)
        pygame.display.flip()

'''
Responsible for all the graphics within a current game state.
'''
def draw_game_state(screen, gs, valid_moves, square_selected, move_log_font):
    draw_board(screen)
    highlight_squares(screen, gs, valid_moves, square_selected)
    draw_pieces(screen, gs.board)
    draw_move_log(screen, gs, move_log_font)

'''
Draw the square on the board.
'''
def draw_board(screen):
    global colors
    colors = [pygame.Color('white'), pygame.Color('gray')]
    for row in range(dimension):
        for col in range(dimension):
            color = colors[((row + col) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(col*square_size, row*square_size, square_size, square_size))

'''
Highlight sqaure selected and moves for piece selected
'''
def highlight_squares(screen, gs, valid_moves, square_selected):
    if square_selected != ():
        row, col = square_selected
        if gs.board[row][col][0] == ('w' if gs.white_to_move else 'b'): # square_selected is a piece that can be moved
            # highlight selected square
            surf = pygame.Surface((square_size, square_size))
            surf.set_alpha(100)
            surf.fill(pygame.Color('green'))
            screen.blit(surf, (col*square_size, row*square_size))
            # highlight moves from that square
            surf.fill(pygame.Color('blue'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(surf, (move.end_col*square_size, move.end_row*square_size))

'''
Draw the pieces on the board using the current GameState.board.
'''
def draw_pieces(screen, board):
    for row in range(dimension):
        for col in range(dimension):
            piece = board[row][col]
            if piece != '--':
                screen.blit(images[piece], pygame.Rect(col*square_size, row*square_size, square_size, square_size))

'''
draws the move log
'''
def draw_move_log(screen, gs, font):
    move_log_rect = pygame.Rect(board_width, 0, move_log_panel_width, move_log_panel_height)
    pygame.draw.rect(screen, pygame.Color('black'), move_log_rect)
    move_log = gs.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + ' '
        if i + 1 < len(move_log):
            move_string += str(move_log[i+1]) + '    '
        move_texts.append(move_string)
    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ''
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i+j]
        text_object = font.render(text, True, pygame.Color('White'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing

'''
Animating a move
'''
def animate_move(move, screen, board, clock):
    global colors
    coords = [] # list of coords that the animation will move through
    delta_row = move.end_row - move.start_row
    delta_col = move.end_col - move.start_col
    frames_per_square = 10
    frame_count = (abs(delta_row) + abs(delta_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + delta_row*frame/frame_count, move.start_col + delta_col*frame/frame_count)
        draw_board(screen)
        draw_pieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = pygame.Rect(move.end_col*square_size, move.end_row*square_size, square_size, square_size)
        pygame.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.is_enpassant_move:
                end_square = pygame.Rect(move.end_col*square_size, move.start_row*square_size, square_size, square_size)
            screen.blit(images[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(images[move.piece_moved], pygame.Rect(col*square_size, row*square_size, square_size, square_size))
        pygame.display.flip()
        clock.tick(60)

def draw_end_game_text(screen, text):
    font = pygame.font.SysFont('Helvitca', 64, True, False)
    text_object = font.render(text, 0, pygame.Color('White'))
    text_location = pygame.Rect(0, 0, board_width, board_height).move(board_width/2 - text_object.get_width()/2, board_height/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, pygame.Color('Black'))
    screen.blit(text_object, text_location.move(2, 2))


if __name__ == '__main__':
    main()
