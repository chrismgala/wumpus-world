""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Created by:
Chris Gala
galac@uci.edu

CS 171 - Project
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Agent():

    def __init__(self):
        "All of the class variables including leftTurns (turn count), direction, and state trackers"

        self.wumpus         = {}
        self.pit            = {}
        self.visited        = set()
        self.rowsVisited    = set([1])
        self.safe           = set()
        self.death          = set()
        self.lastSpot       = set()

        self.leftTurns      = 0
        self.row            = 1
        self.col            = 1
        self.boardSize      = 0
        self.score          = 0
        self.scoreCap       = 0
        self.sameTile       = 0

        self.up             = False
        self.down           = False
        self.right          = True
        self.left           = False

        self.hasGold        = False
        self.killedWumpus   = False
        self.shotArrow      = False
        self.justShotArrow  = False
        self.startSpot      = True
        self.newRow         = False
        self.facingDeath    = False

    def get_move(self, percepts):
        "Takes in set of String (percepts) and returns String specifying the Agent's move or action"

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Clear lastSpot so that it only has the MOST RECENT tile (1 tile)
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if (len(self.lastSpot) > 1):
            self.lastSpot.pop()

        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        leftTurns shows whether Agent is facing right, up, left, or down
        1 == Up
        2 == Left
        3 == Down
        4 == Right
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

        if self.leftTurns == 1 or self.leftTurns == 5:
            self.up = True
            self.down = False
            self.left = False
            self.right = False
            if self.leftTurns == 5:
                self.leftTurns -= 4

        if self.leftTurns == 2 or self.leftTurns == 6:
            self.left = True
            self.right = False
            self.up = False
            self.down = False
            if self.leftTurns == 6:
                self.leftTurns -= 4

        if self.leftTurns == 3 or self.leftTurns == 7:
            self.down = True
            self.up = False
            self.left = False
            self.right = False
            if self.leftTurns == 7:
                self.leftTurns -= 4


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Reset so we keep the count within 1-7 (Right = 3 Left turns)
        (focus on those 4 numbers only to determine direction instead of
        a bunch of numbers)
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if self.leftTurns == 4 or self.leftTurns == 8:
            self.right = True
            self.left = False
            self.up = False
            self.down = False
            self.leftTurns = 0


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Handle potential errors and outer boundaries in coordinate
        tracking, also once you hit a wall, set the boardSize to the
        corresponding value (only need row or col b/c it is a square)
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if self.up and "Bump" in percepts:
            self.row = 1

        if self.down and "Bump" in percepts:
            self.row -= 1
            if self.boardSize == 0:
                self.boardSize = self.row
                if self.boardSize == 4:
                    self.scoreCap = 35
                if self.boardSize == 5:
                    self.scoreCap = 45
                if self.boardSize == 6:
                    self.scoreCap = 50
                if self.boardSize == 7:
                    self.scoreCap = 55

        if self.left and "Bump" in percepts:
            self.col = 1

        if self.right and "Bump" in percepts:
            self.col -= 1
            if self.boardSize == 0:
                self.boardSize = self.col
                if self.boardSize == 4:
                    self.scoreCap = 35
                if self.boardSize == 5:
                    self.scoreCap = 45
                if self.boardSize == 6:
                    self.scoreCap = 50
                if self.boardSize == 7:
                    self.scoreCap = 55


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Add coordinates of visited tiles for cross referencing
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        self.visited.add((self.row, self.col))


        print("===========================================")
        print("Row: ", self.row, "\nCol: ", self.col)
        print("Avoid wumpus: ", self.wumpus)
        print("Avoid Pit: ", self.pit)
        print("Visited: ", self.visited)
        print("No Add: ", self.safe)
        print("Last Spot: ", self.lastSpot)
        print("-------------------------------------------")
        print("UP: ", self.up)
        print("DOWN: ", self.down)
        print("LEFT: ", self.left)
        print("RIGHT: ", self.right)
        print("Left Turns: ", self.leftTurns)
        print("Has Gold: ", self.hasGold)
        print("Killed Wumpus: ", self.killedWumpus)
        print("Shot Arrow: ", self.shotArrow)
        print("New Row: ", self.newRow)
        print("Board Size: ", self.boardSize)
        print("Score :", self.score)
        print("Start Spot: ", self.startSpot)
        print("Facing Death: ", self.facingDeath)
        print("Score Cap: ", self.scoreCap)
        print("Same Tile: ", self.sameTile)
        print("===========================================")


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Get coordinates with the highest count, because it is the most
        likely spot for a wumpus to be in
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if (len(self.wumpus) > 0):
            self.death.add(max(self.wumpus, key=self.wumpus.get))


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Check if Agent is in the starting tile
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if self.row == 1 and self.col == 1:
            self.startSpot = True


        if self.row != 1 or self.col != 1:
            self.startSpot = False


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        If the Agent's score goes past the number of tiles in the board,
        then pull it out of the game to prevent endless loops and hurting
        the overall score
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if self.scoreCap > 0 or self.score < -49:
            if abs(self.score) > self.scoreCap:
                self.hasGold = True


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Agent is stuck in a loop so yank it out of the cave
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if self.sameTile >= 4:
            self.hasGold = True


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        If the gold is in your tile, grab it, and start heading back
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if "Glitter" in percepts:
            self.hasGold = True
            return "Grab"


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        If there is a breeze in the starting tile or you have gold, leave
        the cave
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if self.startSpot == True:
            if "Breeze" in percepts or self.hasGold == True:
                return "Climb"


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Keep turning until facing Up once you have the gold
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if self.hasGold and self.up == False and self.row != 1 and self.facingDeath == False:
            if self.right:
                self.leftTurns += 1
                self.score -= 1

                self.sameTile += 1

                return "Left"

            if self.left:
                self.leftTurns += 3
                self.score -= 1

                self.sameTile += 1

                return "Right"


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Keep turning until facing Up once you have the gold
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if self.hasGold and self.left == False and self.row == 1:
            if self.right:
                self.leftTurns += 1
                self.score -= 1

                self.sameTile += 1

                return "Left"


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        If the Agent is on a odd numbered row, go right
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if self.right == False and self.row % 2 != 0 and self.hasGold == False and self.row not in self.rowsVisited:
            self.newRow = True
            self.rowsVisited.add(self.row)
            self.leftTurns += 1
            self.score -= 1

            self.sameTile += 1

            return "Left"


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        If the Agent is on a new row, turn right
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if self.down and self.hasGold == False and self.row not in self.rowsVisited:
            self.newRow = True
            self.rowsVisited.add(self.row)
            self.leftTurns += 3
            self.score -= 1

            self.sameTile += 1

            return "Right"


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        If you are in a tile with Stench, shoot your arrow if you haven't
        already and if the Wumpus has not already been killed
        (also checks to make sure you have not just hit/faced a wall)
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if "Stench" in percepts and "Bump" not in percepts and self.killedWumpus == False and self.shotArrow == False:
            if self.left == True and self.col != 1:
                self.shotArrow = True
                self.justShotArrow = True
                self.score -= 11
                return "Shoot"
            if self.right == True and self.col != self.boardSize:
                self.shotArrow = True
                self.justShotArrow = True
                self.score -= 11
                return "Shoot"


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        If you hit a wall while trying to find gold in a NEW ROW, turn
        left
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if "Bump" in percepts and self.hasGold == False and self.left == True and (self.newRow == True or self.row == 1):
            self.leftTurns += 1
            self.score -= 1

            self.sameTile += 1

            return "Left"


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        If you hit a wall while trying to find gold, turn right
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if "Bump" in percepts and self.hasGold == False:
            self.leftTurns += 3
            self.score -= 1

            self.sameTile += 1

            return "Right"


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        If you hit a wall while returning home, turn left
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if "Bump" in percepts and self.hasGold == True:
            self.leftTurns += 1
            self.score -= 1

            self.sameTile += 1

            return "Left"


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Wumpus is dead
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if "Scream" in percepts:
            self.killedWumpus = True
            self.wumpus.clear()


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Add coordinates to the Pit / Wumpus arrays when stepping into a
        tile with a Stench / Breeze
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if self.right == True:
            if "Stench" in percepts and self.killedWumpus == False:
                if self.boardSize == 0:

                    if (self.row + 1, self.col) not in self.wumpus.keys() and (self.row + 1, self.col) not in self.safe:
                        self.wumpus[(self.row + 1, self.col)] = 1

                    if (self.row, self.col + 1) not in self.wumpus.keys() and (self.row, self.col + 1) not in self.safe:
                        self.wumpus[(self.row, self.col + 1)] = 1

                    elif (self.row + 1, self.col) in self.wumpus.keys():
                        self.wumpus[(self.row + 1, self.col)] += 1

                    elif (self.row, self.col + 1) in self.wumpus.keys():
                        self.wumpus[(self.row, self.col + 1)] += 1

                if self.boardSize != 0:
                    if (self.row + 1) <= self.boardSize:

                        if (self.row + 1, self.col) not in self.wumpus.keys() and (self.row + 1, self.col) not in self.safe:
                            self.wumpus[(self.row + 1, self.col)] = 1

                        elif (self.row + 1, self.col) in self.wumpus.keys():
                            self.wumpus[(self.row + 1, self.col)] += 1

                    if (self.col + 1) <= self.boardSize:

                        if (self.row, self.col + 1) not in self.wumpus.keys() and (self.row, self.col + 1) not in self.safe:
                            self.wumpus[(self.row, self.col + 1)] = 1

                        elif (self.row, self.col + 1) in self.wumpus.keys():
                            self.wumpus[(self.row, self.col + 1)] += 1

                if self.row > 1:

                    if (self.row - 1, self.col) not in self.wumpus.keys() and (self.row - 1, self.col) not in self.safe:
                        self.wumpus[(self.row - 1, self.col)] = 1

                    elif (self.row - 1, self.col) in self.wumpus.keys():
                        self.wumpus[(self.row - 1, self.col)] += 1

            if "Breeze" in percepts:
                if self.boardSize == 0:

                    if (self.row + 1, self.col) not in self.pit.keys() and (self.row + 1, self.col) not in self.safe:
                        self.pit[(self.row + 1, self.col)] = 1

                    if (self.row, self.col + 1) not in self.pit.keys() and (self.row, self.col + 1) not in self.safe:
                        self.pit[(self.row, self.col + 1)] = 1

                    elif (self.row + 1, self.col) in self.pit.keys():
                        self.pit[(self.row + 1, self.col)] += 1

                    elif (self.row, self.col + 1) in self.pit.keys():
                        self.pit[(self.row, self.col + 1)] += 1

                if self.boardSize != 0:
                    if (self.row + 1) <= self.boardSize:

                        if (self.row + 1, self.col) not in self.pit.keys() and (self.row + 1, self.col) not in self.safe:
                            self.pit[(self.row + 1, self.col)] = 1

                        elif (self.row + 1, self.col) in self.pit.keys():
                            self.pit[(self.row + 1, self.col)] += 1

                    if (self.col + 1) <= self.boardSize:

                        if (self.row, self.col + 1) not in self.pit.keys() and (self.row, self.col + 1) not in self.safe:
                            self.pit[(self.row, self.col + 1)] = 1

                        elif (self.row, self.col + 1) in self.pit.keys():
                            self.pit[(self.row, self.col + 1)] += 1

                if self.row > 1:

                    if (self.row - 1, self.col) not in self.pit.keys() and (self.row - 1, self.col) not in self.safe:
                        self.pit[(self.row - 1, self.col)] = 1

                    elif (self.row - 1, self.col) in self.pit.keys():
                        self.pit[(self.row - 1, self.col)] += 1

        if self.left == True:
            if "Stench" in percepts and self.killedWumpus == False:
                if self.boardSize == 0:

                    if (self.row + 1, self.col) not in self.wumpus.keys() and (self.row + 1, self.col) not in self.safe:
                        self.wumpus[(self.row + 1, self.col)] = 1

                    elif (self.row + 1, self.col) in self.wumpus.keys():
                        self.wumpus[(self.row + 1, self.col)] += 1

                if self.boardSize != 0:
                    if (self.row + 1) <= self.boardSize:

                        if (self.row + 1, self.col) not in self.wumpus.keys() and (self.row + 1, self.col) not in self.safe:
                            self.wumpus[(self.row + 1, self.col)] = 1

                        elif (self.row + 1, self.col) in self.wumpus.keys():
                            self.wumpus[(self.row + 1, self.col)] += 1

                if self.col > 1:

                    if (self.row, self.col - 1) not in self.wumpus.keys() and (self.row, self.col - 1) not in self.safe:
                        self.wumpus[(self.row, self.col - 1)] = 1

                    elif (self.row, self.col - 1) in self.wumpus.keys():
                        self.wumpus[(self.row, self.col - 1)] += 1

                if self.row > 1:

                    if (self.row - 1, self.col) not in self.wumpus.keys() and (self.row - 1, self.col) not in self.safe:
                        self.wumpus[(self.row - 1, self.col)] = 1

                    elif (self.row - 1, self.col) in self.wumpus.keys():
                        self.wumpus[(self.row - 1, self.col)] += 1

            if "Breeze" in percepts:
                if self.boardSize == 0:

                    if (self.row + 1, self.col) not in self.pit.keys() and (self.row + 1, self.col) not in self.safe:
                        self.pit[(self.row + 1, self.col)] = 1

                    elif (self.row + 1, self.col) in self.pit.keys():
                        self.pit[(self.row + 1, self.col)] += 1

                if self.boardSize != 0:
                    if (self.row + 1) <= self.boardSize:

                        if (self.row + 1, self.col) not in self.pit.keys() and (self.row + 1, self.col) not in self.safe:
                            self.pit[(self.row + 1, self.col)] = 1

                        elif (self.row + 1, self.col) in self.pit.keys():
                            self.pit[(self.row + 1, self.col)] += 1

                if self.col > 1:

                    if (self.row, self.col - 1) not in self.pit.keys() and (self.row, self.col - 1) not in self.safe:
                        self.pit[(self.row, self.col - 1)] = 1

                    elif (self.row, self.col - 1) in self.pit.keys():
                        self.pit[(self.row, self.col - 1)] += 1

                if self.row > 1:

                    if (self.row - 1, self.col) not in self.pit.keys() and (self.row - 1, self.col) not in self.safe:
                        self.pit[(self.row - 1, self.col)] = 1

                    elif (self.row - 1, self.col) in self.pit.keys():
                        self.pit[(self.row - 1, self.col)] += 1

        if self.down == True:
            if "Stench" in percepts and self.killedWumpus == False:
                if self.boardSize == 0:

                    if (self.row + 1, self.col) not in self.wumpus.keys() and (self.row + 1, self.col) not in self.safe:
                        self.wumpus[(self.row + 1, self.col)] = 1

                    if (self.row, self.col + 1) not in self.wumpus.keys() and (self.row, self.col + 1) not in self.safe:
                        self.wumpus[(self.row, self.col + 1)] = 1

                    elif (self.row + 1, self.col) in self.wumpus.keys():
                        self.wumpus[(self.row + 1, self.col)] += 1

                    elif (self.row, self.col + 1) in self.wumpus.keys():
                        self.wumpus[(self.row, self.col + 1)] += 1

                if self.boardSize != 0:

                    if (self.row + 1) <= self.boardSize:

                        if (self.row + 1, self.col) not in self.wumpus.keys() and (self.row + 1, self.col) not in self.safe:
                            self.wumpus[(self.row + 1, self.col)] = 1

                        elif (self.row + 1, self.col) in self.wumpus.keys():
                            self.wumpus[(self.row + 1, self.col)] += 1

                    if (self.col + 1) <= self.boardSize:

                        if (self.row, self.col + 1) not in self.wumpus.keys() and (self.row, self.col + 1) not in self.safe:
                            self.wumpus[(self.row, self.col + 1)] = 1

                        elif (self.row, self.col + 1) in self.wumpus.keys():
                            self.wumpus[(self.row, self.col + 1)] += 1

                if self.col > 1:

                    if (self.row, self.col - 1) not in self.wumpus.keys() and (self.row, self.col - 1) not in self.safe:
                        self.wumpus[(self.row, self.col - 1)] = 1

                    elif (self.row, self.col - 1) in self.wumpus.keys():
                        self.wumpus[(self.row, self.col - 1)] += 1

            if "Breeze" in percepts:
                if self.boardSize == 0:

                    if (self.row + 1, self.col) not in self.pit.keys() and (self.row + 1, self.col) not in self.safe:
                        self.pit[(self.row + 1, self.col)] = 1

                    if (self.row, self.col + 1) not in self.pit.keys() and (self.row, self.col + 1) not in self.safe:
                        self.pit[(self.row, self.col + 1)] = 1

                    elif (self.row + 1, self.col) in self.pit.keys():
                        self.pit[(self.row + 1, self.col)] += 1

                    elif (self.row, self.col + 1) in self.pit.keys():
                        self.pit[(self.row, self.col + 1)] += 1

                if self.boardSize != 0:

                    if (self.row + 1) <= self.boardSize:

                        if (self.row + 1, self.col) not in self.pit.keys() and (self.row + 1, self.col) not in self.safe:
                            self.pit[(self.row + 1, self.col)] = 1

                        elif (self.row + 1, self.col) in self.pit.keys():
                            self.pit[(self.row + 1, self.col)] += 1

                    if (self.col + 1) <= self.boardSize:

                        if (self.row, self.col + 1) not in self.pit.keys() and (self.row, self.col + 1) not in self.safe:
                            self.pit[(self.row, self.col + 1)] = 1

                        elif (self.row, self.col + 1) in self.pit.keys():
                            self.pit[(self.row, self.col + 1)] += 1

                if self.col > 1:

                    if (self.row, self.col - 1) not in self.pit.keys() and (self.row, self.col - 1) not in self.safe:
                        self.pit[(self.row, self.col - 1)] = 1

                    elif (self.row, self.col - 1) in self.pit.keys():
                        self.pit[(self.row, self.col - 1)] += 1

        if self.up == True:
            if "Stench" in percepts and self.killedWumpus == False:
                if self.boardSize == 0:

                    if (self.row, self.col + 1) not in self.wumpus.keys() and (self.row, self.col + 1) not in self.safe:
                        self.wumpus[(self.row, self.col + 1)] = 1

                    elif (self.row, self.col + 1) in self.wumpus.keys():
                        self.wumpus[(self.row, self.col + 1)] += 1

                if self.boardSize != 0:
                    if (self.col + 1) <= self.boardSize:

                        if (self.row, self.col + 1) not in self.wumpus.keys() and (self.row, self.col + 1) not in self.safe:
                            self.wumpus[(self.row, self.col + 1)] = 1

                        elif (self.row, self.col + 1) in self.wumpus.keys():
                            self.wumpus[(self.row, self.col + 1)] += 1

                if self.col > 1:

                    if (self.row, self.col - 1) not in self.wumpus.keys() and (self.row, self.col - 1) not in self.safe:
                        self.wumpus[(self.row, self.col - 1)] = 1

                    elif (self.row, self.col - 1) in self.wumpus.keys():
                        self.wumpus[(self.row, self.col - 1)] += 1

                if self.row > 1:

                    if (self.row - 1, self.col) not in self.wumpus.keys() and (self.row - 1, self.col) not in self.safe:
                        self.wumpus[(self.row - 1, self.col)] = 1

                    elif (self.row - 1, self.col) in self.wumpus.keys():
                        self.wumpus[(self.row - 1, self.col)] += 1

            if "Breeze" in percepts:
                if self.boardSize == 0:

                    if (self.row, self.col + 1) not in self.pit.keys() and (self.row, self.col + 1) not in self.safe:
                        self.pit[(self.row, self.col + 1)] = 1

                    elif (self.row, self.col + 1) in self.pit.keys():
                        self.pit[(self.row, self.col + 1)] += 1

                if self.boardSize != 0:
                    if (self.col + 1) <= self.boardSize:

                        if (self.row, self.col + 1) not in self.pit.keys() and (self.row, self.col + 1) not in self.safe:
                            self.pit[(self.row, self.col + 1)] = 1

                        elif (self.row, self.col + 1) in self.pit.keys():
                            self.pit[(self.row, self.col + 1)] += 1

                if self.col > 1:

                    if (self.row, self.col - 1) not in self.pit.keys() and (self.row, self.col - 1) not in self.safe:
                        self.pit[(self.row, self.col - 1)] = 1

                    elif (self.row, self.col - 1) in self.pit.keys():
                        self.pit[(self.row, self.col - 1)] += 1

                if self.row > 1:

                    if (self.row - 1, self.col) not in self.pit.keys() and (self.row - 1, self.col) not in self.safe:
                        self.pit[(self.row - 1, self.col)] = 1

                    elif (self.row - 1, self.col) in self.pit.keys():
                        self.pit[(self.row - 1, self.col)] += 1


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Remove out of bounds coordinates from Wumpus and Pit dicts, if
        any were recorded
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if len(self.wumpus) > 0:
            temp = None
            for key in self.wumpus.keys():
                if key in self.visited:
                    self.safe.add(key)
                    temp = key
            if temp != None:
                del self.wumpus[temp]

        if len(self.pit) > 0:
            temp2 = None
            for key in self.pit.keys():
                if key in self.visited:
                    self.safe.add(key)
                    temp2 = key
            if temp2 != None:
                del self.pit[temp2]


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        If arrow was shot but no Wumpus was killed, add possible Wumpus
        coordinates
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if self.justShotArrow == True and "Scream" not in percepts:
            if self.right:
                if self.row == 1:
                    if (self.row + 1, self.col) not in self.wumpus.keys():
                        self.wumpus[(self.row + 1, self.col)] = 1
                    elif (self.row + 1, self.col) in self.wumpus.keys():
                        self.wumpus[(self.row + 1, self.col)] += 1

                if self.row == self.boardSize:
                    if (self.row - 1, self.col) not in self.wumpus.keys():
                        self.wumpus[(self.row - 1, self.col)] = 1
                    elif (self.row - 1, self.col) in self.wumpus.keys():
                        self.wumpus[(self.row - 1, self.col)] += 1


        """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        Use dictionaries of potential danger spots to prevent moving
        Forward into a Wumpus or Pit tile
        """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
        if self.right == True:
            if (self.row, self.col + 1) in self.death:
                self.facingDeath = True

            elif (self.row, self.col + 1) in self.pit.keys():
                self.facingDeath = True

            elif (self.row, self.col + 1) not in self.death and (self.row, self.col + 1) not in self.pit.keys():
                self.facingDeath = False

        if self.down == True:
            if (self.row + 1, self.col) in self.death:
                self.facingDeath = True

            elif (self.row + 1, self.col) in self.pit.keys():
                self.facingDeath = True

            elif (self.row + 1, self.col) not in self.death and (self.row + 1, self.col) not in self.pit.keys():
                self.facingDeath = False

        if self.left == True:
            if (self.row, self.col - 1) in self.death:
                self.facingDeath = True

            elif (self.row, self.col - 1) in self.pit.keys():
                self.facingDeath = True

            elif (self.row, self.col - 1) not in self.death and (self.row, self.col - 1) not in self.pit.keys():
                self.facingDeath = False

        if self.up == True:
            if (self.row - 1, self.col) in self.death:
                self.facingDeath = True

            elif (self.row - 1, self.col) in self.pit.keys():
                self.facingDeath = True

            elif (self.row - 1, self.col) not in self.death and (self.row - 1, self.col) not in self.pit.keys():
                self.facingDeath = False


        if self.facingDeath == True:
            self.justShotArrow = False
            self.score -= 1
            self.leftTurns += 3

            self.sameTile += 1

            return "Right"


        if (self.row, self.col) not in self.lastSpot:
            self.sameTile = 0


        if self.facingDeath == False:
            """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            Keep track of coordinates ((1,1) is the starting tile) and add
            current tile to lastSpot before moving to new tile
            """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
            if (self.row, self.col) not in self.lastSpot:
                self.lastSpot.add((self.row, self.col))

            if self.down:
                self.row += 1

            if self.up and self.row > 1:
                self.row -= 1

            if self.right:
                self.col += 1

            if self.left and self.col > 1:
                self.col -= 1

            self.justShotArrow = False
            self.score -= 1

            if self.up and self.row == 1:
                self.sameTile += 1

            if self.down and self.row == self.boardSize:
                self.sameTile += 1

            if self.left and self.col == 1:
                self.sameTile += 1

            if self.right and self.col == self.boardSize:
                self.sameTile += 1

            return "Forward"
