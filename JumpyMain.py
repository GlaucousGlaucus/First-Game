import imp
from re import S
from sys import exit

import pygame

import random as rand
from utility import cont_movement

# Color Pallete: https://colorhunt.co/palette/f9ebc8fefbe7dae5d0a0bcc2


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
        self.jump_sound.set_volume(sfx_voice.get_volume())

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            sfx_voice.play(self.jump_sound)

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


class ButtonSprite(pygame.sprite.Sprite):

    def __init__(self, btn_idle, btn_hover, btn_pressed, coords, amount=70, scale_fac_x=2, scale_fac_y=1):
        super().__init__()

        scale_fac = scale_fac_x * amount, scale_fac_y * amount
        self.btn_idle = pygame.transform.smoothscale(
            btn_idle, scale_fac)
        self.btn_hover = pygame.transform.smoothscale(
            btn_hover, scale_fac)
        self.btn_pressed = pygame.transform.smoothscale(
            btn_pressed, scale_fac)

        self.image = self.btn_idle
        self.rect = self.image.get_rect(center=coords)

    def animation_state(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.btn_pressed if pygame.mouse.get_pressed()[
                0] else self.btn_hover
        else:
            self.image = self.btn_idle

    def update(self):
        self.animation_state()


class Slider:

    def __init__(self, pos: tuple, font, text: str = "Slider", outlineSize: tuple = (300, 10), color: tuple = (0, 0, 0)):
        self.pos = pos
        self.outlineSize = outlineSize
        self.text = text
        self.radius = 10
        self.sliderPos = pos[0] + self.outlineSize[0]
        self.font = font
        self.color = color
        self.focused = False

    def getValue(self) -> float:
        return (self.sliderPos - self.pos[0]) / (self.outlineSize[0])

    def render(self, display_surface: pygame.display):
        # draw outline and slider rectangles
        pygame.draw.rect(display_surface, self.color, (self.pos[0], self.pos[1],
                                                       self.outlineSize[0], self.outlineSize[1]), 3)
        # The Slider
        pygame.draw.circle(display_surface, self.color, (self.sliderPos,
                           self.pos[1] + (self.outlineSize[1]//2)), self.radius)

        value_surface = self.font.render(
            f"{self.text}: {round(self.getValue() * 100)}", True, self.color)
        textx = self.pos[0] - (self.outlineSize[0]/2) - 50
        texty = self.pos[1] + (self.outlineSize[1]/2) - \
            (value_surface.get_rect().height/2)

        display_surface.blit(value_surface, (textx, texty))

    def mouse_up(self):
        self.focused = False

    def update(self, mouse_point):
        if pointInCircle(mouse_point, self.sliderPos, self.pos[1] + (self.outlineSize[1]//2), self.radius) or self.focused:
            self.focused = True
            x_pos = mouse_point[0]
            if x_pos < self.pos[0]:
                self.sliderPos = self.pos[0]
            elif x_pos > self.pos[0] + self.outlineSize[0]:
                self.sliderPos = self.pos[0] + self.outlineSize[0]
            else:
                self.sliderPos = x_pos


def pointInCircle(points, circle_x, circle_y, circle_rad):
    point_x, point_y = points
    if point_x > circle_x - circle_rad and point_x < circle_x + circle_rad:
        if point_y > circle_y - circle_rad and point_y < circle_y + circle_rad:
            return True
    return False


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
prev_game_state = None
start_time = 0
score = 0

# Fonts
test_font = pygame.font.Font('Resources\Fonts\Pixeltype.ttf', 50)
score_font = pygame.font.Font('Resources\Fonts\Pixeltype.ttf', 50)
title_font = pygame.font.Font('Resources\Fonts\Fipps-Regular.otf', 50)
general_font = pygame.font.Font('Resources\Fonts\Pixeltype.ttf', 50)

# Sounds
pygame.mixer.init()
pygame.mixer.set_num_channels(8)
bg_voice = pygame.mixer.Channel(1)
sfx_voice = pygame.mixer.Channel(2)
bg_music = pygame.mixer.music.load('Resources\Audio\music.wav')

btn_sound = pygame.mixer.Sound(r'Resources\Audio\btn_click.wav')
game_over = pygame.mixer.Sound('Resources\Audio\game_over.wav')

btn_sound.set_volume(sfx_voice.get_volume())
game_over.set_volume(sfx_voice.get_volume())

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Surfaces
sky_surface = pygame.image.load('Resources\Images\Sky.png').convert()
ground_surface = pygame.image.load('Resources\Images\ground.png').convert()
made_by_surface = test_font.render('Made By using: Pygame', False, 'White')

# Main Menu
title_surface = pygame.image.load(
    'Resources\Images\Logo4.png').convert_alpha()  # 996 x 316
title_ratio = 150
title_scale_fac = (3.15 * title_ratio, 1 * title_ratio)
title_surface = pygame.transform.smoothscale(title_surface, title_scale_fac)

# Play Button
play_btn_idle = pygame.image.load(
    'Resources\Images\GUI\play_btn\Play_btn_1.png').convert_alpha()
play_btn_hover = pygame.image.load(
    'Resources\Images\GUI\play_btn\Play_btn_2.png').convert_alpha()
play_btn_pressed = pygame.image.load(
    'Resources\Images\GUI\play_btn\Play_btn_3.png').convert_alpha()
play_btn_sprite = ButtonSprite(
    play_btn_idle, play_btn_hover, play_btn_pressed, (width//2 - 100, 250))


# Options Button
options_btn_idle = pygame.image.load(
    'Resources\Images\GUI\options_btn\options_btn_1.png').convert_alpha()
options_btn_hover = pygame.image.load(
    'Resources\Images\GUI\options_btn\options_btn_2.png').convert_alpha()
options_btn_pressed = pygame.image.load(
    'Resources\Images\GUI\options_btn\options_btn_3.png').convert_alpha()
options_btn_sprite = ButtonSprite(
    options_btn_idle, options_btn_hover, options_btn_pressed, (width//2 + 40, 250))

# Quit Button

quit_btn_idle = pygame.image.load(
    'Resources\Images\GUI\quit_btn\quit_btn_1.png').convert_alpha()
quit_btn_hover = pygame.image.load(
    'Resources\Images\GUI\quit_btn\quit_btn_2.png').convert_alpha()
quit_btn_pressed = pygame.image.load(
    'Resources\Images\GUI\quit_btn\quit_btn_3.png').convert_alpha()
quit_btn_sprite = ButtonSprite(
    quit_btn_idle, quit_btn_hover, quit_btn_pressed, (width//2 + 180, 250))

buttons = pygame.sprite.Group(play_btn_sprite, options_btn_sprite, quit_btn_sprite)

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

# Options Menu
options_title_surface = general_font.render('Options', False, 'Black')
intermediate = pygame.surface.Surface((width - 100, 600))
scroll_y = 0
intermediate_pos = 50, scroll_y

pygame.draw.rect(intermediate, '#F9EBC8', (500, 250, 10, 10))
music_slider = Slider((230 + intermediate_pos[0], 100 + intermediate_pos[1]), test_font,
                      text="Music", color=(160, 188, 194))
sfx_slider = Slider((230 + intermediate_pos[0], 150 + intermediate_pos[1]),
                    test_font, text="SFX", color=(160, 188, 194))
sliders = [music_slider, sfx_slider]

done_btn = ButtonSprite(play_btn_idle, play_btn_hover, play_btn_pressed, (intermediate.get_width()//2-80, 25))
options_menu_ui = pygame.sprite.Group(done_btn)

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
    # Set Volumes for all sounds
    pygame.mixer.music.set_volume(music_slider.getValue())
    sfx_voice.set_volume(sfx_slider.getValue())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # All code when mouse is pressed when on options menu
        if game_state == "options" and event.type == pygame.MOUSEBUTTONUP:
            for sprite in options_menu_ui.sprites():
                if sprite.rect.collidepoint(event.pos):
                    sfx_voice.play(btn_sound)
                    if sprite is done_btn:
                        game_state = prev_game_state

        if game_state == "options" and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: # Scroll UP
                    scroll_y = min(scroll_y + 15, 0)
                if event.button == 5: # Scroll DOWN
                    scroll_y = max(scroll_y - 15, -(intermediate.get_height() - height))
                intermediate_pos = intermediate_pos[0], scroll_y

        if game_state == "options" and event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                x, y = event.pos
                for slider in sliders:
                    if not any([x.focused for x in sliders if x != slider]):
                        slider.update((x - intermediate_pos[0], y - intermediate_pos[1]))
            else:
                for slider in sliders:
                    slider.mouse_up()

        # All code when mouse is pressed when on main menu
        if game_state == "main_menu" and event.type == pygame.MOUSEBUTTONUP:
            for sprite in buttons.sprites():
                if sprite.rect.collidepoint(event.pos):
                    sfx_voice.play(btn_sound)
                    if sprite is play_btn_sprite:
                        start_time = pygame.time.get_ticks()
                        prev_game_state = game_state
                        game_state = "in_game"
                    elif sprite is options_btn_sprite:
                        prev_game_state = game_state
                        game_state = "options"
                    elif sprite is quit_btn_sprite:
                        pygame.quit()
                        exit()


        if game_state == "in_game" and event.type == obstacle_timer:
            obstacle_group.add(Obstacles(rand.choice(
                ["Fly", "Snail", "Snail", "Snail"])))

    match game_state:
        case "main_menu":
            pygame.mixer.music.set_volume(music_slider.getValue())
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(loops=-1)
            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))
            screen.blit(made_by_surface, (20, 350))

            screen.blit(title_surface, (width//2 - 3.15*title_ratio//2, 30))

            buttons.draw(screen)
            buttons.update()

        case "options":
            screen.fill("White")
            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))
            screen.blit(made_by_surface, (20, 350))

            intermediate.fill('#F9EBC8')
            intermediate.blit(options_title_surface, (intermediate.get_width()//2-80, 25))
            for slider in sliders:
                slider.render(intermediate)
            options_menu_ui.draw(intermediate)
            options_menu_ui.update()
            screen.blit(intermediate, intermediate_pos)

            if keys[pygame.K_BACKSPACE]:
                game_state = prev_game_state

        case "in_game":
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(loops=-1)
            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))
            screen.blit(made_by_surface, (20, 350))

            score = display_score()

            player.draw(screen)
            player.update()

            obstacle_group.draw(screen)
            obstacle_group.update()

            if not collisionSprite():
                prev_game_state = game_state
                game_state = "game_over"
                pygame.mixer.stop()
                pygame.mixer.music.stop()
                sfx_voice.play(game_over)
        case "game_over":
            if keys[pygame.K_RETURN]:
                start_time = pygame.time.get_ticks()
                prev_game_state = game_state
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
