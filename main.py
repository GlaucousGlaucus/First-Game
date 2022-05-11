import py
import pygame
from sys import exit

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('RPG Survival | Dungeon Run') # Gives a title to the window

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # Draw all our elements and update everything
    pygame.display.update() # This updates the display created above