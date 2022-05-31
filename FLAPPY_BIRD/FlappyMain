from random import randint
from sys import exit

import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        bird_dwn_flap = pygame.image.load(r'FLAPPY_BIRD\resources\sprites\yellowbird-downflap.png').convert_alpha()
        bird_mid_flap = pygame.image.load(r'FLAPPY_BIRD\resources\sprites\yellowbird-midflap.png').convert_alpha()
        bird_up_flap = pygame.image.load(r'FLAPPY_BIRD\resources\sprites\yellowbird-upflap.png').convert_alpha()
        self.player_flap = [bird_dwn_flap, bird_mid_flap, bird_up_flap]
        self.player_index = 0
        self.image = self.player_flap[self.player_index]
        self.rect = self.image.get_rect(midbottom=(100,200))
        self.gravity = 0
        self.init_gravity = False
        self.rot = 0
        self.amt = 0

    def set_init_gravity(self, val):
        self.init_gravity = val

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            if self.init_gravity is False: self.init_gravity = True
            self.gravity = -4

    def apply_gravity(self):
        self.gravity += 0.35 if self.init_gravity else 0
        self.rect.y += self.gravity

    def animation_state(self):
        self.player_index += 0.1
        if self.player_index >= len(self.player_flap):
            self.player_index = 0
        curr_img = self.player_flap[int(self.player_index)]
        clamp = lambda n: max(-35, min(n, 35))
        rot_image = pygame.transform.rotate(curr_img, -clamp(self.gravity*6.45))
        self.image = rot_image

    def update(self):
        self.player_input()
        if self.init_gravity:
            self.apply_gravity()
        self.animation_state()

    def __repr__(self):
        return f""" {self.rect}
        {self.init_gravity}
        {self.gravity}
        """


class Base(pygame.sprite.Sprite):
    def __init__(self, tup):
        super().__init__()

        base = pygame.image.load(r'FLAPPY_BIRD\resources\sprites\base.png').convert()
        self.image = base
        self.rect = self.image.get_rect(topleft=tup)
        self.x, self.y = tup
    
    def update(self):
        self.rect.x -= 2
        if self.rect.x <= self.x - 336: 
            self.rect.x = self.x
        

class Pillar(pygame.sprite.Sprite):
    def __init__(self, pos, inverted):
        super().__init__()
        pillar_up = pygame.image.load(r"FLAPPY_BIRD\resources\sprites\pipe-green.png").convert_alpha()
        pillar_down = pygame.transform.flip(pillar_up, False, True)
        self.image = pillar_down if inverted else pillar_up
        if inverted:
            self.rect = self.image.get_rect(midbottom=pos)
        else:
            self.rect = self.image.get_rect(midtop=pos)

    def update(self):
        self.rect.x -= 2
        if self.rect.x <= -52:
            self.kill()


def collisionSprite():
    return pygame.sprite.spritecollide(player.sprite, obstacle_group, False)

pygame.init()
width, height = 288, 512
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')  # Gives a title to the window
clock = pygame.time.Clock()  # This will give a clock object
game_state = "main_menu"
prev_game_state = None
score = 0

mouse_event_buttons_index = {
            "LMB": 1, "MMB": 2, "RMB": 3, "Scroll_UP": 4, "Scroll_DOWN": 5}

# Fonts
score_font = pygame.font.Font('Resources\Fonts\Pixeltype.ttf', 50)
title_font = pygame.font.Font('Resources\Fonts\Fipps-Regular.otf', 50)
general_font = pygame.font.Font('Resources\Fonts\Pixeltype.ttf', 50)

# Surfaces
bg_day = pygame.image.load(r'FLAPPY_BIRD\resources\sprites\background-day.png').convert_alpha()
bg_night = pygame.image.load(r'FLAPPY_BIRD\resources\sprites\background-day.png').convert()
msg = pygame.image.load(r'FLAPPY_BIRD\resources\sprites\message.png').convert_alpha()
game_over = pygame.image.load(r'FLAPPY_BIRD\resources\sprites\gameover.png').convert_alpha()

