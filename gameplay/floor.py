from gameplay.map import getBoard
import random

class Floor:
    def __init__(self, bSize, numEmptySquares):
        self.boardSize = bSize
        self.distanceSeparator = self.boardSize // 4
        self.board = getBoard(self.boardSize, numEmptySquares)
        self.ladderLoc = self.genLadderLoc()
        self.startingLocs = []
        self.genStartingLocs()

    def __str__(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] == None:
                    print(' ', end='')
                elif (i,j) == self.ladderLoc:
                    print('L', end='')
                else:
                    try:
                        print(self.startingLocs.index((i,j)), end='')
                    except ValueError:
                        print('X', end='')
            print('')
        return str(self.startingLocs) + str(self.ladderLoc)

    def genLadderLoc(self):
        ladderLoc = None
        while(ladderLoc is None):
            xLoc = random.randrange(0, self.boardSize)
            yLoc = random.randrange(0, self.boardSize)
            if self.board[xLoc][yLoc] is not None:
                ladderLoc = (xLoc, yLoc)
        return ladderLoc

    def genStartingLocs(self):
        while (len(self.startingLocs) < 4):
            xLoc = random.randrange(0, self.boardSize)
            yLoc = random.randrange(0, self.boardSize)
            if self.validatePos(xLoc, yLoc):
                self.startingLocs.append((xLoc, yLoc))

    def validatePos(self, x, y):
        works = True
        if self.board[x][y] is None:
            works = False
        if not self.checkDist(x, y, self.ladderLoc[0], self.ladderLoc[1]):
            works = False
        for i in range(len(self.startingLocs)):
            if not self.checkDist(x, y, self.startingLocs[i][0], self.startingLocs[i][1]):
                works = False
        return works


    def checkDist(self, x1, y1, x2, y2):
        works = True
        xDist = min(abs(x2 - x1), self.boardSize - abs(x2 - x1))
        yDist = min(abs(y2 - y1), self.boardSize - abs(y2 - y1))
        if xDist + yDist <= self.distanceSeparator:
            works = False
        return works
