import pygame
import math

def slot_to_coords(n):
    fac = math.ceil(n/3)
    x = width//8 + 130 * math.ceil((n-fac)/3)
    y = height//3 - 45 + (130) * (fac-1)
    return (x, y)

def drawX(col, row):
    # TODO: Instead of taking in x and y take in the slot no.
    f = 80
    x, y = f + 130*(col-1), f + 130*(row-1)
    pygame.draw.line(screen, pygame.Color("White"), (x, y), (x+f, y+f), width=5)
    pygame.draw.line(screen, pygame.Color("White"), (x + f, y), (x, y+f), width=5)

def drawO(col, row):
    pygame.draw.circle(screen, pygame.Color("White"), (60 + 60 + 130*(col-1), 130*row - 10), 100//2, width=5)

def drawBoard():
    # Vertical Lines
    for x in range(2):
        fac = x * 135
        heght = width//3 + fac + 15
        pygame.draw.line(screen, pygame.Color("white"), (heght, width//8), (heght, (7*width)//8))
    # Horizontal Lines
    for x in range(2):
        fac = x * 135
        heght = height//3 + fac + 15
        pygame.draw.line(screen, pygame.Color("white"), (width//8, heght), ((7*width)//8, heght))

pygame.init()
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()

# GUI elements
screen.fill((68, 169, 227))

# Drawing the board
length = 200

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    drawBoard()
    pygame.display.update()
    clock.tick(60)