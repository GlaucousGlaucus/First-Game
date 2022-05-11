from sys import exit

import pygame

import utility as util

pygame.init()
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('RPG Survival | Dungeon Run') # Gives a title to the window
clock = pygame.time.Clock() # This will give a clock object
test_font = pygame.font.Font('Resources\Fonts\ArchitectsDaughter-Regular.ttf', 25) # (Font type, Font size) are arguments
score_font = pygame.font.Font('Resources\Fonts\Kalam-Light.ttf', 25) # (Font type, Font size) are arguments

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

score = 0

# Player
Player_Surface = pygame.image.load('Resources\Images\Player\player_walk_1.png').convert_alpha()
# We can pygame.Rect(left, top, Player_rect_width, Player_rect_height) but we need a rectangle
# that is identical to the surface
Player_rectangle = Player_Surface.get_rect(midbottom = (80, 300))
Player_Gravity = 0

# UI
Score_Surface = score_font.render(f'Score: {score}', True, 'Black')
Score_rectangle = Score_Surface.get_rect(midbottom = (width // 2, 50))

# Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and Player_rectangle.bottom == 300:
                Player_Gravity = -20
        # if event.type == pygame.KEYUP:
        #     print("Keyup")

        if event.type == pygame.MOUSEBUTTONDOWN:
            if Player_rectangle.collidepoint(event.pos) and Player_rectangle.bottom == 300: Player_Gravity = -20

        # Gets the pos of the mouse
        # coords = util.MouseMotionCoords(pygame, event)

    # To attach the regular surafce with the display surface
    # Needs two arguments (The surface, the position)
    # screen.blit(Test_Surface, (200, 100)) # BlIT: Block Image Transfer | You put one surface on top of another surface.
    
    # Here sky is rendered below the ground
    screen.blit(Sky_Surface, (0, 0))
    screen.blit(Ground_Surface, (0, 300))
    screen.blit(Text_Surface, (20, 350))

    screen.blit(Snail_Surface, Snail_rectangle)

    # Player
    Player_Gravity += 1
    Player_rectangle.y += Player_Gravity
    if Player_rectangle.bottom >= 300: Player_rectangle.bottom = 300
    screen.blit(Player_Surface, Player_rectangle)


    pygame.draw.rect(screen, '#947EC3', Score_rectangle, 10) # surface, color, rect
    pygame.draw.rect(screen, (182, 137, 192), Score_rectangle) # surface, color, rect
    screen.blit(Score_Surface, Score_rectangle)

    # pygame.draw.line(screen, 'Red', (0,0), pygame.mouse.get_pos())

    # util.cont_movement(Rect=Player_rectangle, speed=SnailSpeed, inverse=True)
    SnailDirection = util.to_and_fro_movement(Snail_rectangle, SnailDirection, speed=SnailSpeed)

    # Draw all our elements and update everything
    pygame.display.update() # This updates the display created above
    clock.tick(60)
        