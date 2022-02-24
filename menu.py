import pygame
from pygame.locals import *
import os

# Game Initialization
pygame.init()

# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Game Resolution
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

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

    menu=True
    selected="start"

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
                        selected = '< 1 player >'

                if selected == '< 1 player >':
                    if event.key == pygame.K_UP:
                        selected = 'start'
                    elif event.key == pygame.K_DOWN:
                        selected = '< white >'

                if selected == '< white >':
                    if event.key == pygame.K_UP:
                        selected = '< 1 player >'
                    elif event.key == pygame.K_DOWN:
                        selected = 'quit'

                if selected == 'quit':
                    if event.key == pygame.K_UP:
                        selected = '< white >'
                    elif event.key == pygame.K_DOWN:
                        selected = 'start'

                if event.key == pygame.K_RETURN:
                    if selected == 'start':
                        print('Start')
                    if selected == 'quit':
                        pygame.quit()
                        quit()

                print(selected)


        # Main Menu UI
        screen.fill(blue)
        title=text_format('Chess AI', font, 90, yellow)

        if selected=='start':
            text_start=text_format('PLAY', font, 75, white)
        else:
            text_start = text_format('PLAY', font, 75, black)

        if selected=='< 1 player >':
            text_player=text_format('< 1 player >', font, 75, white)
        else:
            text_player = text_format('< 1 player >', font, 75, black)

        if selected=='< white >':
            text_side=text_format('< white >', font, 75, white)
        else:
            text_side = text_format('< white >', font, 75, black)

        if selected=='quit':
            text_quit=text_format('exit', font, 75, white)
        else:
            text_quit = text_format('exit', font, 75, black)


        title_rect = title.get_rect()
        start_rect = text_start.get_rect()
        player_rect = text_player.get_rect()
        side_rect = text_side.get_rect()
        quit_rect = text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 20))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 200))
        screen.blit(text_player, (screen_width/2 - (player_rect[2]/2), 300))
        screen.blit(text_side, (screen_width/2 - (side_rect[2]/2), 400))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 500))
        pygame.display.update()
        clock.tick(FPS)



if __name__ == '__main__':
    main_menu()
