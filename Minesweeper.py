import pygame
import sys
import random

pygame.init()
myfont = pygame.font.Font(None, 25)
red = (255, 0, 0)
hit_color = (100, 100, 100)
unhit_color = (155, 155, 155)
grid_color = (80, 80, 80)

while True:
    size = input("What size would you like? [10-25] ")
    try:
        int(size) // 1
    except (TypeError, ValueError):
        continue
    else:
        if 9 < int(size) < 26:
            break
size = int(size)
while True:
    difficulty = input("Would you like to play on hard [3], medium [2] or easy [1]? ")
    try:
        int(difficulty) // 1
    except (TypeError, ValueError):
        continue
    else:
        difficulty = int(difficulty)
        if 0 < difficulty < 4:
            break
multiplier = size*difficulty

screen = pygame.display.set_mode((30 * size, 30 * size))
screen.fill(grid_color)
pygame.display.set_caption('Minesweeper')

# grid is a 2D array used to create the grid
# visit is a 2D array used to check if a box has been evaluated by recursion
# bombpos is a 2D array that stores the position of a bomb, 1 for bomb 0 for none
# neigh is a 2D array that stores the number of neighbouring bombs a box has
grid = []
visit = []
bombpos = []
neigh = []
for y in range(size+1):
    visit.append([])
    grid.append([])
    bombpos.append([])
    neigh.append([])
    for p in range(size+1):
        visit[y].append(False)
        grid[y].append([])
        bombpos[y].append(0)
        neigh[y].append(0)
# draws grid
for i in range(size):
    for u in range(size):
        pygame.draw.rect(screen, unhit_color, (1 + i * 30, 1 + u * 30, 28, 28))


def createbombs():
    for i in range(multiplier):
        a = random.randint(0, size-1)
        b = random.randint(0, size-1)
        bombpos[a][b] = 1
    find_neighbours()


def find_neighbours():
    # first nested loop hits every box
    for z in range(size):
        for x in range(size):
            # second nested loop gets the number of neighbours a box has
            for q in range(-1, 2):
                for w in range(-1, 2):
                    if bombpos[z + q][x + w] == 1:
                        neigh[z][x] += 1
    main()


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = pos[1] // 30
                col = pos[0] // 30
                if 0 <= row < (size + 1) and 0 <= col < (size + 1):
                    onclick(col, row)
        pygame.display.update()


def onclick(col, row):
    # grid_row and col are the starting points for the rectangle to print
    # i.e the top left corner of a box excluding the lines between them
    grid_row = row * 30 + 1
    grid_col = col * 30 + 1
    textsurface = myfont.render("{}".format(str(neigh[row][col])), False, (255, 255, 255))
    if neigh[row][col] == 0:
        floodfill(col, row)
    elif bombpos[row][col] == 1:
        pygame.draw.rect(screen, red, (grid_col, grid_row, 28, 28))
        return
    else:
        pygame.draw.rect(screen, hit_color, (grid_col, grid_row, 28, 28))
        screen.blit(textsurface, (col * 30 + 10, row * 30 + 7, 28, 28))


def floodfill(col, row):
    # grid row and col need to be declared again so they will change with recursion
    # kinda redundant, look for better way
    grid_row = row * 30 + 1
    grid_col = col * 30 + 1
    if not (-1 < row < size and -1 < col < size):
        return
    textsurface = myfont.render("{}".format(str(neigh[row][col])), False, (255, 255, 255))
    if neigh[row][col] == 0 and not visit[row][col]:
        pygame.draw.rect(screen, hit_color, (grid_col, grid_row, 28, 28))
        visit[row][col] = True
        floodfill(col - 1, row)
        floodfill(col, row - 1)
        floodfill(col + 1, row)
        floodfill(col, row + 1)
        floodfill(col - 1, row - 1)
        floodfill(col - 1, row + 1)
        floodfill(col + 1, row - 1)
        floodfill(col + 1, row + 1)
    elif bombpos[row][col] == 1:
        return
    elif neigh[row][col] == 0:
        pygame.draw.rect(screen, hit_color, (grid_col, grid_row, 28, 28))
    else:
        pygame.draw.rect(screen, hit_color, (grid_col, grid_row, 28, 28))
        screen.blit(textsurface, (grid_col + 9, grid_row + 6, 28, 28))
        return


createbombs()
