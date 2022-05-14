import configparser

config = configparser.RawConfigParser()
# Save our config here
config.add_section('Music & Sounds')
config['Music & Sounds']['music'] = '1'
config['Music & Sounds']['sfx'] = '1'
config.add_section('Game')
config['Game']['High Score'] = '0'
with open('jumpy_config.cfg', 'w') as configfile:
    config.write(configfile)

def MouseMotionCoords(pygame, event):
    if event.type == pygame.MOUSEMOTION:
            return event.pos


def to_and_fro_movement(Rect, Direction, min_x = 0, max_x = 800, speed=1):
    # To and Fro Motion
    Rect.left += -speed if Direction else speed
    return not Direction if Rect.left == min_x or Rect.left >= max_x else Direction 

def cont_movement(Rect, min_x=-72, max_x = 1200, speed=1, inverse=False):
    # Continous Motion
    if inverse:
        Rect.left += speed
        if Rect.left > max_x: Rect.left = min_x
    else:
        Rect.left -= speed
        if Rect.left < min_x: Rect.left = max_x