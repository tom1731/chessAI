import pygame
from pygame.locals import *
import os

import ChessMain

# Game Initialization
pygame.init()

# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Game Resolution
screen_width = 800
screen_height = 700

# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText


# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Game Fonts
font = "Raleway-Regular.ttf"


# Game Framerate
clock = pygame.time.Clock()
FPS=15


# Main Menu
def main_menu():
    screen = pygame.display.set_mode((screen_width, screen_height))
    menu = True

    selected = 'start'
    player = '< 1 player >'
    side = '< white >'
    level = 0

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if selected == 'start':
                    if event.key == pygame.K_UP:
                        selected = 'quit'
                    elif event.key == pygame.K_DOWN:
                        selected = player

                elif selected == player:
                    if event.key == pygame.K_UP:
                        selected = 'start'
                    elif event.key == pygame.K_DOWN:
                        selected = side
                    elif player == '< 0 player >':
                        if event.key == pygame.K_RIGHT:
                            player = '< 1 player >'
                            selected = player
                        elif event.key == pygame.K_LEFT:
                            player = '< 2 players >'
                            selected = player
                    elif player == '< 1 player >':
                        if event.key == pygame.K_RIGHT:
                            player = '< 2 players >'
                            selected = player
                        elif event.key == pygame.K_LEFT:
                            player = '< 0 player >'
                            selected = player
                    elif player == '< 2 players >':
                        if event.key == pygame.K_RIGHT:
                            player = '< 0 player >'
                            selected = player
                        elif event.key == pygame.K_LEFT:
                            player = '< 1 player >'
                            selected = player

                elif selected == side:
                    if event.key == pygame.K_UP:
                        selected = player
                    elif event.key == pygame.K_DOWN:
                        selected = level
                    elif side == '< white >':
                        if event.key == pygame.K_RIGHT:
                            side = '< black >'
                            selected = side
                        elif event.key == pygame.K_LEFT:
                            side = '< black >'
                            selected = side
                    elif side == '< black >':
                        if event.key == pygame.K_RIGHT:
                            side = '< white >'
                            selected = side
                        elif event.key == pygame.K_LEFT:
                            side = '< white >'
                            selected = side

                elif selected == level:
                    if event.key == pygame.K_UP:
                        selected = side
                    elif event.key == pygame.K_DOWN:
                        selected = 'quit'
                    elif event.key == pygame.K_RIGHT:
                        if level < 2:
                            level += 1
                        else:
                            level = 0
                        selected = level
                    elif event.key == pygame.K_LEFT:
                        if level > 0:
                            level -= 1
                        else:
                            level = 2
                        selected = level

                elif selected == 'quit':
                    if event.key == pygame.K_UP:
                        selected = level
                    elif event.key == pygame.K_DOWN:
                        selected = 'start'

                if player == '< 0 player >':
                    player_one = False
                    player_two = False
                elif player == '< 1 player >':
                    if side == '< white >':
                        player_one = True
                        player_two = False
                    elif side == '< black >':
                        player_one = False
                        player_two = True
                elif player == '< 2 players >':
                    player_one = True
                    player_two = True

                if event.key == pygame.K_RETURN:
                    if selected == 'start':
                        ChessMain.main(player_one, player_two, level)
                    elif selected == 'quit':
                        pygame.quit()
                        quit()


        # Main Menu UI
        screen.fill(blue)
        title=text_format('Chess AI', font, 90, yellow)

        if selected == 'start':
            text_start = text_format('PLAY', font, 75, white)
        else:
            text_start = text_format('PLAY', font, 75, black)

        if selected == player:
            text_player = text_format(player, font, 75, white)
        else:
            text_player = text_format(player, font, 75, black)

        if selected == side:
            text_side = text_format(side, font, 75, white)
        else:
            text_side = text_format(side, font, 75, black)

        if selected == level:
            text_level = text_format(f'Level : < {level} >', font, 75, white)
        else:
            text_level = text_format(f'Level : < {level} >', font, 75, black)

        if selected == 'quit':
            text_quit = text_format('exit', font, 75, white)
        else:
            text_quit = text_format('exit', font, 75, black)


        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        player_rect = text_player.get_rect()
        side_rect = text_side.get_rect()
        level_rect = text_level.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 20))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 200))
        screen.blit(text_player, (screen_width/2 - (player_rect[2]/2), 300))
        screen.blit(text_side, (screen_width/2 - (side_rect[2]/2), 400))
        screen.blit(text_level, (screen_width/2 - (level_rect[2]/2), 500))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 600))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main_menu()
