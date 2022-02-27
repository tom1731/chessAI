import pygame
import ChessEngine
# import ChessAI
import ChessStockfish
import main
from multiprocessing import Process, Queue

board_width = board_height = 512
move_log_panel_width = 300
move_log_panel_height = board_height
dimension = 8
square_size = board_height // dimension
max_fps = 15
images = {}


'''
The main driver for our code. This will handle user input and updating the graphics.
'''
def main_game(player_one, player_two, side, level):
    global human_turn
    player_one, player_two = player_one, player_two
    stockfish = ChessStockfish.stockfish_init(level)
    pygame.init()
    screen = pygame.display.set_mode((board_width + move_log_panel_width, board_height))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('white'))
    move_log_font = pygame.font.SysFont('Arial', 14, False, False)
    gs = ChessEngine.GameState(side)
    valid_moves = gs.get_valid_moves(side)
    move_made = False
    animate = False

    load_images() #only do this once, before the while loop.
    running = True
    square_selected = ()
    player_clicks = []
    game_over = False
    ai_thinking = False
    move_finder_process = None
    move_undone = False

    while running:
        human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
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
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i], side)
                                move_made = True
                                animate = True # human animate
                                square_selected = ()
                                player_clicks = []
                        if not move_made:
                            player_clicks = [square_selected]
            # key handler
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                    main.main_menu()
                if e.key == pygame.K_z: # undo when 'z' is pressed
                    if len(gs.move_log) > 1:
                        gs.undo_move(side)
                    else:
                        gs = ChessEngine.GameState(side)
                    square_selected = ()
                    player_clicks = []
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True

                if e.key == pygame.K_r: # reset the board when 'r' is pressed
                    gs = ChessEngine.GameState(side)
                    valid_moves = gs.get_valid_moves(side)
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False

        # # AI move finder
        # if not game_over and not human_turn and not move_undone:
        #     if not ai_thinking:
        #         ai_thinking = True
        #         return_queue = Queue()
        #         move_finder_process = Process(target=ChessAI.find_best_move, args=(gs, valid_moves, depth_game, return_queue))
        #         move_finder_process.start()

        #     if not move_finder_process.is_alive():
        #         ai_move = return_queue.get()
        #         if ai_move == None:
        #             ai_move = ChessAI.find_random_move(valid_moves)
        #         gs.make_move(ai_move)
        #         move_made = True
        #         animate = True # ai animate
        #         ai_thinking = False

        # StockFish
        if not game_over and not human_turn and not move_undone:
            best_move = ChessStockfish.find_position(gs.sf_move_log, stockfish)
            start_square = ChessStockfish.convert_best_move(best_move)[0]
            end_square = ChessStockfish.convert_best_move(best_move)[1]
            move = ChessEngine.Move(start_square, end_square, gs.board)
            for i in range(len(valid_moves)):
                if move == valid_moves[i]:
                    gs.make_move(valid_moves[i], side)
            move_made = True
            animate = True  # ai animate

        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock, move_log_font, side)
            valid_moves = gs.get_valid_moves(side)
            move_made = False
            animate = False
            move_undone = False

        draw_game_state(screen, gs, valid_moves, square_selected, move_log_font, side)

        if gs.check_mate or gs.draw:
            game_over = True
            draw_end_game_text(screen, gs.end_text)

        clock.tick(max_fps)
        pygame.display.flip()


'''
Initialize a global dictionnary of images.
'''
def load_images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ',
              'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(
            'images/' + piece + '.png').convert_alpha(), (square_size, square_size))


'''
Responsible for all the graphics within a current game state.
'''
def draw_game_state(screen, gs, valid_moves, square_selected, move_log_font, side):
    draw_board(screen, move_log_font, side)
    highlight_squares(screen, gs, valid_moves, square_selected)
    draw_pieces(screen, gs.board)
    draw_move_log(screen, gs, move_log_font)


'''
Draw the square on the board.
'''
def draw_board(screen, font, side):
    global colors
    colors = [pygame.Color('white'), pygame.Color('gray')]

    if side == '< white >':
        text_letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        text_number = ['8', '7', '6', '5', '4', '3', '2', '1']
    else:
        text_letter = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']
        text_number = ['1', '2', '3', '4', '5', '6', '7', '8']


    for row in range(dimension):
        for col in range(dimension):
            color = colors[((row + col) % 2)]
            square_rect = pygame.draw.rect(screen, color, pygame.Rect(col*square_size, row*square_size, square_size, square_size))
            square_rect

            if row == 7:
                text_location = square_rect.move(53, 48)
                text_object = font.render(text_letter[col], True, pygame.Color('Black'))
                screen.blit(text_object, text_location)

            if col == 0:
                text_location = square_rect.move(2, 2)
                text_object = font.render(text_number[row], True, pygame.Color('Black'))
                screen.blit(text_object, text_location)


'''
Highlight sqaure selected and moves for piece selected
'''
def highlight_squares(screen, gs, valid_moves, square_selected):
    surf = pygame.Surface((square_size, square_size))
    surf.set_alpha(100)

    # highlight previous move
    if len(gs.move_log) > 0:
        start_row = gs.move_log[-1].start_row
        start_col = gs.move_log[-1].start_col
        end_row = gs.move_log[-1].end_row
        end_col = gs.move_log[-1].end_col

        # highlight previous move start square
        surf.fill(pygame.Color('yellow'))
        screen.blit(surf, (start_col*square_size, start_row*square_size))

        # highlight previous move end square
        surf.fill(pygame.Color('yellow'))
        screen.blit(surf, (end_col*square_size, end_row*square_size))

    # highlight select square and valid moves
    if square_selected != () and human_turn:
        row, col = square_selected
        if gs.board[row][col][0] == ('w' if gs.white_to_move else 'b'): # square_selected is a piece that can be moved
            # highlight selected square
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
    check_notation = []
    for i in gs.in_check_log:
        if i:
            check_notation.append('+')
        else:
            check_notation.append('')
    move_texts = []
    for i in range(0, len(move_log), 2):
        if gs.check_mate:
            check_notation[-1] = '#'
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + check_notation[i]
        move_texts.append(move_string)
        if i + 1 < len(move_log):
            move_string = str(move_log[i+1]) + check_notation[i+1]
            move_texts.append(move_string)
    line_spacing = 5
    text_y = 5
    for i in range(len(move_texts)):
        text = ''
        if i < 50:
            padding = 5
        else:
            padding = 160
        if i == 50:
            text_y = 5
        if i < len(move_texts):
            text += move_texts[i]

        text_object = font.render(text, True, pygame.Color('White'))

        if i > 0 and i != 50:
            if i % 2 == 0:
                text_y += text_object.get_height() + line_spacing
            else:
                padding += 75

        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)


'''
Animating a move
'''
def animate_move(move, screen, board, clock, move_log_font, side):
    global colors
    delta_row = move.end_row - move.start_row
    delta_col = move.end_col - move.start_col
    frames_per_square = 10
    frame_count = (abs(delta_row) + abs(delta_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + delta_row*frame/frame_count, move.start_col + delta_col*frame/frame_count)
        draw_board(screen, move_log_font, side)
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
    font = pygame.font.SysFont('Helvitca', 32, True, False)
    text_object = font.render(text, 0, pygame.Color('white'))
    text_location = pygame.Rect(0, 0, board_width, board_height).move(board_width/2 - text_object.get_width()/2, board_height/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, pygame.Color('blue'))
    screen.blit(text_object, text_location.move(2, 2))
