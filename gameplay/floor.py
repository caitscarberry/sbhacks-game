from gameplay.map import getBoard
from gameplay.entity import Ladder
import random
from gameplay.events import GameEvent
from gameplay.room import Room
import json

class Floor:
    def __init__(self):
        self.boardSize = 0
        self.distanceSeparator = 0
        self.board = [[None] * self.boardSize for _ in range(self.boardSize)]
        self.ladderLoc = (0,0)
        self.startingLocs = []

    def genFloor(self, bSize, numEmptySquares):
        self.boardSize = bSize
        self.distanceSeparator = self.boardSize // 4
        self.board = getBoard(self.boardSize, numEmptySquares)
        self.ladderLoc = self.genLadderLoc()
        # adds ladder entity to collidable list
        # self.board[self.ladderLoc[0]][self.ladderLoc[1]].collidable.append(1)
        self.genStartingLocs()

    def to_dict(self):
        brd = [[None]*self.boardSize for _ in range(self.boardSize)]
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] is None:
                    brd[i][j] = None
                else:
                    brd[i][j] = self.board[i][j].to_dict()

        dict = {"board": brd,
                "board_size": self.boardSize,
                "startingLocs": self.startingLocs}
        return dict

    # NOTE: NOT STATIC METHOD
    def from_dict(self, dict):
        self.boardSize = dict["board_size"]
        self.startingLocs = dict["startingLocs"]
        self.board = [[None] * self.boardSize for _ in range(self.boardSize)]
        for x in range(dict["board_size"]):
            for y in range(dict["board_size"]):
                if dict["board"][x][y] is None:
                    self.board[x][y] = None
                else:
                    self.board[x][y] = Room()
                    self.board[x][y].from_dict(dict["board"][x][y])

    def serialize(self):
        return json.dumps(self.to_dict())

    def get_update_event(self, room_x, room_y):
        game_event_dict = {
            "type": "STATUS",
            "kind": "ROOM",
            "room_x": room_x,
            "room_y": room_y,
            "room": self.board[room_x][room_y].to_dict()
        }
        return GameEvent(game_event_dict)

    def handle_update_event(self, event):
        self.board[event["room_x"]][event["room_y"]].from_dict(event["room"])

    def __str__(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] == None:
                    print(' ', end='')
                elif self.board[i][j].collidable != []:
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
