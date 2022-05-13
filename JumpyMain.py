from csv import Sniffer
from sys import exit

import pygame

import utility as util
import random as rand

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  

        player_Walk1 = pygame.image.load('Resources\Images\Player\player_walk_1.png').convert_alpha()
        player_Walk2 = pygame.image.load('Resources\Images\Player\player_walk_2.png').convert_alpha()
        self.player_Walk = [player_Walk1, player_Walk2]
        self.player_index = 0
        self.player_Jump = pygame.image.load('Resources\Images\Player\jump.png').convert_alpha()

        self.image = self.player_Walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('Resources\Audio\\audio_jump.mp3')
        self.jump_sound.set_volume(0.15)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_Jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_Walk): self.player_index = 0
            self.image = self.player_Walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacles(pygame.sprite.Sprite):
    
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.anim_speed = {'Snail': 0.2, 'Fly': 0.1}[self.type]
        if type == "Snail":
            Frame_1 = pygame.image.load('Resources\Images\Snail\snail1.png').convert_alpha() # 72x36
            Frame_2 = pygame.image.load('Resources\Images\Snail\snail2.png').convert_alpha() # 72x36
            self.Frames = [Frame_1, Frame_2]
            ypos = 300
        elif type == "Fly":
            Frame_1 = pygame.image.load('Resources\Images\Fly\Fly1.png').convert_alpha() # 84x40
            Frame_2 = pygame.image.load('Resources\Images\Fly\Fly2.png').convert_alpha() # 84x40
            self.Frames = [Frame_1, Frame_2]
            ypos = 210 #TODO: Make the ypos random for Fly
        
        self.anim_index = 0
        self.image = self.Frames[self.anim_index]
        self.rect = self.image.get_rect(midbottom = (rand.randint(900, 1100), ypos))

    def animation_state(self):
        self.anim_index += self.anim_speed
        if self.anim_index >= len(self.Frames): self.anim_index = 0
        self.image = self.Frames[int(self.anim_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(round((pygame.time.get_ticks() - start_time) / 1000, 0))
    score_surface = score_font.render(f'  Score: {str(current_time)}  ', True, 'Black')
    score_rectangle = score_surface.get_rect(midbottom = (width // 2, 50))
    pygame.draw.rect(screen, '#947EC3', score_rectangle, 10) # surface, color, rect
    pygame.draw.rect(screen, (182, 137, 192), score_rectangle) # surface, color, rect
    screen.blit(score_surface, score_rectangle)
    return current_time

def collisionSprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True

# Initialization
pygame.init()
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('JUMPY!!') # Gives a title to the window
clock = pygame.time.Clock() # This will give a clock object
# (Font type, Font size) are arguments
test_font = pygame.font.Font('Resources\Fonts\Pixeltype.ttf', 50)
score_font = pygame.font.Font('Resources\Fonts\Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

# Sounds
pygame.mixer.init()
pygame.mixer.set_num_channels(8)
bg_voice = pygame.mixer.Channel(1)
bg_music = pygame.mixer.Sound('Resources\Audio\music.wav')
bg_music.set_volume(0.15)
bg_voice.play(bg_music)

game_over = pygame.mixer.Sound('Resources\Audio\game_over.wav')
game_over.set_volume(0.5)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Surfaces
sky_surface = pygame.image.load('Resources\Images\Sky.png').convert()
ground_surface = pygame.image.load('Resources\Images\ground.png').convert()
text_surface = test_font.render('Made By using: Pygame', False, 'White') # .render(text, Anti-Alias(Smooth edges), color)

# Intro Screen
title_surface = test_font.render('JUMPY!!', False, 'White')
title_rect = title_surface.get_rect(center = (width // 2, 50))

instructions_surface = test_font.render('Press ENTER To Play', False, 'White')
instructions_rect = instructions_surface.get_rect(center = (width // 2, 340))

player_stand = pygame.image.load('Resources\Images\Player\player_stand.png').convert_alpha() # 68x84
player_stand_roto = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle = player_stand_roto.get_rect(center = (400, 200))

# Game Over
playAgain_surface = score_font.render(f'Play Again', True, 'Black')
playAgain_rectangle = playAgain_surface.get_rect(center = (width // 2, 250))

fade_surface = pygame.Surface((width, height), pygame.SRCALPHA)
fade_surface.fill((148, 126, 195, 1))

# Timer(s)
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_anim_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_anim_timer, 500)

fly_anim_timer = pygame.USEREVENT + 3 
pygame.time.set_timer(fly_anim_timer, 200)

# Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacles(rand.choice(["Fly", "Snail", "Snail", "Snail", "Snail"])))

    if game_active == False and pygame.key.get_pressed()[pygame.K_RETURN]:
            game_active = True
            start_time = pygame.time.get_ticks()
    
    if game_active:
        # pygame.mixer.unpause()
        if not bg_voice.get_busy():
            bg_music.play(loops=-1)
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        screen.blit(text_surface, (20, 350))

        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collisionSprite()
        if not game_active:
            pygame.mixer.stop()
            game_over.play()

    else:
        screen.fill((148, 126, 195))
        screen.blit(fade_surface, (0,0)) 
        screen.blit(player_stand_roto, player_stand_rectangle)
        screen.blit(title_surface, title_rect)
        final_score_surface = test_font.render(f"Score: {score}", False, 'White')
        final_score_rect = final_score_surface.get_rect(center = (width // 2, 340))
        if score == 0:
            screen.blit(instructions_surface, instructions_rect)
        else:
            screen.blit(final_score_surface, final_score_rect)


    pygame.display.update()
    clock.tick(60)
        