import pygame, sys, math
from pygame.locals import *
from random import randrange
from math import *

ROTATION_SPEED = 1
RADIUS = 18
DISTANCE = RADIUS * sqrt(3) 
ROWS = 14
COLUMNS_ODD = 7
COLUMNS_EVEN = 8
TOTAL_COLUMNS = COLUMNS_ODD + COLUMNS_EVEN
screenX, screenY = 640, 480
DEG_TO_RAD = 0.0174532925


BUBBLE_SPEED=10
pointsForConnection=100 # 100 points for each bubble

# CLASS GAMEWORLD: Holds the values of the ongoing game including the current level, timer, score.
# Class currently is not being fully utilized. A temporary "test" level is being used in the GameScreen class.
class GameWorld:

    def __init__(self):
        self.bubbleStack = []
        self.connectedBubbles = [[]] 
        self.attachedBubbles = [[]]
        self.vX = 0 # Velocity of X direction. NEITHER BEING USED
        self.vY = 0 # Velocity of Y direction.

    score = 0
    gameOver = '' # WIN or LOST
    GAME_OVER = False # is the game over?
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
        '''bubblesOnBoard = [   [1, 0, 0, 4, 0, 0, 3, 5],  # DEFAULT: Level 1 Test
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
                            [0, 0, 0, 0, 0, 0, 0]]'''
        bubblesOnBoard = [   [0, 0, 0, 0, 0, 0, 0, 0],	# Level with random bubbles
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
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
        for r in range(8):
        	if r%2 == 0:
        		for c in range(COLUMNS_EVEN):
        			bubblesOnBoard[r][c] = randrange(1,6)
        	else:
        		for c in range(COLUMNS_ODD):
        			bubblesOnBoard[r][c] = randrange(1,6)
        self.loadBubbles(bubblesOnBoard) # Load board bubbles.

    def borderLine(self):
        # borderLine: Draws right line indicating the right edge of the GameScreen.   
        self.lineColor = (250, 250, 250) # WHITE
        self.borderX = RADIUS + RADIUS * TOTAL_COLUMNS # Total columns times radius of bubble plus radius for offset.
        self.borderY = screenY
        pygame.draw.line(screen, self.lineColor, (self.borderX, 0), (self.borderX, screenY), 5) # Thinking about changing this somehow. Make it more general.

    def drawBubbles(self):
        for index, bubble in enumerate(gameWorld.bubbleStack):

            if (bubble.move): 
                self.bubblesParked = False # Determines if all of the bubbles are stopped.
        
            pygame.draw.circle(screen, bubble.bubbleColor, (int(bubble.posX), int(bubble.posY)), RADIUS) # (7/17/2014) cast posX, posY to int to avoid the error    

    def fireBubble(self):
        # fireBubble: calculate and set the x and y velocity
        print("FIRE BUBBLE")
        if(not self.bubblesParked):
            if(gameWorld.bubbleStack[-1].velY==0):
                gameWorld.bubbleStack[-1].velX = BUBBLE_SPEED * math.cos(self.cannon.angle) # set x velocity
                gameWorld.bubbleStack[-1].velY = -BUBBLE_SPEED * math.sin(self.cannon.angle) # set y velocity
            
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
                    if(row < 14 and self.bubblesOnBoard[row][col] > 0): # If inbounds and the bubble exists (>0).
                        bubble = Bubble(bubblesOnBoard[row][col], row, col)
                        gameWorld.bubbleStack.append(bubble)
                        gameWorld.connectedBubbles = []  # Reset list to find new bubble chains. (6/25/14) This and below line can be turned into new chain method.
                        Bubble.checkBubbleChain(bubble, row, col, bubblesOnBoard)
                       
                # If it's odd row: start grid slightly offset of left side of screen.
                else:
                    if(col < COLUMNS_ODD):
                        if(row < 14 and self.bubblesOnBoard[row][col] > 0): # If inbounds and the bubble exists (>0).
                            bubble = Bubble(bubblesOnBoard[row][col], row, col)
                            gameWorld.bubbleStack.append(bubble)
                            gameWorld.connectedBubbles = []  # Reset list to find new bubble chains. (6/25/14) This and below line can be turned into new chain method.
                            Bubble.checkBubbleChain(bubble, row, col, bubblesOnBoard)
       
                           

    def redraw(self):
        # redraw: Called by main game loop. Updates the gameScreen's borderLine, bubbles, and cannon.
        self.borderLine()
        self.drawBubbles()
        cannon.redraw()
        self.isWinning()
    
    def isWinning(self):
        if len(gameWorld.bubbleStack)==1:
            gameWorld.GAME_OVER=True
            gameWorld.gameOver='WIN'
                    
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
            
    def rotateLeft(self, move):
        # rotateLeft: Rotate the cannon to the left at current ROTATION_SPEED.
        if(move and self.startRadian < self.maxLeft):
            self.startRadian += ROTATION_SPEED*DEG_TO_RAD
            self.endRadian += ROTATION_SPEED*DEG_TO_RAD
            self.angle += DEG_TO_RAD
        else:
            return
    
    def rotateRight(self, move):
        # rotateRight: Rotate the cannon to the right at current ROTATION_SPEED.
        if(move and self.startRadian > self.maxRight):
            self.startRadian -= ROTATION_SPEED*DEG_TO_RAD
            self.endRadian -= ROTATION_SPEED*DEG_TO_RAD
            self.angle -= DEG_TO_RAD
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
        
        self.velX=0
        self.velY=0
        self.name=str(row)+','+str(col)

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
        if self.inRange(row, col)==False: # check if the row and col valid
            return False
        valuesMatch = val == self.getValue(row, col, bubblesOnBoard) # Check same color.
        if str(row) + "," + str(col) in gameWorld.connectedBubbles: # Check if visited.
            alreadyVisited = True
        else:
            alreadyVisited = False
        return (alreadyVisited == False) and valuesMatch
       
    def move(self):
		#Move the bubble after firing, check collisions with walls and top 
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
                    self.parkBubble() 

    def parkBubble(self):
        # parkBubble: calculate and set the position where the bubble should park
        print('Bubble Parked')  
        
        row=math.floor(self.posY/DISTANCE) 
        col=0
        
        #depending on the row changes the way the column is calculated
        if row%2==0:
            col=math.floor(self.posX/(2*RADIUS))
        else:
            col=math.floor((self.posX-RADIUS)/(2*RADIUS))
            
    	row = int(row)
        col = int(col)
    	
        if self.inRange(row, col)==False:
            if row>=13:
                gameWorld.GAME_OVER = True
                gameWorld.gameOver = 'LOST'
        else: 
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
            self.row=row
            self.col=col
            self.move=False
            gameScreen.bubblesParked=True
            self.placeBubble(row,col)
        
                      
            # gameScreen.loadBubbles(gameScreen.bubblesOnBoard)
            if self.inRange(row , col ):
                self.checkBubbleChain(row, col, gameScreen.bubblesOnBoard)
                print("chain = "+str(len(gameWorld.connectedBubbles)))
            
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
                         #   print(gameWorld.bubbleStack[j].row)
                         #   print(gameWorld.bubbleStack[j].col)
                            gameScreen.bubblesOnBoard[gameWorld.bubbleStack[j].row][gameWorld.bubbleStack[j].col]=0
                            gameWorld.bubbleStack.remove(gameWorld.bubbleStack[j])
                
                gameScreen.bubblesOnBoard[self.row][self.col]=0    
                gameWorld.bubbleStack.remove(self)

                print('====Start checking whether the bubble is attached to the grid==============')
                
                self.removeNotAttached()
         
                

    
    def removeNotAttached(self):
        # removeNotAttached: remove the bubble which is not attached to the grid
        for i in range(1,13):
            for j in range(0,8):
                if self.getValue(i,j, gameScreen.bubblesOnBoard)>0:
                    print("checking: "+str(i)+","+str(j))
                    gameWorld.attachedBubbles=[]
                    self.checkAttached(i, j, gameScreen.bubblesOnBoard)
                    if(gameWorld.attachedBubbles[0]!='attached'):
                        self.removeByName(str(i)+","+str(j))
                        print("remove: "+str(i)+","+str(j))
                        if(gameScreen.bubblesOnBoard[i][j]!=0):
                            print("Fail to remove!!!! =========================!!!")
    
   
    def removeByName(self,name):
        # removeByName: remove the bubble by its name
        for j in range(0,len(gameWorld.bubbleStack)):
         #   print(gameWorld.bubbleStack[j].name+" =? "+name)
            if gameWorld.bubbleStack[j].name==name:
                gameScreen.bubblesOnBoard[gameWorld.bubbleStack[j].row][gameWorld.bubbleStack[j].col]=0
                gameWorld.bubbleStack.remove(gameWorld.bubbleStack[j])
                gameWorld.score+=pointsForConnection
                break
      
    def isNewConnection(self,row,col, bubblesOnBoard):
        # isNewConnection: return True if the bubble has not been visited
        if self.getValue(row, col, bubblesOnBoard)<1:
            return False
        if str(row) + "," + str(col) in gameWorld.attachedBubbles: # Check if visited.
            alreadyVisited = True
      #      print("visited: "+ str(row)+','+str(col) )
        else:
            alreadyVisited = False
        return (alreadyVisited == False)
    

    def checkAttached(self,row,col,bubblesOnBoard):
        # checkAttached: mark the bubble if the bubble is attached to the grid
        if row<0 or col<0:
            return
        if self.inRange(row , col)==False:
            return
        odd = row % 2
        gameWorld.attachedBubbles.append(str(row) + "," + str(col))
        for i in range(-1,2):
            for j in range(-1,2):
                if(i!=0 or j!=0):
                    if i == 0 or j == 0 or (j == -1 and odd == 0) or (j == 1 and odd == 1):
                        if self.isNewConnection(row+i, col+j, bubblesOnBoard):
                            if(row+i==0):
                           #     print('mark as attached: '+str(row)+","+str(col))   
                                gameWorld.attachedBubbles[0]='attached'
                            else:
                                self.checkAttached(row+i,col+j, bubblesOnBoard)    
        
    def placeBubble(self,row,col): 
        # placeBubble: Assign color value in bubblesOnBoard according to the color.
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
FIRE = True
TIME = True
while gameRunning:
    delta_Time = clock.tick(55)  # FPS
    screen.fill(backgroundColor) # Reset screen.
    gameScreen.redraw()          # Redraw screen.
    
    if(TIME == True):
    	seconds = pygame.time.get_ticks()/1000
    
    Bubble.move(gameWorld.bubbleStack[-1]) # call the move method in the main loop so that the bubble can keep moving
    
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
            
        if gameWorld.GAME_OVER == True:
    		FIRE = False
    		TIME = False
            
        elif event.type == KEYDOWN:
            if (event.key == pygame.K_UP) & FIRE == True:  # Fire a bubble.
                gameScreen.fireBubble()              
            elif event.key == pygame.K_LEFT: # Move cannon left.
            	cannon.rotateLeft(True)
            elif event.key == pygame.K_RIGHT:  # Move cannon right.
            	cannon.rotateRight(True)
            	
        elif event.type == KEYUP:
        	if event.key == pygame.K_LEFT: 
        		cannon.rotateLeft(False)
        	elif event.key == pygame.K_RIGHT:
        		cannon.rotateRight(False)
        
    # display the score  
    if pygame.font:
        font = pygame.font.Font(None, 26)
        text = font.render("Score: %d " % gameWorld.score, True,(255,0,0))
        textpos = text.get_rect(centerx=screen.get_width()/2 + 100)
        screen.blit(text, textpos)
        
    if pygame.font:
        font = pygame.font.Font(None, 26)
        text = font.render("Time: %d " % seconds, True,(255,0,0))
        textpos = text.get_rect(centerx=screen.get_width()/2 + 225)
        screen.blit(text, textpos)

    if pygame.font:
        font = pygame.font.Font(None, 26)
        text = font.render("Game Over: "+gameWorld.gameOver, True,(255,0,0))
        if gameWorld.GAME_OVER == True:
            screen.blit(text, (screen.get_width()/2,100))
	
    pygame.display.update()