'''
Created on May 30, 2014

@author: Alex Sullivan
'''


'''
NOTES UPDATED 7/2/2014
Alex's Notes
    (7/1/2014)
    - Comments added up until the bubble class. Some noted TODO are getting the rotation of cannon to work, better cannon graphic, and learning/implementing pygame sprites..and more.
    - Finally got the chain to be recognized - Finished debugging (swapped while loop for for loop and worked every test)
    - Need to comment code -- will probably spend time writing good comments.
    (Late June)
    - Been working on recognizing the chain. Made some good progress and as you can see based on the True's when you run the code there are some connections being made.
    - My work will continue to polish this backend chain identification. You will notice I added more methods to the Bubble class and completely got RID of the placeBubble method.
    - Hashs (#) that are all the way to the left represents Code that is commented out. I also denoted most of my comments with a Date (6/25/14) so you can see what I did.
    - Also note: The GameWorld class does not really do anything right now... It will be used once the graphics and mechanis are done and we can add levels, moving bubbles, etc.
    - Let me know if you have any questions
    
Evan's Notes
	(7/2/2014)
    - Noticed that, at least in the console window, you can move the cannon and fire at the same time
'''

import pygame, sys
from pygame.locals import *
from random import randrange
from math import *

# Notes on Variables (7/1/2014)
# Rotation speed is too fast currently.
ROTATION_SPEED = 2
RADIUS = 18
DISTANCE = RADIUS * sqrt(3) 
ROWS = 14
COLUMNS_ODD = 7
COLUMNS_EVEN = 8
TOTAL_COLUMNS = COLUMNS_ODD + COLUMNS_EVEN
screenX, screenY = 640, 480
DEG_TO_RAD = 0.0174532925

# CLASS GAMEWORLD: Holds the values of the ongoing game including the current level, timer, score.
# Class currently is not being fully utilized. A temporary "test" level is being used in the GameScreen class.
class GameWorld:
    
    vX = 0  # Velocity of X direction.
    vY = 0  # Velocity of Y direction.
    
    bubbleStack = []
    bubblesOnBoard = [[]]    # Bubbles that already exist in the game world. (fieldArray)
    connectedBubbles = [[]]  # 2D Array that is part of checkBubbleChain method for bubble. 
                             #Extends to the size of a bubble chain of the same color and contains row,col position. (chainArray)
    attachedBubbles = [[]]   # Bubbles attached to specific bubble. (connArray) NOT CURRENTLY IN USE. Will be used to determine if a bubble is "free floating" and will be deleted if so.
    
    timer = 0 # NOT CURRENTLY IN USE.
    level = 0 # NOT CURRENTLY IN USE.
    score = 0 # NOT CURRENTLY IN USE.
    # maxLevel, highScore... lives?
    
    # Temporary initialization of GameWorld.
    def init__level(self, level):
        self.level = level
        # BUILD LEVEL HERE (IMPLEMENT CURR DEFAULT).
        # bubblesOnBoard = []

# CLASS GAMESCREEN: Displays the graphics of the game. Takes a gameWorld and screen that determines screen size, background layer. 
class GameScreen:
    def __init__(self, gameWorld, screen):
        self.gameWorld = gameWorld # Gameworld taken.
        self.screen = screen # Screen size, info taken.
        self.width, self.height = screen.get_size() # Width and height determined from screen.
        self.backGroundLayer = pygame.Surface(screen.get_size())
        self.cannon = Cannon() # New cannon created. Currently contains manual parameters.
        self.borderLine() # Build right line border.
        bubblesOnBoard = [   [1, 0, 0, 4, 0, 0, 3, 5],  # DEFAULT: Level 1 Test
                            [2, 1, 0, 4, 0, 0, 5],
                            [0, 0, 0, 0, 0, 0, 0, 5],
                            [0, 0, 0, 0, 0, 5, 5],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0]]
        self.loadBubbles(bubblesOnBoard) # Load board bubbles.

    def redraw(self):
        self.borderLine()
        self.drawBubbles()
        cannon.redraw()

    # getCannon: Returns cannon of GameScreen. Not necessary anymore but still implemented.
    def getCannon(self):
        return self.cannon
    
    # borderLine: Draws right line indicating the right edge of the GameScreen.   
    def borderLine(self):
        self.lineColor = (250, 250, 250) # WHITE
        self.borderX = RADIUS + Bubble.radius * TOTAL_COLUMNS # Total columns times radius of bubble plus radius for offset.
        self.borderY = screenY
        pygame.draw.line(screen, self.lineColor, (self.borderX, 0), (self.borderX, screenY), 5) # Thinking about changing this somehow. Make it more general.
        
    def drawBubbles(self):
        for bubble in GameWorld.bubbleStack:
            pygame.draw.circle(screen, bubble.bubbleColor, (bubble.getPosX(bubble.row), int(bubble.getPosY(bubble.col))), RADIUS)

            
        
    # loadBubbles: Loads and draws the first 7 rows of the GameScreen. Also clears connectedBubble array and checks for a new chain of bubbles (this can be turned into a small method
    # to clean it up). 
    def loadBubbles(self, bubblesOnBoard):
        self.bubblesOnBoard = bubblesOnBoard
        
        for row in range(ROWS): 
            for col in range(COLUMNS_EVEN):
                # If it is an even row. Load 1st 7 rows with bubbles.
                if(row % 2 == 0):
                    if(row < 8 and self.bubblesOnBoard[row][col] > 0): # If inbounds and the bubble exists (>0).
                        bubble = Bubble(bubblesOnBoard[row][col], row, col)
                        GameWorld.bubbleStack.append(bubble)
                        GameWorld.connectedBubbles = []  # Reset list to find new bubble chains. (6/25/14) This and below line can be turned into new chain method.
                        Bubble.checkBubbleChain(bubble, row, col, bubblesOnBoard)
                    
                    # If it's odd row: start grid slightly offset of left side of screen.
                else:
                    if(col < COLUMNS_ODD):
                        if(row < 8 and self.bubblesOnBoard[row][col] > 0): # If inbounds and the bubble exists (>0).
                            bubble = Bubble(bubblesOnBoard[row][col], row, col)
                            GameWorld.bubbleStack.append(bubble)
