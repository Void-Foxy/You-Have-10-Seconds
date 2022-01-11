#########################################
# File Name: TenSeconds
# Description: This file contain the class for the game You Have Ten Seconds
# Author: Ryan Ho
# Date: 5/30/2019
#########################################
import pygame

#---------------------------------------#
#Defining colors
#---------------------------------------#
WHITE = (255,255,255)
YELLOW = (255,255,  0)
BLUE = (  0,  0,255)
BLACK = (  0,  0,  0)
GREEN = ( 81, 255, 81)
RED = (255,  0,  0)
PINK = (255,  0,255)
LIGHT_BLUE = (170, 51,255)

class Block(object):                    
    """ A square - basic building block
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col                  
        self.row = row                  
        self.clr = clr

    def __str__(self):                  
        return "("+str(self.col)+","+str(self.row)+") "+CLR_names[self.clr]

    def draw(self, surface, gridsize):                     
        x = self.col * gridsize        
        y = self.row * gridsize
        pygame.draw.rect(surface,WHITE,(x,y,gridsize,gridsize), 0)

    def moveLeft(self):                
        self.col = self.col - 1    
        
    def moveRight(self):               
        self.col = self.col + 1   
        
    def moveDown(self):                
        self.row = self.row + 1   
        
    def moveUp(self):                  
        self.row = self.row - 1  

#---------------------------------------#
class Level(object):
    """ Collection of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        self.col = col                    
        self.row = row                   
        self.clr = 0
        self.blocks = [Block()]*blocksNo      
        self.colOffsets = [0]*blocksNo
        self.rowOffsets = [0]*blocksNo

    def update(self):
        for i in range(len(self.blocks)):
            blockCOL = self.col+self.colOffsets[i]
            blockROW = self.row+self.rowOffsets[i]
            blockCLR = self.clr
            self.blocks[i]= Block(blockCOL, blockROW, blockCLR)

    def draw(self, surface, gridsize):                     
        for block in self.blocks:
            block.draw(surface, gridsize)

    def fallingIntersection(self,player,GRIDSIZE):
        for block in self.blocks:
            if player.downY >= block.row * GRIDSIZE and player.downY <= (block.row+1) * GRIDSIZE:
                if block.col*GRIDSIZE < player.leftX and player.leftX < (block.col+1)*GRIDSIZE:
                    return True
                elif block.col*GRIDSIZE < player.rightX and player.rightX < (block.col+1)*GRIDSIZE:
                    return True
        return False
    def downBlockLocation(self,player,GRIDSIZE):
        for block in self.blocks:
            if player.downY >= block.row * GRIDSIZE and player.downY <= (block.row+1) * GRIDSIZE:
                if block.col*GRIDSIZE < player.leftX and player.leftX < (block.col+1)*GRIDSIZE:
                    return block.row * GRIDSIZE - player.size
                elif block.col*GRIDSIZE < player.rightX and player.rightX < (block.col+1)*GRIDSIZE:
                    return block.row * GRIDSIZE - player.size
    def upwardIntersection(self,player,GRIDSIZE):
        for block in self.blocks:
            if player.y < (block.row + 1) * GRIDSIZE and player.y > (block.row + 0.5) * GRIDSIZE:
                if block.col*GRIDSIZE < player.leftX and player.leftX < (block.col+1)*GRIDSIZE:
                    return True
                elif block.col*GRIDSIZE < player.rightX and player.rightX < (block.col+1)*GRIDSIZE:
                    return True
        return False
    def upBlockLocation(self,player,GRIDSIZE):
        for block in self.blocks:
            if player.y < (block.row + 1) * GRIDSIZE and player.y > (block.row + 0.5) * GRIDSIZE:
                if block.col*GRIDSIZE < player.leftX and player.leftX < (block.col+1)*GRIDSIZE:
                    return (block.row + 1) * GRIDSIZE
                elif block.col*GRIDSIZE < player.rightX and player.rightX < (block.col+1)*GRIDSIZE:
                    return (block.row + 1) * GRIDSIZE
    def leftIntersection(self,player,GRIDSIZE):
        for block in self.blocks:
            if (block.col + 1) * GRIDSIZE > player.leftX and player.leftX > (block.col + 0.5) * GRIDSIZE:
                if block.row*GRIDSIZE < player.upY and player.upY < (block.row + 1)*GRIDSIZE:
                    return True
                elif block.row*GRIDSIZE < player.downY and player.downY < (block.row+1)*GRIDSIZE:
                    return True
        return False
    def leftBlockLocation(self,player,GRIDSIZE):
        for block in self.blocks:
            if (block.col + 1) * GRIDSIZE > player.leftX and player.leftX > (block.col + 0.5) * GRIDSIZE:
                if block.row*GRIDSIZE < player.upY and player.upY < (block.row + 1)*GRIDSIZE:
                    return (block.col+1) * GRIDSIZE
                elif block.row*GRIDSIZE < player.downY and player.downY < (block.row+1)*GRIDSIZE:
                    return (block.col+1) * GRIDSIZE
        return False
    def rightIntersection(self,player,GRIDSIZE):
        for block in self.blocks:
            if block.col * GRIDSIZE <= player.rightX and player.rightX <= (block.col + 0.5) * GRIDSIZE:
                if block.row*GRIDSIZE < player.upY and player.upY < (block.row + 1)*GRIDSIZE:
                    return True
                elif block.row*GRIDSIZE < player.downY and player.downY < (block.row+1)*GRIDSIZE:
                    return True
        return False
    def rightBlockLocation(self,player,GRIDSIZE):
        for block in self.blocks:
            if block.col * GRIDSIZE <= player.rightX and player.rightX <= (block.col + 0.5) * GRIDSIZE:
                if block.row*GRIDSIZE < player.upY and player.upY < (block.row + 1)*GRIDSIZE:
                    return block.col * GRIDSIZE - player.size
                elif block.row*GRIDSIZE < player.downY and player.downY < (block.row+1)*GRIDSIZE:
                    return block.col * GRIDSIZE - player.size
        return False
    def generalIntersection(self,player,GRIDSIZE):
        if self.col * GRIDSIZE <= player.rightX and player.rightX <= (self.col + 1) * GRIDSIZE:
            if self.row * GRIDSIZE <= player.y and player.y <= (self.row + 1) *GRIDSIZE:
                return True
            if self.row * GRIDSIZE <= player.downY and player.downY <= (self.row + 1) *GRIDSIZE:
                return True
        elif self.col * GRIDSIZE <= player.x and player.x <= (self.col + 1) * GRIDSIZE:
            if self.row * GRIDSIZE <= player.y and player.y <= (self.row + 1) *GRIDSIZE:
                return True
            if self.row * GRIDSIZE <= player.downY and player.downY <= (self.row + 1) *GRIDSIZE:
                return True


