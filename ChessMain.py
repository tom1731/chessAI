import pygame
import ChessEngine

width = height = 512
dimension = 8
square_size = height // dimension
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
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('white'))
    gs = ChessEngine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    animate = False

    load_images() #only do this once, before the while loop.
    running = True
    square_selected = ()
    player_clicks = []
    game_over = False

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            # mouse handler
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    location = pygame.mouse.get_pos()
                    col = location[0] // square_size
                    row = location[1] // square_size
                    if square_selected == (row, col):
                        square_selected = ()
                        player_clicks = []
                    else:
                        square_selected = (row, col)
                        player_clicks.append(square_selected)
                    if len(player_clicks) == 2:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                        print(move.get_chess_notation())
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i])
                                move_made = True
                                animate = True
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
                if e.key == pygame.K_r: # reset the board when 'r' is pressed
                    gs = ChessEngine.GameState()
                    valid_moves = gs.get_valid_moves()
                    square_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False

        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock)
            valid_moves = gs.get_valid_moves()
            move_made = False
            animate = False

        draw_game_state(screen, gs, valid_moves, square_selected)

        if gs.check_mate:
            game_over = True
            if gs.white_to_move:
                draw_text(screen, 'Black wins')
            else:
                draw_text(screen, 'White wins')
        elif gs.stale_mate:
            game_over = True
            draw_text(screen, 'Stalemate')

        clock.tick(max_fps)
        pygame.display.flip()

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
Responsible for all the graphics within a current game state.
'''
def draw_game_state(screen, gs, valid_moves, square_selected):
    draw_board(screen)
    highlight_squares(screen, gs, valid_moves, square_selected)
    draw_pieces(screen, gs.board)

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
Draw the pieces on the board using the current GameState.board.
'''
def draw_pieces(screen, board):
    for row in range(dimension):
        for col in range(dimension):
            piece = board[row][col]
            if piece != '--':
                screen.blit(images[piece], pygame.Rect(col*square_size, row*square_size, square_size, square_size))

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
            screen.blit(images[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(images[move.piece_moved], pygame.Rect(col*square_size, row*square_size, square_size, square_size))
        pygame.display.flip()
        clock.tick(60)

def draw_text(screen, text):
    font = pygame.font.SysFont('Helvitca', 64, True, False)
    text_object = font.render(text, 0, pygame.Color('White'))
    text_location = pygame.Rect(0, 0, width, height).move(width/2 - text_object.get_width()/2, height/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, pygame.Color('Black'))
    screen.blit(text_object, text_location.move(2, 2))


if __name__ == '__main__':
    main()
