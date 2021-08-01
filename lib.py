import pygame
from os import listdir
from random import randint

import var

pygame.init()


def getUserLevel():
    while True:
        try:
            userSelection = int(input(
                "\n"*100+"Please select difficulty:\n1. Beginner\n2. Intermediate\n3. Expert\n4. Exit\n---> "))
            if userSelection == 4:
                var.running = False
            else:
                if userSelection == 1:
                    var.ROW, var.COL = 8, 8
                    var.MINES = 10
                elif userSelection == 2:
                    var.ROW, var.COL = 16, 16
                    var.MINES = 40
                elif userSelection == 3:
                    var.ROW, var.COL = 16, 30
                    var.MINES = 99
                else:
                    pass
            print("\n"*100)
            print(
                f"LAYOUT = {var.ROW}x{var.COL}\nNumber of mines: {var.MINES}")
            var.gameData = [[' ' for _ in range(var.COL)]
                            for _ in range(var.ROW)]
            var.userData = [['d' for _ in range(var.COL)]
                            for _ in range(var.ROW)]
            break
        except ValueError:
            print("Wrong input, try again!!!\n\n")


def loadImgs():
    files = listdir(var.PATH)
    for f in files:
        tmpImg = pygame.image.load(f"{var.PATH}{f}")
        tmpImg = pygame.transform.scale(tmpImg, (var.CELL_SIZE, var.CELL_SIZE))
        var.gameImgs[f[0]] = tmpImg


def displayInit(game):
    for x in range(var.COL):
        for y in range(var.ROW):
            game.blit(var.gameImgs[var.userData[y][x]],
                      (x*var.CELL_SIZE, y*var.CELL_SIZE))
    pygame.display.update()


def gameInit():
    setMines()
    for y in range(var.ROW):
        for x in range(var.COL):
            setCellVal((y, x))


def setMines():
    # seed(1)
    for i in range(var.MINES):
        pos = (randint(0, var.ROW-1), randint(0, var.COL-1))
        while(pos in var.minePos):
            pos = (randint(0, var.ROW-1), randint(0, var.COL-1))
        var.minePos.append(pos)

    for mine in var.minePos:
        y, x = mine
        var.gameData[y][x] = 'b'


def setCellVal(pos):
    if pos not in var.minePos:
        numberOfBombs = 0
        y, x = pos

        for tmp_y in range(y-1, y+2):
            for tmp_x in range(x-1, x+2):
                if tmp_y in range(var.ROW) and tmp_x in range(var.COL) and (tmp_y, tmp_x) in var.minePos:
                    numberOfBombs += 1

        var.gameData[y][x] = str(numberOfBombs)


def getClickedPos(pos):
    x, y = pos
    return (y//var.CELL_SIZE, x//var.CELL_SIZE)


def updateUserDisplay(game, pos, updateAll=False):
    if updateAll is True:
        for y in range(var.ROW):
            for x in range(var.COL):
                game.blit(var.gameImgs[var.userData[y][x]],
                          (x*var.CELL_SIZE, y*var.CELL_SIZE))
    else:
        y, x = pos
        game.blit(var.gameImgs[var.userData[y][x]],
                  (x*var.CELL_SIZE, y*var.CELL_SIZE))
    pygame.display.update()


def revealCell(game, pos, checkedCells, isDone=True):
    y, x = pos
    zeroCells = []
    var.userData[y][x] = var.gameData[y][x]

    if (y, x) not in checkedCells:
        checkedCells.append((y, x))
    if var.gameData[y][x] == '0':
        for tmp_y in range(y-1, y+2):
            for tmp_x in range(x-1, x+2):
                if tmp_y in range(var.ROW) and tmp_x in range(var.COL) and (tmp_y, tmp_x) not in checkedCells and (tmp_y, tmp_x) != (y, x):
                    var.userData[tmp_y][tmp_x] = var.gameData[tmp_y][tmp_x]
                    if var.gameData[tmp_y][tmp_x] == '0':
                        zeroCells.append((tmp_y, tmp_x))
                        isDone = False
                    checkedCells.append((tmp_y, tmp_x))
    else:
        isDone = True

    if isDone is False:
        for cell in zeroCells:
            revealCell(game, cell, checkedCells, isDone=isDone)

    updateUserDisplay(game, pos, updateAll=True)


def checkGameResult():
    retVal = True
    for i in range(var.ROW):
        userResult = ''.join(var.userData[i]).replace(
            'f', 'b').replace('d', 'b')
        gameResult = ''.join(var.gameData[i])
        if userResult != gameResult:
            retVal = False
            break
    return retVal