#                             pygame.draw.circle(screen, bubble.bubbleColor, (bubble.getPosX(row), int(bubble.getPosY(col))), RADIUS)
                            GameWorld.connectedBubbles = []  # Reset list to find new bubble chains. (6/25/14) This and below line can be turned into new chain method.
                            Bubble.checkBubbleChain(bubble, row, col, bubblesOnBoard)
        print GameWorld.bubbleStack.__len__()
        
# CANNON CLASS: Represents a cannon that can rotate which adjusts trajectory of a bubble. Not much implemented yet. TODO: better graphic, and working rotation methods.
class Cannon:
    def __init__(self):
        self.cannonColor = (255, 255, 255)
        # Rectangle: Left,Top,Width, Height
        self.rectangle = [(RADIUS * 8) - RADIUS, 450 - RADIUS, 2 * RADIUS, 2 * RADIUS]
        self.startRadian = pi
        self.endRadian = 2 * pi
        self.maxRight = 2.094395102 # 4PI/6
        self.maxLeft = 4.188790205  # 8PI/6
        pygame.draw.arc(screen, self.cannonColor, self.rectangle, self.startRadian, self.endRadian, 3)
    
    def redraw(self):
#         self.loadCannon() # Check if cannon needs to be loaded
        pygame.draw.arc(screen, self.cannonColor, self.rectangle, self.startRadian, self.endRadian, 3)

#     def loadCannon(self):
#         if(bubblesParked()):
#             self.addBubble()
#     
#     def addBubble(self):
#         bubbleNew = Bubble(0, 0, 0) # Make new bubble.
#         bubbleNew.cannonBubble() # Adjust bubble for cannon.
    
    # Rotate the cannon to the left at current ROTATION_SPEED.
    def rotateLeft(self, move):
        if(move and self.startRadian < self.maxLeft):
            self.startRadian += ROTATION_SPEED*DEG_TO_RAD
            self.endRadian += ROTATION_SPEED*DEG_TO_RAD
        else:
            return
    
    # Rotate the cannon to the right at current ROTATION_SPEED.
    def rotateRight(self, move):
        if(move and self.startRadian > self.maxRight):
            self.startRadian -= ROTATION_SPEED*DEG_TO_RAD
            self.endRadian -= ROTATION_SPEED*DEG_TO_RAD
        else:
            return

class Bubble:
    radius = RADIUS
    
    def __init__(self, bubbleColor, row, col):
        self.radius = RADIUS
        self.bubbleColor = self.pickColor(bubbleColor)
        self.row = row
        self.col = col
        self.posX = 0
        self.posY = 0

#     def cannonBubble(self):
#         self.bubbleColor = self.randomColor()
#         self.posX = RADIUS*8 + RADIUS # Temp Coordinates -- Pretty sure wrong (7/2/2014)
#         self.posY = 450-RADIUS

        # Added position methods for the bubble class (6/25/2014)
    def getPosX(self, col):
        if(self.row % 2 == 0):
            posX = RADIUS + self.col * RADIUS * 2;
            return posX
        else:
            posX = 2 * RADIUS + self.col * RADIUS * 2
            return posX
            
    def getPosY(self, row):
        if(self.row % 2 == 0):
            posY = RADIUS + self.row * DISTANCE;
            return posY
        else:
            posY = RADIUS + self.row * DISTANCE       
            return posY

    def randomColor(self):
        bubbleCase = randrange(5)
        if(bubbleCase == 1):
            return (12, 72, 237)  # BLUE
        elif(bubbleCase == 2):
            return (237, 12, 34)  # RED
        elif(bubbleCase == 3):
            return (0, 237, 83)  # GREEN
        elif(bubbleCase == 4):
            return (224, 255, 51)  # YELLOW
        elif(bubbleCase == 5):
            return (255, 255, 255)  # WHITE
        
    def pickColor(self, number):
        bubbleCase = number
        if(bubbleCase == 1):
            return (12, 72, 237)  # BLUE
        elif(bubbleCase == 2):
            return (237, 12, 34)  # RED
        elif(bubbleCase == 3):
            return (0, 237, 83)  # GREEN
        elif(bubbleCase == 4):
            return (224, 255, 51)  # YELLOW
        elif(bubbleCase == 5):
            return (255, 255, 255)  # WHITE
        
    # Recursively create chain of matching bubbles that are attached.
    def checkBubbleChain(self, row, col, bubblesOnBoard):
        # Exception: Out of bounds
        if row < 0 or col < 0: return
        
        odd = row % 2
