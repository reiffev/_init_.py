'''
Created on May 30, 2014

@author: Alex Sullivan
'''


'''
NOTES UPDATED 7/3/2014
Alex's Notes
    (7/2/2014)
    - Working on firing bubble. Current problem is accessing the bubbleStack list. When I try to pop/get the bubble to be fired it says that it
    is not callable and throws an exception. Spent a good amount of time troubleshooting to no avail. (Fire, gameScreen.fireBubble, if bubble
    isn't parked then move, get direction,... more methods that need implementation).
    - Added a "redraw" method for screen and cannon. Checks and loads cannon if needed.
    - Rotation of cannon working.
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
    (7/3/2014)
     - Before firing the bubble, a little calculation needs to be done. I believe that that angle of the open sector of the cannon is pi/2 to start, then either adding or subtracting
    - DEG_TO_RAD depending on turning the cannon left or right
	(7/3/2014)
    - Noticed that, at least in the console window, you can move the cannon and fire at the same time. It will be easier to see when we actually have a bubble firing
    	- Checked with the old game. This doesn't matter because once up is pressed, the ball is fired and another one won't be loaded.
    (7/3/2014)
    - Before firing the bubble, a little calculation needs to be done. I believe that that angle of the open sector of the cannon is pi/2 to start, then either adding or subtracting
    DEG_TO_RAD depending on turning the cannon left or right
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
FIRE = False
screenX, screenY = 640, 480
DEG_TO_RAD = 0.0174532925
FIRE = False

# CLASS GAMEWORLD: Holds the values of the ongoing game including the current level, timer, score.
# Class currently is not being fully utilized. A temporary "test" level is being used in the GameScreen class.
class GameWorld:

    def __init__(self):
        self.bubbleStack = []
        self.connectedBubbles = [[]]
        self.attachedBubbles = [[]]
        self.vX = 0 # Velocity of X direction. NEITHER BEING USED
        self.vY = 0 # Velocity of Y direction.

    timer = 0 # NOT CURRENTLY IN USE.
    level = 0 # NOT CURRENTLY IN USE.
    score = 0 # NOT CURRENTLY IN USE.
    # maxLevel, highScore... lives?
    
    def init__level(self, level):
    # Temporary initialization of GameWorld.
        self.level = level

# CLASS GAMESCREEN: Displays the graphics of the game. Takes a gameWorld and screen that determines screen size, background layer. 
class GameScreen:
    
    def __init__(self, gameWorld, screen):
    # Initialize gamescreen with a game world and screen. Creates game border line, cannon, level (bubblesOnBoard), and bubbles on the screen.    
        self.gameWorld = gameWorld # Gameworld taken.
        self.screen = screen # Screen size, info taken.
        self.bubblesParked = True # Variable holding whether or not all bubbles are stopped.
        self.movingBubble = Bubble(0,0,0) # Temporary bubble value. Replaced by bubble being fired.
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

    def borderLine(self):
        # borderLine: Draws right line indicating the right edge of the GameScreen.   
        self.lineColor = (250, 250, 250) # WHITE
        self.borderX = RADIUS + RADIUS * TOTAL_COLUMNS # Total columns times radius of bubble plus radius for offset.
        self.borderY = screenY
        pygame.draw.line(screen, self.lineColor, (self.borderX, 0), (self.borderX, screenY), 5) # Thinking about changing this somehow. Make it more general.

    def drawBubbles(self):
        # drawBubbles: CURRENTLY NOT WORKING. Draws the game screen of bubbles by traversing the gameWorld bubble stack. Also checks if bubble is moving (if statement) but what does not work
        #              is using it to get the bubble object for the "fireBubble" class to work above. Should be a simple fix, but it evades me (amsully).
        for index, bubble in enumerate(gameWorld.bubbleStack):
            if (bubble.move): 
                self.bubblesParked = False # Determines if all of the bubbles are stopped.
            pygame.draw.circle(screen, bubble.bubbleColor, (bubble.posX, int(bubble.posY)), RADIUS)

    def fireBubble(self):
        # fireBubble: CURRENTLY NOT WORKING. Problem in the bubbleStack list where an object cannot be used properly when trying to retrieve it.
        print "FIRE BUBBLE"
        if(not self.bubblesParked):
#             print gameWorld.bubbleStack.pop()
            print "ERROR HERE WITH LIST - fireBubble() -"
            
    def getCannon(self):
        # getCannon: Returns cannon of GameScreen. Not necessary anymore but still implemented.
        return self.cannon

    def loadBubbles(self, bubblesOnBoard):
        # loadBubbles: Loads and draws the first 7 rows of the GameScreen. Also clears connectedBubble array and checks for a new chain of bubbles (this can be turned into a small method
        # to clean it up). 
        self.bubblesOnBoard = bubblesOnBoard
        for row in range(ROWS): 
            for col in range(COLUMNS_EVEN):
                # If it is an even row. Load 1st 7 rows with bubbles.
                if(row % 2 == 0):
                    if(row < 8 and self.bubblesOnBoard[row][col] > 0): # If inbounds and the bubble exists (>0).
                        bubble = Bubble(bubblesOnBoard[row][col], row, col)
                        gameWorld.bubbleStack.append(bubble)
                        gameWorld.connectedBubbles = []  # Reset list to find new bubble chains. (6/25/14) This and below line can be turned into new chain method.
                        Bubble.checkBubbleChain(bubble, row, col, bubblesOnBoard)
                # If it's odd row: start grid slightly offset of left side of screen.
                else:
                    if(col < COLUMNS_ODD):
                        if(row < 8 and self.bubblesOnBoard[row][col] > 0): # If inbounds and the bubble exists (>0).
                            bubble = Bubble(bubblesOnBoard[row][col], row, col)
                            gameWorld.bubbleStack.append(bubble)
                            gameWorld.connectedBubbles = []  # Reset list to find new bubble chains. (6/25/14) This and below line can be turned into new chain method.
                            Bubble.checkBubbleChain(bubble, row, col, bubblesOnBoard)

    def redraw(self):
        # redraw: Called by main game loop. Updates the gameScreen's borderLine, bubbles, and cannon.
        self.borderLine()
        self.drawBubbles()
        cannon.redraw()
        
# CANNON CLASS: Represents a cannon that can rotate which adjusts trajectory of a bubble. Not much implemented yet. TODO: better graphic, and working rotation methods.
class Cannon:
    
    def __init__(self):
        self.cannonColor = (255, 0, 255)
        # Rectangle: Left,Top,Width, Height
        self.rectangle = [(RADIUS * 8) - RADIUS, 450 - RADIUS, 2 * RADIUS, 2 * RADIUS]
        self.startRadian = pi
        self.endRadian = 2 * pi
        self.maxRight = 2.094395102 # 4PI/6
        self.maxLeft = 4.188790205  # 8PI/6
        self.angle = 1.570796317    # PI/2
        pygame.draw.arc(screen, self.cannonColor, self.rectangle, self.startRadian, self.endRadian, 3)
    
    def redraw(self):
        self.loadCannon() # Check if cannon needs to be loaded
        pygame.draw.arc(screen, self.cannonColor, self.rectangle, self.startRadian, self.endRadian, 3)

    def addBubble(self):
        # addBubble: Makes a new bubble and makes it a cannonBubble. Appends to the gameWorld stack.
        bubbleNew = Bubble(0, 0, 0) # Make new bubble.
        bubbleNew.cannonBubble() # Adjust bubble for cannon.
        gameWorld.bubbleStack.append(bubbleNew)

    def loadCannon(self):
        # loadCannon: If the bubbles are not moving (assigned in game screen) then add a bubble to the cannon.
        if(gameScreen.bubblesParked):
            print "Bubble Loaded"
            self.addBubble()    

    def redraw(self):
        # redraw: Loads cannon if necessary and redraws the cannon.
        self.loadCannon() # Check if cannon needs to be loaded
        pygame.draw.arc(screen, self.cannonColor, self.rectangle, self.startRadian, self.endRadian, 3)

    def rotateLeft(self, move):
        # rotateLeft: Rotate the cannon to the left at current ROTATION_SPEED.
        # print "START %s" % self.startRadian
        # print "END %s" % self.endRadian
    	#print "START %s" % self.startRadian
    	#print "END %s" % self.endRadian
        if(move and self.startRadian < self.maxLeft):
            self.startRadian += ROTATION_SPEED*DEG_TO_RAD
            self.endRadian += ROTATION_SPEED*DEG_TO_RAD
            self.angle += DEG_TO_RAD
            print "ANGLE %f" % self.angle
        else:
            return
    
    def rotateRight(self, move):
        # rotateRight: Rotate the cannon to the right at current ROTATION_SPEED.
        # print "START %s" % self.startRadian
        # print "END %s" % self.endRadian
    	#print "START %s" % self.startRadian
    	#print "END %s" % self.endRadian
        if(move and self.startRadian > self.maxRight):
            self.startRadian -= ROTATION_SPEED*DEG_TO_RAD
            self.endRadian -= ROTATION_SPEED*DEG_TO_RAD
            self.angle -= DEG_TO_RAD
            print "ANGLE %f" % self.angle
        else:
            return

# BUBBLE CLASS: Bubble object that has a color and location. Can be turned into a cannon bubble and be assigned a movement value.
class Bubble:
    
    def __init__(self, bubbleColor, row, col):
        self.radius = RADIUS
        self.bubbleColor = self.pickColor(bubbleColor)
        self.row = row
        self.col = col
        self.posX = self.getPosX(row)
        self.posY = self.getPosY(col)
        self.move = False

    def cannonBubble(self):
        # cannonBubble: Assigns bubble to the cannon location.
        self.bubbleColor = self.randomColor()
        self.move = True
        self.posX = RADIUS*8
        self.posY = 450
        
    def checkBubbleChain(self, row, col, bubblesOnBoard):
        # checkBubbleChain: Recursively create chain of matching bubbles that are attached.
        # Exception: Out of bounds then return.
        if row < 0 or col < 0: return
        odd = row % 2
        gameWorld.connectedBubbles.append(str(row) + "," + str(col))
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0: 
                    if i == 0 or j == 0 or (j == -1 and odd == 0) or (j == 1 and odd == 1):
                        if self.inRange(row + i, col + j) and self.isNewChain(row + i, col + j, bubblesOnBoard[row][col], bubblesOnBoard): # If adjacent cell is in range and new.
                            self.checkBubbleChain(row + i, col + j, bubblesOnBoard) # Then recurse to that cell location.

    def getValue(self, row, col, bubblesOnBoard):
        # getValue: Get the color value of the bubble from the bubblesOnBoard from gameWorld. If out of bounds it returns -1.
        if row > ROWS - 1:
            return -1
        if row % 2 == 0 and col > COLUMNS_EVEN - 1:
            return -1
        elif row % 2 == 1 and col > COLUMNS_ODD - 1:
            return -1
        if bubblesOnBoard[row][col] == None:
            return -1   
        return bubblesOnBoard[row][col]     
                     
    def getPosX(self, col):
        # getPosX: Based on a column returns the X value for location.
        if(self.row % 2 == 0):
            posX = RADIUS + self.col * RADIUS * 2;
            return posX
        else:
            posX = 2 * RADIUS + self.col * RADIUS * 2
            return posX

    def getPosY(self, row):
        # getPosY: Based on a row returns the Y value for location.
        if(self.row % 2 == 0):
            posY = RADIUS + self.row * DISTANCE;
            return posY
        else:
            posY = RADIUS + self.row * DISTANCE       
            return posY        
 
    def inRange(self, x, y):
        # inRange: If the row and column exist return true. Checks row number and col number.
        if(x < 0 or y < 0): return False
        if(x >= ROWS): return False
        if(x % 2 == 0 and y >= COLUMNS_EVEN): return False
        elif(x % 2 == 1 and y >= COLUMNS_ODD): return False
        return True
 
    def isNewChain(self, row, col, val, bubblesOnBoard):
        # isNewChain: Return if the value is equal to the row and column of bubblesOnBoard (same color) and connectedBubbles DOES NOT contain the x,y (not already visited).
        valuesMatch = val == self.getValue(row, col, bubblesOnBoard) # Check same color.
        if str(row) + "," + str(col) in gameWorld.connectedBubbles: # Check if visited.
            alreadyVisited = True
        else:
            alreadyVisited = False
        return (alreadyVisited == False) and valuesMatch
       
    def move(self):
        # move: CURRENTLY NOT WORKING: Will increment the bubble based on a direction and will determine if it needs to be positioned.
        print "MOVED!"
#         x,y = self.getDirection()
#         posX += x
#         posY += y
#         if(self.bump())
#             row,col = self.closestSpot()   
        
    def pickColor(self, number):
        # pickColor: Assigns a selected color to a bubble.
        #     1 - Blue
        #     2 - Red
        #     3 - Green
        #     4 - Yellow
        #     5 - White
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
            
    def randomColor(self):
        # randomColor: Assigns a random color to a bubble. Used for loading a bubble onto a cannon.
        bubbleCase = randrange(1,6)
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

"""
______________________________________________________________________________
                            RUN GAME
"""
# Initialize the game
pygame.init()

# Build: screem, clock, world, cannon.
screen = pygame.display.set_mode((screenX, screenY), 0, 32)
backgroundColor = (0,0,0)
clock = pygame.time.Clock()
gameWorld = GameWorld()
gameScreen = GameScreen(gameWorld, screen)  # Class to build screen/play board.
cannon = gameScreen.getCannon()

# Game loop.
gameRunning = True
while gameRunning:
    delta_Time = clock.tick(30)  # 30 Frames per second?
    screen.fill(backgroundColor) # Reset screen.
    gameScreen.redraw()          # Redraw screen.
    
    # CHECKS FOR ALREADY PRESSED KEYS
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[K_RIGHT]:   # Rotate cannon right.
        cannon.rotateRight(True)
    if keys_pressed[K_LEFT]:    # Rotate cannon left.
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
                gameScreen.fireBubble()
                FIRE = True
                print "True"
            	print "fire"
            	gameScreen.fireBubble()
            	FIRE = True
            	print "True"
            elif event.key == pygame.K_LEFT: # Move cannon left.
            	print "FIRE = %f" % FIRE
            	if FIRE == False:
            		cannon.rotateLeft(True)
            	else:
            		cannon.rotateLeft(False)
            	print "FIRE = %f" % FIRE
            elif event.key == pygame.K_RIGHT:  # Move cannon right.
            	print "FIRE = %f" % FIRE
            	if FIRE == False:
            		cannon.rotateRight(True)
            	else:
            		cannon.rotateRight(False)
            	print "FIRE = %f" % FIRE
        elif event.type == KEYUP:
        	if event.key == pygame.K_UP:
        		FIRE = False
        		print "False"
        	if event.key == pygame.K_LEFT: 
        		cannon.rotateLeft(False)
        	elif event.key == pygame.K_RIGHT:
        		cannon.rotateRight(False)

    pygame.display.update()

        