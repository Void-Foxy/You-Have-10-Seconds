#########################################
# File Name: TenSeconds
# Description: This file contain the game You Have Ten Seconds
# Author: Ryan Ho
# Date: 5/30/2019
#########################################
import pygame
import time
from TenSeconds import *
pygame.init()
WIDTH = 900
HEIGHT= 600
gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))
GRIDSIZE = 30

#---------------------------------------#
#Defining Variables
RUN_SPEED = 4
JUMP_SPEED = -8
velocityX = 0
velocityY = 0
GRAVITY = 0.3
baseLives = 5
stage = 1
stageX = []
stageY = []
levelpack = 1
level = 1
timeLimit = 10
maxlevelpack = 4
Win = False
Defeat = False
gameRun = True
Dev = False
#---------------------------------------#
#Rendering text
smallFont = pygame.font.Font("small_pixel.ttf",GRIDSIZE - (GRIDSIZE/5))
startFont = pygame.font.Font("small_pixel.ttf",50)
titleFont = pygame.font.Font("small_pixel.ttf",100)
titlePic1 = titleFont.render("YOU HAVE", 1, WHITE)
titlePic2 = titleFont.render("10 SECONDS", 1, RED)
startPic = startFont.render("PRESS SPACE TO START",1,WHITE)
levelPackPic = startFont.render(str(levelpack),1,WHITE)
defeatPic = startFont.render("YOU LOSE",1,WHITE)
winPic = startFont.render("YOU WIN!",1,WHITE)
continuePic = startFont.render("Press space to continue",1,WHITE)
#---------------------------------------#
#Defining display updates

def displayUpdate():
    gameWindow.fill(BLACK)
#Drawing borders
    rightWall.draw(gameWindow,GRIDSIZE)
    leftWall.draw(gameWindow,GRIDSIZE)
    floor.draw(gameWindow,GRIDSIZE)
    roof.draw(gameWindow,GRIDSIZE)
#Drawing the stage
    stage.draw(gameWindow,GRIDSIZE)
    door.draw(gameWindow,GRIDSIZE,coins)
    hazards.draw(gameWindow,GRIDSIZE)
    coins.draw(gameWindow,GRIDSIZE)
#Drawing the player
    player.draw(gameWindow)
#Level info
    gameWindow.blit(timePic,(WIDTH/2-GRIDSIZE,GRIDSIZE/10))
    gameWindow.blit(lifePic,(WIDTH - (GRIDSIZE * 4),HEIGHT - (GRIDSIZE/10 * 9)))
    gameWindow.blit(levelInfoPic,(GRIDSIZE/5,HEIGHT - GRIDSIZE))
    pygame.display.update()

#Drawing main menu
def mainMenuUpdate():
    gameWindow.fill(BLACK)
    gameWindow.blit(titlePic1,(WIDTH/8,HEIGHT/10))
    gameWindow.blit(titlePic2,(WIDTH/5,(HEIGHT/10) + 100))
    gameWindow.blit(startPic,(WIDTH/8,HEIGHT/3 * 2))
    gameWindow.blit(levelPackPic,(WIDTH/2,HEIGHT/3 * 2 + 50))
    pygame.display.update()

#Drawing the win screen
def drawWin():
    gameWindow.fill(BLACK)
    gameWindow.blit(winPic,(WIDTH/8,HEIGHT/10))
    gameWindow.blit(continuePic,(WIDTH/8,HEIGHT/3 * 2))
    gameWindow.blit(scorePic,(WIDTH/2,HEIGHT/3 * 2 + 50))
    pygame.display.update()

#Drawing the defeat screen
def drawDefeat():
    gameWindow.fill(BLACK)
    gameWindow.blit(defeatPic,(WIDTH/8,HEIGHT/10))
    gameWindow.blit(continuePic,(WIDTH/8,HEIGHT/3 * 2))
    gameWindow.blit(scorePic,(WIDTH/2,HEIGHT/3 * 2 + 50))
    pygame.display.update()

