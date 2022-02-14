import random
import os
import json
import datetime as datetime
from saveHelper import readFile, writeFile

fileExists = os.path.exists("gamelog.json")

EMPTY = 'E'
TREASURE = 'T'
MONSTER = 'M'
VENOM = 'V'
SWORD = 'S'
POTION = 'P'

whatToAddInGrid = (
    TREASURE, TREASURE, TREASURE, TREASURE, TREASURE, MONSTER, MONSTER, MONSTER, MONSTER, MONSTER, SWORD, SWORD,
    POTION, POTION, POTION, VENOM, VENOM, VENOM)

startTime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
currentScore = 0
swordCount = 0
potionCount = 0
gameEnded = False

NROWS_IN_GRID = 6
NCOLS_IN_GRID = 7

moveList = []
gridForGame = []
gridToPrint = []
visitedCells = []

for r in range(0, NROWS_IN_GRID):  # 0-5
    aRow = []
    bRow = []
    for c in range(0, NCOLS_IN_GRID):  # 0-7
        aRow.append(EMPTY)
        bRow.append(' ')
    gridForGame.append(aRow)
    gridToPrint.append(bRow)


def findEmptyCell(aGrid, nRows, nCols):
    # Find a random starting cell that is empty.
    while True:
        row = random.randrange(nRows)
        col = random.randrange(nCols)
        if (aGrid[row][col] == EMPTY):
            return row, col


for item in whatToAddInGrid:
    rowRandom, colRandom = findEmptyCell(gridForGame, NROWS_IN_GRID, NCOLS_IN_GRID)
    gridForGame[rowRandom][colRandom] = item

startRow, startCol = findEmptyCell(gridForGame, NROWS_IN_GRID, NCOLS_IN_GRID)
gridForGame[startRow][startCol] = 'E'
visitedCells.append((startRow, startCol))


def printGrid(grid):
    for i in range(0, len(grid)):
        row = grid[i]
        for j in range(0, len(row)):
            if (i, j) in visitedCells:
                gridToPrint[i][j] = grid[i][j]
            else:
                gridToPrint[i][j] = ' '
        print(gridToPrint[i])


def printTable(a, b, c):
    print()
    print("Score: " + "[" + str(a) + "]" + " " + "Sword: " + "[" + str(b) + "]" + " " + "Potion: " + "[" + str(c) + "]")


printGrid(gridForGame)
printTable(currentScore, swordCount, potionCount)

print('Starting at row:', startRow, 'col:', startCol)
print('You are here -> E')
gridForGame[startRow][startCol] = EMPTY

while True:
    # move the user around
    gridForGame[startRow][startCol] = EMPTY
    direction = input('Press L, U, R, D to move: ').lower()
    print()

    if (direction == 'l'):
        os.system('clear')
        moveList.append('l')
        if (startCol == 0):
            startCol = NCOLS_IN_GRID - 1

        else:
            startCol -= 1

    elif (direction == 'r'):
        os.system('clear')
        moveList.append('r')
        if (startCol == NCOLS_IN_GRID - 1):
            startCol = 0

        else:
            startCol += 1

    elif (direction == 'u'):
        os.system('clear')
        moveList.append('u')
        if (startRow == 0):
            startRow = NROWS_IN_GRID - 1

        else:
            startRow -= 1

    elif (direction == 'd'):
        os.system('clear')
        moveList.append('d')
        if (startRow == NROWS_IN_GRID - 1):
            startRow = 0

        else:
            startRow += 1

    else:
        print('Invalid move. Quitting the game.')
        gameEnded = True

    if (gridForGame[startRow][startCol] == EMPTY):
        visitedCells.append((startRow, startCol))
        currentScore += 1


    elif (gridForGame[startRow][startCol] == TREASURE):
        visitedCells.append((startRow, startCol))
        currentScore += 2

        print('💎 You found a Treasure! 💎')
        print()



    elif (gridForGame[startRow][startCol] == SWORD):
        visitedCells.append((startRow, startCol))
        currentScore += 1
        swordCount += 1
        print('❗ You have a Sword ' + "🗡️" + " " + "and Monsters do not like swords. ❗")
        print()


    elif (gridForGame[startRow][startCol] == MONSTER):
        visitedCells.append((startRow, startCol))
        if (swordCount <= 0):
            print('❗ YOU LOST fighting a MONSTER ❗')
            print()
            gameEnded = True

        else:
            print()
            swordCount -= 1
            currentScore += 1
            print('❗ You killed a Monster. | 1 Sword is broken. ❗')
            print()

    elif (gridForGame[startRow][startCol] == POTION):
        visitedCells.append((startRow, startCol))
        potionCount += 1
        print('❗ You have a Potion ' + "🧪" + ' now and Venoms do not like potions. ❗')
        print()

    elif (gridForGame[startRow][startCol] == VENOM):
        visitedCells.append((startRow, startCol))

        if (potionCount <= 0):
            print('❗ YOU LOST by crashing a VENOM ❗')
            print()
            gameEnded = True

        else:
            potionCount -= 1
            gridForGame[startRow][startCol] = EMPTY
            currentScore += 1
            print()
            print('❗ You poisoned a Venom 🐙 | 1 Potion Bottle is broken. ❗')

    if gameEnded == True:
        break

    printGrid(gridForGame)
    printTable(currentScore, swordCount, potionCount)
    print()

print('Your score is: ', currentScore)
print()

saveDict = {
    "moves": moveList,
    "score": currentScore
}

resultsDict = {
    startTime: saveDict
}

if not fileExists:
    with open("gamelog.json", "w") as f:
        s = json.dumps(resultsDict, indent=1, sort_keys=True)
        f.write(s)
        f.close()

else:
    fR = readFile("gamelog.json")
    veri = json.loads(fR)
    veri[startTime] = saveDict
    st = json.dumps(veri, indent=1, sort_keys=True)
    writeFile("gamelog.json", st)
