from errno import ENOTRECOVERABLE
from platform import python_branch
from sys import exit
from unittest import mock

import pygame

import random as rand


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_Walk1 = pygame.image.load(
            'Resources\Images\Player\player_walk_1.png').convert_alpha()
        player_Walk2 = pygame.image.load(
            'Resources\Images\Player\player_walk_2.png').convert_alpha()
        self.player_Walk = [player_Walk1, player_Walk2]
        self.player_index = 0
        self.player_Jump = pygame.image.load(
            'Resources\Images\Player\jump.png').convert_alpha()

        self.image = self.player_Walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
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
            if self.player_index >= len(self.player_Walk):
                self.player_index = 0
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
            Frame_1 = pygame.image.load(
                'Resources\Images\Snail\snail1.png').convert_alpha()  # 72x36
            Frame_2 = pygame.image.load(
                'Resources\Images\Snail\snail2.png').convert_alpha()  # 72x36
            self.Frames = [Frame_1, Frame_2]
            ypos = 300
        elif type == "Fly":
            Frame_1 = pygame.image.load(
                'Resources\Images\Fly\Fly1.png').convert_alpha()  # 84x40
            Frame_2 = pygame.image.load(
                'Resources\Images\Fly\Fly2.png').convert_alpha()  # 84x40
            self.Frames = [Frame_1, Frame_2]
            ypos = rand.randint(150, 210)

        self.anim_index = 0
        self.image = self.Frames[self.anim_index]
        self.rect = self.image.get_rect(
            midbottom=(rand.randint(900, 1100), ypos))

    def animation_state(self):
        self.anim_index += self.anim_speed
        if self.anim_index >= len(self.Frames):
            self.anim_index = 0
        self.image = self.Frames[int(self.anim_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


class GameOverFade(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.rect = pygame.display.get_surface().get_rect()
        self.image = pygame.Surface(self.rect.size, flags=pygame.SRCALPHA)
        self.alpha = 0

    def update(self):
        self.image.fill((148, 126, 195, self.alpha))
        if not self.alpha >= 255:
            self.alpha += 1


class PlayBtn(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        ratio = 70
        scale_fac = 2 * ratio, 1 * ratio
        play_btn_surface_1 = pygame.image.load('Resources\Images\GUI\Play_btn_1.png').convert_alpha()
        self.play_btn_surface_1 = pygame.transform.smoothscale(play_btn_surface_1, scale_fac)
        play_btn_surface_2 = pygame.image.load('Resources\Images\GUI\Play_btn_2.png').convert_alpha()
        self.play_btn_surface_2 = pygame.transform.smoothscale(play_btn_surface_2, scale_fac)
        play_btn_surface_3 = pygame.image.load('Resources\Images\GUI\Play_btn_3.png').convert_alpha()
        self.play_btn_surface_3 = pygame.transform.smoothscale(play_btn_surface_3, scale_fac)

        self.image = self.play_btn_surface_1
        self.rect = self.image.get_rect(center=(width//2 - 100, 250))
        
    
    def animation_state(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.play_btn_surface_3 if pygame.mouse.get_pressed()[0] else self.play_btn_surface_2
        else:
            self.image = self.play_btn_surface_1

    def update(self, game_state):
        self.animation_state()

def display_score():
    current_time = int(round((pygame.time.get_ticks() - start_time) / 1000, 0))
    score_surface = score_font.render(
        f'  Score: {str(current_time)}  ', True, 'Black')
    score_rectangle = score_surface.get_rect(midbottom=(width // 2, 50))
    pygame.draw.rect(screen, '#947EC3', score_rectangle,
                     10)
    pygame.draw.rect(screen, (182, 137, 192), score_rectangle)
    screen.blit(score_surface, score_rectangle)
    return current_time


def collisionSprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        player.sprite.rect.bottom = 300
        return False
    return True


# Initialization
pygame.init()
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('JUMPY!!')  # Gives a title to the window
clock = pygame.time.Clock()  # This will give a clock object
game_state = "main_menu"  # TODO Make enum for game state
start_time = 0
score = 0

# Fonts
test_font = pygame.font.Font('Resources\Fonts\Pixeltype.ttf', 50)
score_font = pygame.font.Font('Resources\Fonts\Pixeltype.ttf', 50)
title_font = pygame.font.Font('Resources\Fonts\Fipps-Regular.otf', 50)

# Sounds
pygame.mixer.init()
pygame.mixer.set_num_channels(8)
bg_voice = pygame.mixer.Channel(1)
bg_music = pygame.mixer.Sound('Resources\Audio\music.wav')
bg_music.set_volume(0.15)
bg_voice.play(bg_music)

btn_voice = pygame.mixer.Channel(2)
btn_sound = pygame.mixer.Sound(r'Resources\Audio\btn_click.wav')

game_over = pygame.mixer.Sound('Resources\Audio\game_over.wav')
game_over.set_volume(0.5)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Surfaces
sky_surface = pygame.image.load('Resources\Images\Sky.png').convert()
ground_surface = pygame.image.load('Resources\Images\ground.png').convert()
made_by_surface = test_font.render('Made By using: Pygame', False, 'White')

# Main Menu
title_surface = pygame.image.load('Resources\Images\Logo4.png').convert_alpha() # 996 x 316
title_ratio = 150
title_scale_fac = (3.15 * title_ratio, 1 * title_ratio)
title_surface = pygame.transform.smoothscale(title_surface, title_scale_fac)
play_btn = pygame.sprite.GroupSingle(PlayBtn())

# Intro Screen
instructions_surface = test_font.render('Press ENTER To Play', False, 'White')
instructions_rect = instructions_surface.get_rect(center=(width // 2, 340))

player_stand = pygame.image.load(
    'Resources\Images\Player\player_stand.png').convert_alpha()  # 68x84
player_stand_roto = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle = player_stand_roto.get_rect(center=(400, 200))

# Game Over
playAgain_surface = score_font.render(f'Play Again', True, 'Black')
playAgain_rectangle = playAgain_surface.get_rect(center=(width // 2, 250))
fade = pygame.sprite.GroupSingle(GameOverFade())

# Timer(s)
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_anim_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_anim_timer, 500)

fly_anim_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_anim_timer, 200)

# Main Loop
while True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_state == "in_game" and event.type == obstacle_timer:
            obstacle_group.add(Obstacles(rand.choice(
                ["Fly", "Snail", "Snail", "Snail"])))

    match game_state:
        case "main_menu":
            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))
            screen.blit(made_by_surface, (20, 350))

            screen.blit(title_surface, (width//2 - 3.15*title_ratio//2, 30))
            
            play_btn.draw(screen)
            play_btn.update(game_state)

            # All code when mouse is pressed when on main menu
            if pygame.mouse.get_pressed()[0] and play_btn.sprites()[0].rect.collidepoint(pygame.mouse.get_pos()):
                btn_sound.play()
                start_time = pygame.time.get_ticks()
                game_state = "in_game"

        case "in_game":
            if not bg_voice.get_busy():
                bg_music.play(loops=-1)
            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))
            screen.blit(made_by_surface, (20, 350))

            score = display_score()

            player.draw(screen)
            player.update()

            obstacle_group.draw(screen)
            obstacle_group.update()

            if not collisionSprite():
                game_state = "game_over"
                pygame.mixer.stop()
                game_over.play()
        case "game_over":
            if keys[pygame.K_RETURN]:
                start_time = pygame.time.get_ticks()
                game_state = "in_game"
            fade.update()
            fade.draw(screen)
            screen.blit(player_stand_roto, player_stand_rectangle)

            final_score_surface = test_font.render(
                f"Score: {score}", False, 'White')
            final_score_rect = final_score_surface.get_rect(
                center=(width // 2, 340))
            if score == 0:
                screen.blit(instructions_surface, instructions_rect)
            else:
                screen.blit(final_score_surface, final_score_rect)
        case _:
            raise Exception(f"Invalid GameState: {game_state}")

    pygame.display.update()
    clock.tick(60)
