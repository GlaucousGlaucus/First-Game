from platform import python_branch
from pprint import pprint
from sys import exit
from matplotlib.pyplot import flag
import pygame

pygame.init()
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('RPG Survival | Dungeon Run') # Gives a title to the window
clock = pygame.time.Clock() # This will give a clock object
test_font = pygame.font.Font('Resources\Fonts\Pixeltype.ttf', 50) # (Font type, Font size) are arguments

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
Text_Surface = test_font.render('Dungeon Run', False, 'Black') # .render(text, Anti-Alias(Smooth edges), color)

# Snail
Snail_Surface = pygame.image.load('Resources\Images\Snail\snail1.png').convert_alpha() # 72x36
Snail_x = 600
SnailDirection = True
SnailSpeed = 0.5

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # To attach the regular surafce with the display surface
    # Needs two arguments (The surface, the position)
    # screen.blit(Test_Surface, (200, 100)) # BlIT: Block Image Transfer | You put one surface on top of another surface.
    
    # Here sky is rendered below the ground
    screen.blit(Sky_Surface, (0, 0))
    screen.blit(Ground_Surface, (0, 300))
    screen.blit(Text_Surface, (300, 50))

    # To and Fro Motion
    # Snail_x += -SnailSpeed if SnailDirection else SnailSpeed
    # if Snail_x == 0 or Snail_x >= 760:
    #     SnailDirection = not SnailDirection

    # Continous Motion
    # Snail_x -= SnailSpeed
    # if Snail_x < -72: Snail_x = 872

    screen.blit(Snail_Surface, (Snail_x, 264))

    # Draw all our elements and update everything
    pygame.display.update() # This updates the display created above
        