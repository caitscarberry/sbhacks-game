from gameplay.room import Room
from queue import Queue
import random

def getBoard(boardSize, numEmptySquares):
    board = [[1]*boardSize for _ in range(boardSize)]
    boardWorks = False
    roomLocs = [[1]*boardSize for _ in range(boardSize)]
    while boardWorks != True:
        roomLocs = genLocBoard(boardSize, numEmptySquares)
        boardWorks = checkConnectedBoard(roomLocs)
    genBoard(board, roomLocs, boardSize)
    return board

# generates a 2D integer array which contains bool values for whether
# there is a room in that location
def genLocBoard(boardSize, numEmptySquares):
    totalSquares = boardSize * boardSize
    if numEmptySquares > totalSquares:
        numEmptySquares = totalSquares

    roomLocs = [[1]*boardSize for _ in range(boardSize)]
    print (roomLocs)
    while numEmptySquares > 0:
        xLoc = random.randrange(0, boardSize)
        yLoc = random.randrange(0, boardSize)
        if roomLocs[xLoc][yLoc] == 1:
            roomLocs[xLoc][yLoc] = 0
            numEmptySquares = numEmptySquares - 1
    return roomLocs

# checks whether a 2d integer array is connected
def checkConnectedBoard (board):
        size = len(board)
        visit = [[0] * size for _ in range(size)]

        start = None
        for i in range(size):
            for j in range(size):
                if board[i][j] != 0:
                    start = (i, j)
                    break
            if start is not None:
                break

        if start is None:
            return False

        check = Queue()
        check.put(start)
        while not check.empty():
            curr = check.get()
            visit[curr[0]][curr[1]] = 1
            to_check = [
                (curr[0] - 1, curr[1]),
                (curr[0] + 1, curr[1]),
                (curr[0], curr[1] - 1),
                (curr[0], curr[1] + 1)
            ]
            for cell in to_check:
                if cell[0] < 0 or cell[0] >= size or cell[1] < 0 or cell[1] >= size:
                    continue
                if visit[cell[0]][cell[1]] == 0 and board[cell[0]][cell[1]] != 0:
                    check.put(cell)

        for i in range(size):
            for j in range(size):
                if visit[i][j] != board[i][j]:
                    return False
        return True

def genBoard (board, roomLocs, boardSize):
    for x in range(boardSize):
        for y in range(boardSize):
            if roomLocs[x][y] == 1:
                board[x][y] = Room()
            else:
                board[x][y] = None
