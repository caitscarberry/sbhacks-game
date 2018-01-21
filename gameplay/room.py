import random
from graphics.sprite_to_render import SpriteToRender
import graphics.view
from gameplay.physics import Simulation, PhysObject, Polygon, Vec2
from gameplay.monster import Monster


class Room:
    def __init__(self):
        self.enemyDifficulties = [1, 2, 3, 5, 7]
        self.enemyProbabilities = [7, 6, 8, 5, 4]
        # following probabilities given as a percentage out of 100 (0-99)
        self.probOfEnemies = 75
        self.probOfSameEnemies = 50
        self.minDifficulty = 3
        self.maxDifficulty = 17
        self.maxEnemies = 5
        self.enemies = []
        self.projectiles = []
        self.collidable = []
        self.background = graphics.view.sprite_factory.from_file("./assets/dungeon.png")
        self.background.rect.x
        self.background.rect.y

        self.simulation = Simulation()
        self.make_walls()
        self.generateEnemies()

    def make_walls(self):
        thickness = 64
        width = 1000 - 188
        height = 650
        x, y = width // 2, 32
        rect = Polygon.square(x, y, width - 100, 32)
        self.simulation.add_object(PhysObject(Vec2(x, y), rect, None))

        y = height - 32
        rect = Polygon.square(x, y, width - 100, 32)
        self.simulation.add_object(PhysObject(rect.pos, rect, None))

        x, y = 32, height // 2
        rect = Polygon.square(x, y, 32, height - 100)
        self.simulation.add_object(PhysObject(rect.pos, rect, None))

        x = width - 32
        rect = Polygon.square(x, y, 32, height - 100)
        self.simulation.add_object(PhysObject(rect.pos, rect, None))

    def to_dict(self):
        enemiesList = []
        for i in range(len(self.enemies)):
            enemiesList.append(self.enemies[i].to_dict())

        projectilesList = []
        for i in range(len(self.projectiles)):
            projectilesList.append(self.projectiles[i].to_dict())

        collidableList = []
        for i in range(len(self.collidable)):
            collidableList.append(self.collidable[i].to_dict())

        dict = {"enemies": enemiesList,
                "projectiles": projectilesList,
                "collidable": collidableList}

        return dict

    # NOTE: NOT STATIC METHOD
    def from_dict(self, dict):
        self.enemies = []
        self.projectiles = []
        self.collidable = []

        self.enemies = []
        for i in dict["enemies"]:
            self.enemies.append(Monster.from_dict(i))
        for i in dict["projectiles"]:
            # TODO
            pass
        for i in dict["collidable"]:

            self.collidable.append(i.from_dict())

    def __str__(self):
        return str(self.enemies)

    def generateEnemies(self):
        for i in range(random.randrange(1, 3)):
            self.enemies.append(Monster(0, 500, 500))
        return

        if random.randrange(0, 100) < self.probOfEnemies:  # there are enemies
            roomDifficulty = random.randrange(self.minDifficulty, self.maxDifficulty + 1)
            if random.randrange(0, 100) < self.probOfSameEnemies:  # same enemies
                enemy = self.chooseEnemy()
                currDifficulty = 0
                while currDifficulty + self.enemyDifficulties[enemy] < roomDifficulty \
                        and len(self.enemies) <= self.maxEnemies:
                    currDifficulty += self.enemyDifficulties[enemy]
                    self.enemies.append(enemy)  # make sure that if you change this to an object you gen a new one
            else:  # different enemies
                enemy = self.chooseEnemy()
                currDifficulty = 0
                while currDifficulty + self.enemyDifficulties[enemy] < roomDifficulty \
                        and len(self.enemies) <= self.maxEnemies:
                    self.enemies.append(enemy)
                    currDifficulty += self.enemyDifficulties[enemy]
                    enemy = self.chooseEnemy()

    def chooseEnemy(self):
        totalProbVals = 0
        for x in range(len(self.enemyProbabilities)):
            totalProbVals += self.enemyProbabilities[x]

        currentSum = 0
        chosenEnemy = -1
        enemyRand = random.randrange(0, totalProbVals)
        for x in range(len(self.enemyProbabilities)):
            if enemyRand < currentSum + self.enemyProbabilities[x] and chosenEnemy == -1:
                chosenEnemy = x
            else:
                currentSum += self.enemyProbabilities[x]
        return chosenEnemy

    def getSprites(self):
        sprites = [
            graphics.view.SpriteToRender(self.background, self.background.rect.x + self.background.rect.width / 2,
                                         self.background.rect.y + self.background.rect.height / 2,
                                         graphics.view.GAME_WIDTH, graphics.view.WINDOW_SIZE[1])]
        sprites = sprites + [x.getSprite() for x in self.projectiles]
        sprites = sprites + [x.getSprite() for x in self.collidable]
        return sprites
