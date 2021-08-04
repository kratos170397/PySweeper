import sys
import pygame
import var
import lib
import tkinter as tk

from tkinter import simpledialog, messagebox

root = tk.Tk()
root.withdraw()

var.running = True

lib.getUserLevel(simpledialog.askinteger("Input", "Please select difficulty:\n1. Beginner\n2. Intermediate\n3. Expert\n4. Exit"))
game = pygame.display.set_mode((var.COL*var.CELL_SIZE, var.ROW*var.CELL_SIZE))
lib.loadImgs()
lib.displayInit(game)
lib.gameInit()

pygame.display.update()

while var.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            var.running = False
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if True in pygame.mouse.get_pressed():
                mouseClicked = pygame.mouse.get_pressed().index(True)

                cellClickedPos = lib.getClickedPos(pygame.mouse.get_pos())
                y, x = cellClickedPos

                if mouseClicked == 0 and var.userData[y][x] == 'd':
                    var.userData[y][x] = var.gameData[y][x]
                    lib.updateUserDisplay(game, cellClickedPos, [])

                    if var.gameData[y][x] == 'b':
                        var.running = False
                        var.retry = messagebox.askyesno("OOPS!!", "YOU STEPPED ON A MINE!!! Wanna try again?")
                        print('You lose')
                    else:
                        lib.revealCell(game, cellClickedPos, [])
                    if lib.checkGameResult() is True:
                        var.running = False
                        var.retry = messagebox.askyesno("CONGRATS!!", "YOU WON!!! Wanna try again?")
                        print('You won')
                        sys.exit()

                if mouseClicked == 1 and var.userData[y][x] != 'd' and var.userData[y][x] != 'f':
                    numberOfFlags = 0
                    for tmp_y in range(y-1, y+2):
                        for tmp_x in range(x-1, x+2):
                            if tmp_y in range(var.ROW) and tmp_x in range(var.COL):
                                if var.userData[tmp_y][tmp_x] == 'f':
                                    numberOfFlags += 1

                    if numberOfFlags == int(var.userData[y][x]):
                        for tmp_y in range(y-1, y+2):
                            for tmp_x in range(x-1, x+2):
                                if tmp_y in range(var.ROW) and tmp_x in range(var.COL):
                                    if var.userData[tmp_y][tmp_x] == 'd':
                                        lib.revealCell(
                                            game, (tmp_y, tmp_x), [])
                                        if var.gameData[tmp_y][tmp_x] == 'b':
                                            var.running = False
                                            var.retry = messagebox.askyesno("OOPS!!", "YOU STEPPED ON A MINE!!! Wanna try again?")
                                            print('You lose')
                        if lib.checkGameResult() is True:
                            var.running = False
                            var.retry = messagebox.askyesno("CONGRATS!!", "YOU WON!!! Wanna try again?")
                            print('You won')
                            

                if mouseClicked == 2 and (var.userData[y][x] == 'd' or var.userData[y][x] == 'f'):
                    if var.userData[y][x] == 'f':
                        var.userData[y][x] = 'd'
                    elif var.userData[y][x] == 'd':
                        var.userData[y][x] = 'f'
                    else:
                        pass

                    lib.updateUserDisplay(game, cellClickedPos)
    if var.retry is True and var.running is False:
        lib.getUserLevel(simpledialog.askinteger("Input", "Please select difficulty:\n1. Beginner\n2. Intermediate\n3. Expert\n4. Exit"))
        if var.retry is False and var.running is False:
            break
        else:
            game = pygame.display.set_mode((var.COL*var.CELL_SIZE, var.ROW*var.CELL_SIZE))
            lib.loadImgs()
            lib.displayInit(game)
            lib.gameInit()
            var.running = True
    else:
        pass
