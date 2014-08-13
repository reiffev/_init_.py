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
    (7/21/2014)
    - Getting this error after firing
    	Traceback (most recent call last):
  			File "init2.py", line 603, in <module>
    			Bubble.move(gameWorld.bubbleStack[-1]) # (7/17/2014) call the move method in 
    			the main loop so that the bubble can keep moving
  			File "init2.py", line 390, in move self.parkBubble() 
  			File "init2.py", line 410, in parkBubble
    			if gameScreen.bubblesOnBoard[row][col]>0: #check if the cell has been occupied
			TypeError: list indices must be integers, not float
	(8/11/2014)
	- Change made in parkBubble
	- row and col in parkBubble were floats. Fixed the bug. Occasionally running into this error, similar to the one above:
		Traceback (most recent call last):
  			File "init2.py", line 625, in <module>
    			Bubble.move(gameWorld.bubbleStack[-1]) # (7/17/2014) call the move method in 
    			the main loop so that the bubble can keep moving
 			File "init2.py", line 404, in move self.parkBubble() 
  			File "init2.py", line 450, in parkBubble
    			self.placeBubble(row,col)
  			File "init2.py", line 525, in placeBubble
    			gameScreen.bubblesOnBoard[row][col]=2
			TypeError: list indices must be integers, not float
	(8/12/2014)
	- While trying to fix the bug from yesterday, noticed that we haven't implemented the function where if you clear bubbles
	and bubbles are left in free space (not touching any walls and detached from everything else) they don't go away
	- Bug from yesterday is hard to recreate, but I have placed comments where I am getting the errors
	
'''

'''
Zhuotao's Notes:
    (7/21/2014) 
    - Problem: 1. Bubble can't move in accurate direction
               2. REMOVING UNATTACHED BUBBLES part is not finished yet
