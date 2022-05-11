from pprint import pprint
from sys import exit
import utility as util

import pygame

pygame.init()
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('RPG Survival | Dungeon Run') # Gives a title to the window
clock = pygame.time.Clock() # This will give a clock object
test_font = pygame.font.Font('Resources\Fonts\ArchitectsDaughter-Regular.ttf', 25) # (Font type, Font size) are arguments

# pprint(pygame.color.THECOLORS)

# Surfaces

# Static Colors
# S1Width, S1Hight = 100, 200
# Test_Surface = pygame.Surface((S1Width, S1Hight))
# Test_Surface.fill('Red')

# Images
# Any kind of graphical import is going to be a new surface
Sky_Surface = pygame.image.load('Resources\Images\Sky.png').convert()
Ground_Surface = pygame.image.load('Resources\Images\ground.png').convert()

# Text
Text_Surface = test_font.render('Made By using: Pygame', True, 'White') # .render(text, Anti-Alias(Smooth edges), color)

# Snail
Snail_Surface = pygame.image.load('Resources\Images\Snail\snail1.png').convert_alpha() # 72x36
Snail_x = 600
SnailDirection = True
SnailSpeed = 3
Snail_rectangle = Snail_Surface.get_rect(midbottom = (600, 300))

# Player
Player_Surface = pygame.image.load('Resources\Images\Player\player_walk_1.png').convert_alpha()
# We can pygame.Rect(left, top, Player_rect_width, Player_rect_height) but we need a rectangle
# that is identical to the surface
Player_rectangle = Player_Surface.get_rect(midbottom = (80, 300))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Gets the pos of the mouse
        # print(util.MouseMotionCoords(pygame, event))

    # To attach the regular surafce with the display surface
    # Needs two arguments (The surface, the position)
    # screen.blit(Test_Surface, (200, 100)) # BlIT: Block Image Transfer | You put one surface on top of another surface.
    
    # Here sky is rendered below the ground
    screen.blit(Sky_Surface, (0, 0))
    screen.blit(Ground_Surface, (0, 300))
    screen.blit(Text_Surface, (20, 350))

    screen.blit(Snail_Surface, Snail_rectangle)
    screen.blit(Player_Surface, Player_rectangle)

    # util.cont_movement(Rect=Player_rectangle, speed=SnailSpeed, inverse=True)
    # SnailDirection = util.to_and_fro_movement(Snail_rectangle, SnailDirection, speed=SnailSpeed)

    # mouse_pos = pygame.mouse.get_pos()
    # if Player_rectangle.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
    #     print("Click")
    
    print(Player_rectangle.colliderect(Snail_rectangle))

    # Draw all our elements and update everything
    pygame.display.update() # This updates the display created above
    clock.tick(60)
        