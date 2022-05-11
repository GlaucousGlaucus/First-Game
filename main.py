from sys import exit

import pygame

import utility as util

def display_score():
    current_time = int(round((pygame.time.get_ticks() - StartTime) / 1000, 0))
    Score_Surface = score_font.render(f'  Score: {str(current_time)}  ', True, 'Black')
    Score_rectangle = Score_Surface.get_rect(midbottom = (width // 2, 50))
    pygame.draw.rect(screen, '#947EC3', Score_rectangle, 10) # surface, color, rect
    pygame.draw.rect(screen, (182, 137, 192), Score_rectangle) # surface, color, rect
    screen.blit(Score_Surface, Score_rectangle)
    return current_time

pygame.init()
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('JUMPY!!') # Gives a title to the window
clock = pygame.time.Clock() # This will give a clock object
test_font = pygame.font.Font('Resources\Fonts\Pixeltype.ttf', 50) # (Font type, Font size) are arguments
score_font = pygame.font.Font('Resources\Fonts\Pixeltype.ttf', 50) # (Font type, Font size) are arguments
GameActive = False
StartTime = 0
score = 0

# Images
# Any kind of graphical import is going to be a new surface
Sky_Surface = pygame.image.load('Resources\Images\Sky.png').convert()
Ground_Surface = pygame.image.load('Resources\Images\ground.png').convert()

# Text
Text_Surface = test_font.render('Made By using: Pygame', False, 'White') # .render(text, Anti-Alias(Smooth edges), color)

# Snail
Snail_Surface = pygame.image.load('Resources\Images\Snail\snail1.png').convert_alpha() # 72x36
Snail_x = 600
SnailDirection = True
SnailSpeed = 4
Snail_rectangle = Snail_Surface.get_rect(midbottom = (600, 300))

# Player
Player_Surface = pygame.image.load('Resources\Images\Player\player_walk_1.png').convert_alpha()
# We can pygame.Rect(left, top, Player_rect_width, Player_rect_height) but we need a rectangle
# that is identical to the surface
Player_rectangle = Player_Surface.get_rect(midbottom = (80, 300))
Player_Gravity = 0
Jump_factor = -25

# Intro Screen
# JUMPY
Title_Surface = test_font.render('JUMPY!!', False, 'White')
Title_Rect = Title_Surface.get_rect(center = (width // 2, 50))

Instructions_Surface = test_font.render('Press SPACE To Play', False, 'White')
Instructions_Rect = Instructions_Surface.get_rect(center = (width // 2, 340))

Player_Stand = pygame.image.load('Resources\Images\Player\player_stand.png').convert_alpha() # 68x84
Player_Stand_ROTO = pygame.transform.rotozoom(Player_Stand, 0, 2)
Player_Stand_rectangle = Player_Stand_ROTO.get_rect(center = (400, 200))

# Game Over
PlayAgain_Surface = score_font.render(f'Play Again', True, 'Black')
PLayAgain_rectangle = PlayAgain_Surface.get_rect(center = (width // 2, 250))

FadeSurface = pygame.Surface((width, height), pygame.SRCALPHA)
FadeSurface.fill((148, 126, 195, 1))

# Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if GameActive:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and Player_rectangle.bottom == 300:
                    Player_Gravity = Jump_factor
            # if event.type == pygame.KEYUP:
            #     print("Keyup")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if Player_rectangle.collidepoint(event.pos) and Player_rectangle.bottom == 300: 
                    Player_Gravity = Jump_factor
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                GameActive = True
                Snail_rectangle.left = 800
                StartTime = pygame.time.get_ticks()

        # Gets the pos of the mouse
        # coords = util.MouseMotionCoords(pygame, event)

    # To attach the regular surafce with the display surface
    # Needs two arguments (The surface, the position)
    # screen.blit(Test_Surface, (200, 100)) # BlIT: Block Image Transfer | You put one surface on top of another surface.
    
    if GameActive:
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

        # Score

        # pygame.draw.rect(screen, '#947EC3', Score_rectangle, 10) # surface, color, rect
        # pygame.draw.rect(screen, (182, 137, 192), Score_rectangle) # surface, color, rect
        # screen.blit(Score_Surface, Score_rectangle)
        score = display_score()

        # pygame.draw.line(screen, 'Red', (0,0), pygame.mouse.get_pos())

        util.cont_movement(Rect=Snail_rectangle, speed=SnailSpeed)
        # SnailDirection = util.to_and_fro_movement(Snail_rectangle, SnailDirection, speed=SnailSpeed)

        # Collision
        if Snail_rectangle.colliderect(Player_rectangle):
            GameActive = False
    else:
        screen.fill((148, 126, 195))
        screen.blit(FadeSurface, (0,0)) 
        screen.blit(Player_Stand_ROTO, Player_Stand_rectangle)
        screen.blit(Title_Surface, Title_Rect)
        TScore_Surface = test_font.render(f"Score: {score}", False, 'White')
        TScore_Rect = TScore_Surface.get_rect(center = (width // 2, 340))
        if score == 0:
            screen.blit(Instructions_Surface, Instructions_Rect)
        else:
            screen.blit(TScore_Surface, TScore_Rect)

    # Draw all our elements and update everything
    pygame.display.update() # This updates the display created above
    clock.tick(60)
        