#---------------------------------------#
class Flats(Level):
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Level.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self.colOffsets[i] = i
        self.update()           
            
#---------------------------------------#
class Wall(Level):
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Level.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self.rowOffsets[i] = i
        self.update()

#---------------------------------------#

class Stage(Level):
    def __init__(self,col,row):
        self.col = [col]
        self.row = [row]
        self.blocks = [Block(col,row)]
    def append(self,col,row):
        self.col.append(col)
        self.row.append(row)
        self.blocks.append(Block(col,row))
    def clear(self):
        self.col = []
        self.row = []
        self.blocks = []

#---------------------------------------#

class Door(Level):
    def __init__(self,col,row):
        self.col = col
        self.row = row
        self.levelPack = 1
        self.level = 1
    def clearCheck(self,player,GRIDSIZE):
        if self.col * GRIDSIZE <= player.rightX and player.rightX <= (self.col + 1) * GRIDSIZE:
            if (self.row - 1) * GRIDSIZE <= player.y and player.y <= (self.row + 1) *GRIDSIZE:
                return True
            if (self.row - 1) * GRIDSIZE <= player.downY and player.downY <= (self.row + 1) *GRIDSIZE:
                return True
        elif self.col * GRIDSIZE <= player.x and player.x <= (self.col + 1) * GRIDSIZE:
            if (self.row - 1) * GRIDSIZE <= player.y and player.y <= (self.row + 1) *GRIDSIZE:
                return True
            if (self.row - 1) * GRIDSIZE <= player.downY and player.downY <= (self.row + 1) *GRIDSIZE:
                return True
    def changePlace(self,col,row):
        self.col = col
        self.row = row
    def draw(self,gameWindow,GRIDSIZE,coins):
        if coins.win():
            pygame.draw.rect(gameWindow,BLUE,(self.col * GRIDSIZE, self.row * GRIDSIZE, GRIDSIZE, GRIDSIZE), 0)
            pygame.draw.ellipse(gameWindow,BLUE,(self.col * GRIDSIZE, (self.row - 1) * GRIDSIZE, GRIDSIZE, GRIDSIZE * 2), 0)
        else:
            pygame.draw.rect(gameWindow,LIGHT_BLUE,(self.col * GRIDSIZE, self.row * GRIDSIZE, GRIDSIZE, GRIDSIZE), 0)
            pygame.draw.ellipse(gameWindow,LIGHT_BLUE,(self.col * GRIDSIZE, (self.row - 1) * GRIDSIZE, GRIDSIZE, GRIDSIZE * 2), 0)
        pygame.draw.rect(gameWindow,PINK,(self.oldCol * GRIDSIZE, self.oldRow * GRIDSIZE, GRIDSIZE, GRIDSIZE), 0)
        pygame.draw.ellipse(gameWindow,PINK,(self.oldCol * GRIDSIZE, (self.oldRow - 1) * GRIDSIZE, GRIDSIZE, GRIDSIZE * 2), 0)
    def nextLevel(self):
        self.level = self.level + 1
    def oldDoor(self,col,row):
        self.oldCol = col
        self.oldRow = row