#         print row,col
        
        GameWorld.connectedBubbles.append(str(row) + "," + str(col))
        
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0: 
                    if i == 0 or j == 0 or (j == -1 and odd == 0) or (j == 1 and odd == 1):
#                         print "In Range: ",self.inRange(row+i,col+j), "is a new Chain:", self.isNewChain(row+i, col+j, bubblesOnBoard[row][col], bubblesOnBoard)
                        if self.inRange(row + i, col + j) and self.isNewChain(row + i, col + j, bubblesOnBoard[row][col], bubblesOnBoard):
                            self.checkBubbleChain(row + i, col + j, bubblesOnBoard)
                
    
    # If the row and column exists return true. Else return false.
    def inRange(self, x, y):
        if(x < 0 or y < 0): return False
        if(x >= ROWS): return False
        if(x % 2 == 0 and y >= COLUMNS_EVEN): return False
        elif(x % 2 == 1 and y >= COLUMNS_ODD): return False  # Made elif and added even/odd check to fix "False" incorrectly returning (6/30/14)
        return True  # ADDED 6/25/2014: May have been error (was returning none).
    
    def isNewChain(self, row, col, val, bubblesOnBoard):
        # Return if the value is equal to the x,y are equal to the bubblesOnBoard and connectedBubbles DOES NOT (6/25/14) contain the x,y.
#         print val
#         print self.getValue(row,col, bubblesOnBoard)
#         GameWorld.connectedBubbles.__contains__(str(row)+","+str(col))
        valuesMatch = val == self.getValue(row, col, bubblesOnBoard)
#         print "value", val,"bubbleOnBoard", bubblesOnBoard[0][7], "getValue value: ",self.getValue(row,col, bubblesOnBoard)

        if str(row) + "," + str(col) in GameWorld.connectedBubbles:
            alreadyVisited = True
        else:
            alreadyVisited = False
#         print "Already Visited:", alreadyVisited, "Values are matching:", valuesMatch
        return (alreadyVisited == False) and valuesMatch
    
    # SET ON GAMESCREEN NOT WORLD
    def getValue(self, row, col, bubblesOnBoard):
        # Check Out of Range (6/25/2014) :: ADDED '-1' to account for index 0.
        if row > ROWS - 1:
            return -1
        if row % 2 == 0 and col > COLUMNS_EVEN - 1:
            return -1
        elif row % 2 == 1 and col > COLUMNS_ODD - 1:
            return -1
        
        # Check if a bubble is on the board.
        """if bubblesOnBoard[row] is None: # Don't think this is needed (6/25/2014,amsully)
            return -1"""
        if bubblesOnBoard[row][col] == None:
            return -1   
        return bubblesOnBoard[row][col]

# Initialize the game
pygame.init()

# Build screen
screen = pygame.display.set_mode((screenX, screenY), 0, 32)
backgroundColor = (0,0,0)

clock = pygame.time.Clock()
gameWorld = GameWorld()
gameScreen = GameScreen(gameWorld, screen)  # Class to build screen/play board.
cannon = gameScreen.getCannon()

gameRunning = True

while gameRunning:
    delta_Time = clock.tick(30)  # 30 Frames per second?
    
    screen.fill(backgroundColor)
    gameScreen.redraw()
    
    # CHECKS FOR ALREADY PRESSED KEYS
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[K_RIGHT]:
        cannon.rotateRight(True)
    if keys_pressed[K_LEFT]:
        cannon.rotateLeft(True)
    
    # CHECKS FOR KEYS NEWLY PRESSED/UNPRESSED
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == pygame.K_UP:  # Fire a bubble.
                print "fire"
            if event.key == pygame.K_LEFT:  # Move cannon left.
                cannon.rotateLeft(True)
            elif event.key == pygame.K_RIGHT:  # Move cannon right.
                cannon.rotateRight(True)
        elif event.type == KEYUP:
            if event.key == pygame.K_LEFT: 
                cannon.rotateLeft(False)
            elif event.key == pygame.K_RIGHT:
                cannon.rotateRight(False)

    pygame.display.update()

        