'''

import pygame, sys, math
from pygame.locals import *
from random import randrange
from math import *

# Notes on Variables (7/1/2014)
# Rotation speed is too fast currently.
ROTATION_SPEED = 1 # (7/21/2014) change from 2 to 1 
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

BUBBLE_SPEED=20 # (7/17/2014) add variable BUBBLE_SPEED
pointsForConnection=100 # (7/19/2014) add variable pointsForConnection. NOT BEING USED

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
                            [0, 0, 0, 0, 0, 0, 0, 4], # (7/19) change 5 to 4 for testing
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
            
            pygame.draw.circle(screen, bubble.bubbleColor, (int(bubble.posX), int(bubble.posY)), RADIUS) # (7/17/2014) cast posX, posY to int to avoid the error
          
            

    def fireBubble(self):
        # fireBubble: CURRENTLY NOT WORKING. Problem in the bubbleStack list where an object cannot be used properly when trying to retrieve it.
        print("FIRE BUBBLE")
        if(not self.bubblesParked):
            
            '''
                (7/17/2014) Notes: Fixed the problem of firing bubble (change by Zhuotao Huang)
                problem: Noticed that "math.cos()" and "math.sin()" return float numbers, but the coordinates of the bubble have 
                        to be int. When we redraw the bubbles, it will give us an error. Thus, I just cast posX and posY 
                        to int to avoid the error when redraw the bubbles, but I don't think it's the best way to fix it,
                        because it turns out that the bubble can't move in the accurate direction. 
                (7/21/2014) Evan Reiff
                	I don't think the error is here. Three lines that are showing up in the error log are (around) 613, 400, and 420. The line
                	numbers depend on when you run it with all the comments
            '''
            gameWorld.bubbleStack[-1].velX = BUBBLE_SPEED * math.cos(self.cannon.angle) # set x velocity
            gameWorld.bubbleStack[-1].velY = -BUBBLE_SPEED * math.sin(self.cannon.angle) # set y velocity

            

#             print gameWorld.bubbleStack.pop()
#            print("ERROR HERE WITH LIST - fireBubble() -")
            
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
            print('============================================================')
            print("Bubble Loaded")
            self.addBubble()   
            
            '''
                7/19 testing
            
            for i in range(0,13):
                if i%2==0:
                    print('-------------------------------')
                    for j in range (0,8):
                        print(gameScreen.bubblesOnBoard[i][j])
                else:
                    print('--------------------------------')
                    for k in range(0,7):
                        print(gameScreen.bubblesOnBoard[i][k])
            '''
             
    '''
    (7/17/2014) Duplicated codes. just comment it out.
    
    def redraw(self):
        # redraw: Loads cannon if necessary and redraws the cannon.
        self.loadCannon() # Check if cannon needs to be loaded
        pygame.draw.arc(screen, self.cannonColor, self.rectangle, self.startRadian, self.endRadian, 3)
    '''
            
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
            print("ANGLE %f" % self.angle)
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
            print("ANGLE %f" % self.angle)
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
        
        self.velX=0 # (7/17) add variable velX
        self.velY=0 # (7/17) add variable velY
        self.name=str(row)+','+str(col) # (7/19) add variable name

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
                        # (7/21/2014) Find an error: list index out of range. NOT FIXED YET.
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
   #     print("MOVED!")
#         x,y = self.getDirection()
#         posX += x
#         posY += y
#         if(self.bump())
#             row,col = self.closestSpot() 
        
        
        # (7/17/2014) Move the bubble after firing, check collisions with walls and top
         
        self.posX+=self.velX
        self.posY+=self.velY
        if self.posX-RADIUS<=0:
            self.velX*=-1
        elif self.posX+RADIUS>=RADIUS + RADIUS * TOTAL_COLUMNS:
            self.velX*=-1
        else:
            pass
        if self.posY-RADIUS<=0:
            self.parkBubble()
        else:
            for index, bubble in enumerate(gameWorld.bubbleStack):
                if(index!=len(gameWorld.bubbleStack)-1 and math.pow(bubble.posX-self.posX,2)+math.pow(bubble.posY-self.posY,2)<=math.pow((2*RADIUS-4),2)):
                    print('index='+str(index))
                    print(index!=len(gameWorld.bubbleStack)-1)
                    print(math.pow(bubble.posX-self.posX,2)+math.pow(bubble.posY-self.posY,2)<=math.pow((2*RADIUS-4),2))
                    #(7/21/2014) Error after firing showing up here
                    #(8/11/2014) Error occurring occasionally
                    self.parkBubble() 
        
    # (7/19/2014) add new methods - parkBubble
    # (7/21/2014) Problem: Sometimes the bubble will go out of the screen from the top
    # (7/21/2014) Notes: The REMOVING UNATTACHED BUBBLES part is not finished.
    def parkBubble(self):
        print('Bubble Parked')
        
        row=math.floor(self.posY/DISTANCE)
        col=0
        
        #depending on the row changes the way the column is calculated
        if row%2==0:
            col=math.floor(self.posX/(2*RADIUS))
        else:
            col=math.floor((self.posX-RADIUS)/(2*RADIUS))
        
        """(8/11/2014) row and col were floats for some reason. changed them to ints. Sometimes running into an error.
        See comments above"""
        row = int(row)
        col = int(col)
        print row, col
        
        if self.inRange(row, col)==False:
            print('LOST or ERROR: index out of range')
        else: 
        	#(7/21/2014) Error after firing showing up here
            if gameScreen.bubblesOnBoard[row][col]>0: #check if the cell has been occupied
                row+=1
                if (row%2==0):
                    col = math.floor(self.posX/(RADIUS*2))
                else:
                    col = math.floor((self.posX-RADIUS)/(RADIUS*2))
        
            if (row%2==0):
                self.posX=(col*RADIUS*2)+RADIUS
            else:
                self.posX=(col*RADIUS*2)+2*RADIUS
                
            self.posY=(row*DISTANCE)+RADIUS
            gameWorld.connectedBubbles = [] 
            self.name=str(row)+','+str(col)
            self.row=int(row)
            self.col=int(col)
            self.move=False
            gameScreen.bubblesParked=True
            #(8/11/2014) Error occurring occasionally
            self.placeBubble(row,col)
            # gameScreen.loadBubbles(gameScreen.bubblesOnBoard)
            self.checkBubbleChain(row, col, gameScreen.bubblesOnBoard)
            print(len(gameWorld.connectedBubbles))
            if(len(gameWorld.connectedBubbles)>2):
                for i in range(0,len(gameWorld.connectedBubbles)):
                    gameWorld.score+=pointsForConnection
                    # showGameScore()
                    # gameScreen.bubblesOnBoard.remove(gameWorld.connectedBubbles[i])
                    
                  
                    for j in range(0,len(gameWorld.bubbleStack)-1):
                        # print('j:'+str(j))
                        # print('stack: '+str(gameWorld.bubbleStack[j].name))
                        # print('connected:'+str(gameWorld.connectedBubbles[i]))
                        if gameWorld.bubbleStack[j].name==str(gameWorld.connectedBubbles[i]):
                            print(gameWorld.bubbleStack[j].row)
                            print(gameWorld.bubbleStack[j].col)
                            gameScreen.bubblesOnBoard[gameWorld.bubbleStack[j].row][gameWorld.bubbleStack[j].col]=0
                            gameWorld.bubbleStack.remove(gameWorld.bubbleStack[j])
                
                gameScreen.bubblesOnBoard[self.row][self.col]=0    
                gameWorld.bubbleStack.remove(self)
                
                '''
                (7/20/2014) NOT FINISHED
                
                self.removeNotAttached()
       
                print('bubbles left:'+str(len(gameWorld.bubbleStack)))
                print(gameWorld.connectedBubbles[i])
                print('i='+str(i))
                 #   gameScreen.loadBubbles(gameScreen.bubblesOnBoard)
                '''
                
   # (7/20/2014) Need to finish. Remove unattached bubbles.  
    def removeNotAttached(self):
        '''
        for i in range(0,13):
            for j in range(0,8):
                print('remove??????')
                print(self.getValue(self.row, self.col, gameScreen.bubblesOnBoard))
                if self.getValue(i,j, gameScreen.bubblesOnBoard)>0:
                    print("000000000000000000000000000000")
                    self.attachedBubbles=[]
                    self.checkAttached(i,j,gameScreen.bubblesOnBoard)
                    if (self.attachedBubbles[0]!='attached'):
                        gameScreen.bubblesOnBoard[gameWorld.bubbleStack[j].row][gameWorld.bubbleStack[j].col]=0
                        gameWorld.bubbleStack.remove(gameWorld.bubbleStack[j])
        '''
  # (7/20/2014) Need to finish. Check if the bubble is attached.
    def checkAttached(self,row,col,bubblesOnBoard):
        
        '''
        odd = row % 2
        gameWorld.attachedBubbles.append(str(row) + "," + str(col))
        for i in range(-1,2):
            for j in range(-1,2):
                if(i!=1 or j!=1):
                    if i == 0 or j == 0 or (j == -1 and odd == 0) or (j == 1 and odd == 1):
                        if self.inRange(row + i, col + j) and self.isNewChain(row + i, col + j, bubblesOnBoard[row][col], bubblesOnBoard):
                            
                            if(row+i==0):
                                gameWorld.attachedBubbles[0]='attached'
                                
                            else:
                                self.checkAttached(row+i,col+j)
         '''  
             
    # (7/19/2014) Assign correct number in bubblesOnBoard according to the color.
    # (8/11/2014) Error occurring occasionally (depending on which color ball)
    def placeBubble(self,row,col):
    	#(8/12/2014) Thought fixing this new bug would be the same thing. Bug is still occurring "randomly"
    	self.row = int(row)
    	self.col = int(col) 
        if self.inRange(row, col):
            if self.bubbleColor==(12, 72, 237): 
                gameScreen.bubblesOnBoard[row][col]=1 
            elif self.bubbleColor== (237, 12, 34):
                gameScreen.bubblesOnBoard[row][col]=2
            elif self.bubbleColor==(0, 237, 83):
                gameScreen.bubblesOnBoard[row][col]=3
            elif self.bubbleColor==(224, 255, 51):
                gameScreen.bubblesOnBoard[row][col]=4
            elif self.bubbleColor==(255, 255, 255):
                gameScreen.bubblesOnBoard[row][col]=5
            print('(row,col)=('+str(row)+','+str(col)+')'+'; color is '+str(gameScreen.bubblesOnBoard[row][col])
                  + '; (1=BLUE,2=RED,3=GREEN,4=YELLOW,5=WHITE)')
        
                  
    ''' 
    def getChain(self, row, col):
        if self.bubbleColor==(12, 72, 237):
            gameWorld.connectedBubbles[row][col]=1 
        elif self.bubbleColor== (237, 12, 34):
            gameWorld.connectedBubbles[row][col]=2
        elif self.bubbleColor==(0, 237, 83):
            gameWorld.connectedBubbles[row][col]=3
        elif self.bubbleColor==(224, 255, 51):
            gameWorld.connectedBubbles[row][col]=4
        elif self.bubbleColor==(255, 255, 255):
            gameWorld.connectedBubbles[row][col]=5
        
        odd=row%2
        match=gameScreen.bubblesOnBoard[row][col]
        
        for i in range(-1,1):
            for j in range(-1,1):
                if (i!=0 or j!=0):
                    if (i==0 or j==0 or (j==-1 and odd==0) or (j==1 and odd==1)):
                        if (isNewChain(row+i,col+j,match)):
                            getChain(row+i,col+j);
    '''
                           
            
        
                




        
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
    delta_Time = clock.tick(60)  # 30 Frames per second? >>> (7/21/2014) change to 60
    screen.fill(backgroundColor) # Reset screen.
    gameScreen.redraw()          # Redraw screen.
    
    #(7/21/2014) Error after firing showing up here
    #(8/11/2014) Error occurring occasionally
    Bubble.move(gameWorld.bubbleStack[-1]) # (7/17/2014) call the move method in the main loop so that the bubble can keep moving
   
    
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
                print("fire")
                gameScreen.fireBubble()
                FIRE = True
                print("True")
                
                '''
                (7/17/2014) Duplicated codes. just comment it out.
                
                print("fire")
                gameScreen.fireBubble()
                FIRE = True
                print("True")
                '''
                
            elif event.key == pygame.K_LEFT: # Move cannon left.
            	print("FIRE = %f" % FIRE)
            	if FIRE == False:
            		cannon.rotateLeft(True)
            	else:
            		cannon.rotateLeft(False)
            	print("FIRE = %f" % FIRE)
            elif event.key == pygame.K_RIGHT:  # Move cannon right.
            	print("FIRE = %f" % FIRE)
            	if FIRE == False:
            		cannon.rotateRight(True)
            	else:
            		cannon.rotateRight(False)
            	print("FIRE = %f" % FIRE)
        elif event.type == KEYUP:
        	if event.key == pygame.K_UP:
        		FIRE = False
        		print("False")
        	if event.key == pygame.K_LEFT: 
        		cannon.rotateLeft(False)
        	elif event.key == pygame.K_RIGHT:
        		cannon.rotateRight(False)

    pygame.display.update()

        