#---------------------------------------#
class Spikes(object):
    def __init__(self):
        self.col = []
        self.row = []
    def append(self,col,row):
        self.col.append(col)
        self.row.append(row)
    def generalIntersection(self,player,GRIDSIZE):
        for i in range(len(self.col)):
            if self.col[i] * GRIDSIZE < player.rightX and player.rightX < (self.col[i] + 1) * GRIDSIZE:
                if self.row[i] * GRIDSIZE < player.y and player.y < (self.row[i] + 1) *GRIDSIZE:
                    return True
                if self.row[i] * GRIDSIZE < player.downY and player.downY < (self.row[i] + 1) *GRIDSIZE:
                    return True
            elif self.col[i] * GRIDSIZE < player.x and player.x < (self.col[i] + 1) * GRIDSIZE:
                if self.row[i] * GRIDSIZE < player.y and player.y < (self.row[i] + 1) *GRIDSIZE:
                    return True
                if self.row[i] * GRIDSIZE < player.downY and player.downY < (self.row[i] + 1) *GRIDSIZE:
                    return True
    def draw(self,gameWindow,GRIDSIZE):
        for i in range(len(self.col)):
            pygame.draw.rect(gameWindow, RED, (self.col[i] * GRIDSIZE, self.row[i] * GRIDSIZE, GRIDSIZE, GRIDSIZE), 0)
    def clear(self):
        self.col = []
        self.row = []

#---------------------------------------#
class Coins(object):
    def __init__(self):
        self.col = []
        self.row = []
        self.true = []
    def append(self,col,row):
        self.col.append(col)
        self.row.append(row)
        self.true.append(True)
    def generalIntersection(self,player,GRIDSIZE):
        for i in range(len(self.col)):
            if self.col[i] * GRIDSIZE <= player.rightX and player.rightX <= (self.col[i] + 1) * GRIDSIZE:
                if self.row[i] * GRIDSIZE <= player.y and player.y <= (self.row[i] + 1) *GRIDSIZE:
                    self.true[i] = False
                    return
                if self.row[i] * GRIDSIZE <= player.downY and player.downY <= (self.row[i] + 1) *GRIDSIZE:
                    self.true[i] = False
                    return
            elif self.col[i] * GRIDSIZE <= player.x and player.x <= (self.col[i] + 1) * GRIDSIZE:
                if self.row[i] * GRIDSIZE <= player.y and player.y <= (self.row[i] + 1) *GRIDSIZE:
                    self.true[i] = False
                    return
                if self.row[i] * GRIDSIZE <= player.downY and player.downY <= (self.row[i] + 1) *GRIDSIZE:
                    self.true[i] = False
                    return
    def draw(self,gameWindow,GRIDSIZE):
        for i in range(len(self.col)):
            if self.true[i]:
                pygame.draw.rect(gameWindow, YELLOW, (self.col[i] * GRIDSIZE, self.row[i] * GRIDSIZE, GRIDSIZE, GRIDSIZE), 0)
    def clear(self):
        self.col = []
        self.row = []
        self.true = []
    def reset(self):
        for i in range(len(self.true)):
            self.true[i] = True
    def win(self):
        false = 0
        for i in range(len(self.true)):
            if not self.true[i]:
                false = false +1
        if false == len(self.true):
            return True
        else:
            return False
#---------------------------------------#
class Player(object):
    def __init__(self,GRIDSIZE):
        self.x = GRIDSIZE * 1       
        self.y = GRIDSIZE * 14
        self.size = GRIDSIZE-(GRIDSIZE/5)
        self.leftX = self.x
        self.rightX = self.x + self.size
        self.upY = self.y
        self.downY = self.y + self.size
    def update(self):
        self.leftX = self.x
        self.rightX = self.x + self.size
        self.upY = self.y
        self.downY = self.y + self.size
    def move(self):
        self.x = self.x - velocityX
        self.y = self.y - velocityY
    def draw(self,gameWindow):
        pygame.draw.rect(gameWindow, GREEN, (self.x,self.y,self.size,self.size), 0)
    def spawnSet(self,col,row,GRIDSIZE):
        self.spawnX = col * GRIDSIZE
        self.spawnY = row * GRIDSIZE
    def death(self):
        self.x = self.spawnX
        self.y = self.spawnY
