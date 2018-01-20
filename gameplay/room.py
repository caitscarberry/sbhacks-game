import random

class Room:
    def __init__(self):
        self.enemyDifficulties = [1,2,3,5,7]
        self.enemyProbabilities = [7,6,8,5,4]
        #following probabilities given as a percentage out of 100 (0-99)
        self.probOfEnemies = 75
        self.probOfSameEnemies = 50
        self.minDifficulty = 3
        self.maxDifficulty = 17
        self.maxEnemies = 5
        self.enemies = []

        self.generateEnemies()

    def __str__(self):
        return str(self.enemies)

    def generateEnemies(self):
        if random.randrange(0,100) < self.probOfEnemies: #there are enemies
            roomDifficulty = random.randrange(self.minDifficulty, self.maxDifficulty + 1)
            if random.randrange(0, 100) < self.probOfSameEnemies: #same enemies
                enemy = self.chooseEnemy()
                currDifficulty = 0
                while currDifficulty + self.enemyDifficulties[enemy] < roomDifficulty \
                        and len(self.enemies) <= self.maxEnemies:
                    currDifficulty += self.enemyDifficulties[enemy]
                    self.enemies.append(enemy) #make sure that if you change this to an object you gen a new one
            else: #different enemies
                enemy = self.chooseEnemy()
                currDifficulty = 0
                while currDifficulty + self.enemyDifficulties[enemy] < roomDifficulty\
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
