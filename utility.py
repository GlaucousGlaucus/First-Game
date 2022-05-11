from glob import glob


def to_and_fro_movement(Rect, Direction, min_x = 0, max_x = 800, speed=1):
    # To and Fro Motion
    Rect.left += -speed if Direction else speed
    return not Direction if Rect.left == min_x or Rect.left >= max_x else Direction 

def cont_movement(Rect, min_x=-72, max_x = 872, speed=1):
    # Continous Motion
    Rect.left -= speed
    if Rect.left < min_x: Rect.left = max_x