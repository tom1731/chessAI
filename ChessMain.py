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

    load_images() #only do this once, before the while loop.
    running = True
    square_selected = ()
    player_clicks = []

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            # mouse handler
            elif e.type == pygame.MOUSEBUTTONDOWN:
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
                    if move in valid_moves:
                        gs.make_move(move)
                        move_made = True
                        square_selected = ()
                        player_clicks = []
                        print(move.get_chess_notation())
                    else:
                        player_clicks = [square_selected]
            # key handler
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z: # undo when z is pressed
                    gs.undo_move()
                    move_made = True

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False
        draw_game_state(screen, gs)
        clock.tick(max_fps)
        pygame.display.flip()

'''
Responsible for all the graphics within a current game state.
'''
def draw_game_state(screen, gs):
    draw_board(screen)
    draw_pieces(screen, gs.board)

'''
Draw the square on the board.
'''
def draw_board(screen):
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









if __name__ == '__main__':
    main()