score_nums = {
    1: pygame.image.load(r'FLAPPY_BIRD\resources\sprites\1.png').convert_alpha(),
    2: pygame.image.load(r'FLAPPY_BIRD\resources\sprites\2.png').convert_alpha(),
    3: pygame.image.load(r'FLAPPY_BIRD\resources\sprites\3.png').convert_alpha(),
    4: pygame.image.load(r'FLAPPY_BIRD\resources\sprites\4.png').convert_alpha(),
    5: pygame.image.load(r'FLAPPY_BIRD\resources\sprites\5.png').convert_alpha(),
    6: pygame.image.load(r'FLAPPY_BIRD\resources\sprites\6.png').convert_alpha(),
    7: pygame.image.load(r'FLAPPY_BIRD\resources\sprites\7.png').convert_alpha(),
    8: pygame.image.load(r'FLAPPY_BIRD\resources\sprites\8.png').convert_alpha(),
    9: pygame.image.load(r'FLAPPY_BIRD\resources\sprites\9.png').convert_alpha(),
    0: pygame.image.load(r'FLAPPY_BIRD\resources\sprites\0.png').convert_alpha()
}

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

bg_group = pygame.sprite.Group()
bg_group.add(Base((0, 400)))
bg_group.add(Base((336, 400)))

obstacle_group = pygame.sprite.Group()

# Timer(s)

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

obstacle_sprites = []

# Main Loop
while True:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # We quit the game
            pygame.quit()
            exit()

        # Events
        match game_state:
            case "main_menu":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == mouse_event_buttons_index["LMB"]:
                    start_time = pygame.time.get_ticks()
                    prev_game_state = game_state
                    game_state = "in_game"
            case "in_game":
                pass
                if event.type == obstacle_timer and player.sprite.init_gravity:
                    # Decide the y of the lower pillar
                    # Decide the sepration b/w the two pillars
                    # Give data to upper pillar to generate
                    y_coord = randint(100, 175) + 100
                    x_coord = randint(10, 60)
                    sep = randint(150, 200)
                    obstacle_group.add(Pillar((width+52 + x_coord, y_coord), False))
                    obstacle_group.add(Pillar((width+52 + x_coord, y_coord - sep), True))
                    obstacle_sprites = [x for x in obstacle_group]
            case "game_over":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == mouse_event_buttons_index["LMB"]:
                    start_time = pygame.time.get_ticks()
                    prev_game_state = game_state
                    game_state = "in_game"
            case _:
                raise Exception(f"Invalid GameState: {game_state}")


    # Screen Drawings and Stuff
    match game_state:
        case "main_menu":
            screen.blit(bg_day, (0, 0))
            # S -> 288 512
            # Surf 184 267
            #      104 245
            screen.blit(msg, (104//2, 245//2))
        case "in_game":
            screen.blit(bg_day, (0, 0))
            obstacle_group.draw(screen)
            obstacle_group.update()
            bg_group.draw(screen)
            bg_group.update()
            player.draw(screen)
            player.update()

            player_mid = (player.sprite.rect.x+34) // 2
            for pillar in obstacle_sprites:
                pillar_mid = (pillar.rect.x+52) // 2
                if pillar_mid <= player_mid < pillar_mid + 1:
                    score += 1
                    obstacle_sprites.remove(pillar)
            
            length = len(str(score))
            number_centre = width//2 - 24 * length//2
            for i, num in enumerate(str(score)):
                screen.blit(score_nums[int(num)], (number_centre + 25*i, 30))

            if player.sprite.rect.bottom >= 400 or collisionSprite():
                player.sprite.rect.bottom = 200
                player.sprite.set_init_gravity(False)
                player.sprite.rot = 0
                obstacle_group.empty()
                prev_game_state = game_state
                game_state = "game_over"
                score = 0
        case "game_over":
                screen.blit(game_over, ((width-192) // 2, 100))
        case _:
            raise Exception(f"Invalid GameState: {game_state}")

    pygame.display.update()
    clock.tick(60)