#---------------------------------------#
#setting classes
leftWall = Wall(0,0,HEIGHT/GRIDSIZE)
rightWall = Wall(WIDTH/GRIDSIZE - 1,0,HEIGHT/GRIDSIZE)
floor = Flats(0,HEIGHT/GRIDSIZE-1,WIDTH/GRIDSIZE)
roof = Flats(0,0,WIDTH/GRIDSIZE)
player = Player(GRIDSIZE)
stage = Stage(0,0)
door = Door(17,13)
hazards = Spikes()
coins = Coins()

#giving basic instructions
print "Use left and right arrow keys to move or change level pack"
print "Up arrow Key to jump"
print "Space to continue"
print "Press d to activate infinite lives"

while gameRun:
    inPlay = True
    mainMenu = True
    while mainMenu:
        levelPackPic = startFont.render("<Level Pack " + str(levelpack) + ">",1,WHITE)
        pygame.event.clear()
        mainMenuUpdate()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                #testing for interactions in the main menu
                if event.key == pygame.K_ESCAPE:
                    inPlay = False
                    mainMenu = False
                    gameRun = False
                if event.key == pygame.K_SPACE:
                    mainMenu = False
                if event.key == pygame.K_LEFT:
                    levelpack = levelpack - 1
                if event.key == pygame.K_RIGHT:
                    levelpack = levelpack + 1
                if event.key == pygame.K_d:
                #inverses Dev mode
                    if Dev:
                        Dev = False
                    else:
                        Dev = True
                if levelpack <= 0:
                    levelpack = maxlevelpack
                if levelpack >= maxlevelpack + 1:
                    levelpack = 1

    #Getting and mapsing the stage
    level = 1
    maps =  pygame.image.load('Level Pack ' + str(levelpack) + '/Level ' + str(level) + '.png')
    #Clearing the stage and hazards
    stage.clear()
    hazards.clear()
    coins.clear()
    for x in range(1,WIDTH/GRIDSIZE - 1):
        for y in range(1,HEIGHT/GRIDSIZE - 1):
            if maps.get_at((x,y)) == BLACK:
                stage.append(x,y)
            if maps.get_at((x,y)) == RED:
                hazards.append(x,y)
            if maps.get_at((x,y)) == BLUE:
                door.changePlace(x,y)
            if maps.get_at((x,y)) == PINK:
                player.spawnSet(x,y,GRIDSIZE)
                door.oldDoor(x,y)
            if maps.get_at((x,y)) == YELLOW:
                coins.append(x,y)

    #Getting the level title
    levelFile = 'Level Pack ' + str(levelpack) + '/Level ' + str(level) + '.txt'
    fileIn = open(levelFile)
    data = fileIn.read()
    fileIn.close()
    levelInfo = ""

    levelInfo = levelInfo + str(data)
    levelInfoPic = smallFont.render(levelInfo,1,BLACK)

    player.death()        #Reseting the player to spawn
    lives = baseLives     #Reseting the players lives
    score = 0             #Resting the Score

    startTime = time.time()     #Starting the stopwatch

    #Rendering the time and lives
    timeLeft = startTime + timeLimit - time.time()
    timePic = smallFont.render(str(round(timeLeft)), 1, BLACK)
    lifePic = smallFont.render("Lives:" + str(lives), 1, BLACK)

    while inPlay:
        pygame.event.clear()
        displayUpdate()

    # tests for key presses
        pygame.event.get()                  
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            inPlay = False
            
    # set horizontal and vertical velocity
        if keys[pygame.K_UP] and onGround:
            velocityY = JUMP_SPEED
        if keys[pygame.K_LEFT]:
            velocityX = -RUN_SPEED
        elif keys[pygame.K_RIGHT]:
            velocityX = RUN_SPEED
        else:
            velocityX = 0
    # move the object in horizontal direction
        player.x = player.x + velocityX
        player.update()
        if stage.leftIntersection(player,GRIDSIZE):
            player.x = stage.leftBlockLocation(player,GRIDSIZE)
            player.update()
        elif stage.rightIntersection(player,GRIDSIZE):
            player.x = stage.rightBlockLocation(player,GRIDSIZE)
            player.update()
        elif leftWall.leftIntersection(player,GRIDSIZE):
            player.x = leftWall.leftBlockLocation(player,GRIDSIZE)
            player.update()
        elif rightWall.rightIntersection(player,GRIDSIZE):
            player.x = rightWall.rightBlockLocation(player,GRIDSIZE)
            player.update()
        if velocityY < 10:                                      # update object's vertical velocity
            velocityY = velocityY + GRAVITY
    # move the object in vertical direction    
        player.y = player.y + velocityY
        player.update()
        if stage.fallingIntersection(player,GRIDSIZE):          #testing for if the player is in/on the the floor
            player.y = stage.downBlockLocation(player,GRIDSIZE) #changing the loction of the player to be on top of the block and not in the block
            velocityY = 0
            onGround = True
            player.update()
        elif stage.upwardIntersection(player,GRIDSIZE):          #testing for if the player is in/on the the roof
            player.y = stage.upBlockLocation(player,GRIDSIZE)    #changing the loction of the player to be on top of the block and not in the block
            velocityY = 0
            player.update()
        elif floor.fallingIntersection(player,GRIDSIZE):          #testing for if the player is in/on the the floor
            player.y = floor.downBlockLocation(player,GRIDSIZE) #changing the loction of the player to be on top of the block and not in the block
            velocityY = 0
            onGround = True
            player.update()
        elif roof.upwardIntersection(player,GRIDSIZE):          #testing for if the player is in/on the the roof
            player.y = roof.upBlockLocation(player,GRIDSIZE)    #changing the loction of the player to be on top of the block and not in the block
            velocityY = 0
            player.update()

        else:
            onGround = False
        coins.generalIntersection(player,GRIDSIZE) # testing if the player collected a coin
        if onGround:
            velocityY = 0

        if door.clearCheck(player,GRIDSIZE) and coins.win():    #Checking the level clear condistion
            level = level + 1
            if level > 10:  #has the player reached the max level
                inPlay = False
                score = score + ((startTime + timeLimit - time.time()) * 10)
                score = score + (lives * 100)
                print round(score)
                Win = True
                score = round(score,1)
            elif levelpack == 4 and level > 4:#level pack 4 has a seperate amount of levels
                inPlay = False
                score = score + ((startTime + timeLimit - time.time()) * 10)
                score = score + (lives * 100)
                print round(score)
                Win = True
                score = round(score,1)
            else:   #import the next stage
                stage.clear()
                hazards.clear()
                coins.clear()
                maps =  pygame.image.load('Level Pack ' + str(levelpack) + '/Level ' + str(level) + '.png')
                for x in range(1,WIDTH/GRIDSIZE - 1):
                    for y in range(1,HEIGHT/GRIDSIZE - 1):
                        if maps.get_at((x,y)) == BLACK:
                            stage.append(x,y)
                        if maps.get_at((x,y)) == RED:
                            hazards.append(x,y)
                        if maps.get_at((x,y)) == BLUE:
                            door.changePlace(x,y)
                        if maps.get_at((x,y)) == PINK:
                            player.spawnSet(x,y,GRIDSIZE)
                            door.oldDoor(x,y)
                        if maps.get_at((x,y)) == YELLOW:
                            coins.append(x,y)
                levelFile = 'Level Pack ' + str(levelpack) + '/Level ' + str(level) + '.txt'
                fileIn = open(levelFile)
                data = fileIn.read()
                fileIn.close()
                levelInfo = ""
                levelInfo = levelInfo + str(data)
                levelInfoPic = smallFont.render(levelInfo,1,BLACK)
                score = score + ((startTime + timeLimit - time.time()) * 10)
                print round(score)
                startTime = time.time() #reset the timer
        #testing for player death
        if hazards.generalIntersection(player,GRIDSIZE) or startTime + timeLimit <= time.time():
            player.death()
            if not Dev:
                lives = lives - 1
                coins.reset()
            lifePic = smallFont.render("Lives:" + str(lives), 1, BLACK)
            startTime = time.time()
        if lives <= 0:
            inPlay = False
            Defeat = True
        timeLeft = startTime + timeLimit - time.time()
        timePic = smallFont.render(str(round(timeLeft,2)), 1, BLACK)
        pygame.time.delay(10)
    scorePic = startFont.render("Score: " + str(score),1,WHITE)
    #win/lost screens
    while Win:
        drawWin()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Win = False
    while Defeat:
        drawDefeat()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Defeat = False
    
pygame.quit()
