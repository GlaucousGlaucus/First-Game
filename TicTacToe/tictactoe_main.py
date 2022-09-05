import pygame

def drawBoard():
    for x in range(2):
        fac = x * 135
        heght = height//3 + fac + 15
        pygame.draw.line(screen, pygame.Color("white"), (width//8, heght), ((7*width)//8, heght))
    for x in range(2):
        fac = x * 135
        heght = width//3 + fac + 15
        pygame.draw.line(screen, pygame.Color("white"), (heght, width//8), (heght, (7*width)//8))

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
    #TODO make x and o, game functions
    pygame.draw.circle(screen, pygame.Color("White"))
    pygame.display.update()
    clock.tick(60)