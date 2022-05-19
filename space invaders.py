import pygame
import random
import math
from pygame import mixer

#you need to type pygame.init() before your code, for it to work

pygame.init()

#the code below makes a screen for the game to show up in 
#we named the variable "screen"
#after the "display.set_mode", you must add two pair of parentheses for it to work.
#inside the inner pair of parentheses, you type the width and height of your screen in pixels.
screen= pygame.display.set_mode((800,600))


#Background
background=pygame.image.load("D:/Projects/Python/Tutorial/freecodecamp/Pygame/Space Invaders/background.png")

#Background Music
mixer.music.load("D:/Projects/Python/Tutorial/freecodecamp/Pygame/Space Invaders/background.wav")
#putting -1 in the parenthesis below makes sure the music repeats itself after playing, not putting anything in the parenthesis means that the musics will only play once.
mixer.music.play(-1)

#Title & Icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load("D:/Projects/Python/Tutorial/freecodecamp/Pygame/Space Invaders/alien.png")
pygame.display.set_icon(icon)


#Player
PlayerImg=pygame.image.load("D:/Projects/Python/Tutorial/freecodecamp/Pygame/Space Invaders/space.png")
playerX= 365
playerY= 400

playerX_change=0
playerY_change=0


#Enemy
EnemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]

num_of_enemeies=4

for i in range(num_of_enemeies):
    EnemyImg.append(pygame.image.load("D:/Projects/Python/Tutorial/freecodecamp/Pygame/Space Invaders/planet.png"))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))

    enemyX_change.append(3)
    enemyY_change.append(10)


#Bullet
#Ready- you can't see the bullet
#Fire- you can see the bullet moving
BulletImg=pygame.image.load("D:/Projects/Python/Tutorial/freecodecamp/Pygame/Space Invaders/bullets.png")
bulletX= 0
bulletY= 0

bulletX_change=0
bulletY_change=9
bullet_state="ready"

#Score
#making a text on the screen to show the score of the playes

score_value=0

#first we type the name of the font and the size of it in pixels
font=pygame.font.Font('freesansbold.ttf', 32)

#now we say were the text is to be shown on the screen
textX=10
textY=10

#Game Over text

over_font=pygame.font.Font('freesansbold.ttf', 64)


#In the function below, .blit draws what we want (the player icon) on the surface (aka. our screen).
#This function needs to be called in the while loop so it doesn't disappear, it also needs to be called after the "screen.fill" because the screen needs to be drawn first.
def player(x,y):
    screen.blit(PlayerImg, (x, y))


def enemy(x,y, i):
        screen.blit(EnemyImg[i], (x, y))


#to show a text you need to use the ".render" keyword before of ".blit"
#the very last parenthesis has the RGB values of the color white.
def show_score(x,y):
    score= font.render("SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))


def game_over_text():
    over_text= over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200,250))


def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(BulletImg, (x+16, y+10))


def IsCollision(enemyX, enemyY, bulletX, bulletY):

    distance=math.sqrt(math.pow((enemyX-bulletX),2)+math.pow((enemyY-bulletY),2))

    if distance <=27:
        return True




#Game loop
#now we make a loop so that the screen stays open 'till we press the close button.
#any kind of thing that happens in the game when you press a key (like closing the game) is callned an "event"
#for example pressing a key to move in the game is an event.
#anything that you want to stay persistently inside the game must be written inside this while loop.

running=True
while running:

    #we use the scree.fill code to change the appearance of the screen.
    #you type two pair of parentheses after the code, and inside the second pair type the RGB values of the color you want.
    screen.fill((30,30,90))

    #now we add the background with coordinates we want the image to start from
    screen.blit(background,(0,0))

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
                running=False

        #now we want to check which keystroke is being pressed on the keyboard to move the player image accordingly.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change= -4

            if event.key == pygame.K_RIGHT:
                playerX_change= +4

            if event.key == pygame.K_UP:
                playerY_change= -4

            if event.key == pygame.K_DOWN:
                playerY_change= 4
            

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":

                    bullet_sound= mixer.Sound("D:/Projects/Python/Tutorial/freecodecamp/Pygame/Space Invaders/laser.wav")
                    bullet_sound.play()

                    bulletX=playerX
                    bulletY=playerY
                    fire_bullet(bulletX,bulletY)



        #here we check which keystroke is not being pressed anymore, so we'ld be able to stop the movement.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change= 0

            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change= 0


    #player's movement
    playerX +=playerX_change
    playerY +=playerY_change

    #adding boundries so the player doesn't get out of the screen.
    if playerX <=0:
        playerX=0

    #we type 736, because the player is 64 pixels and the screen width is 800 so: 800-64=736
    elif playerX >=736:
        playerX=736

    if playerY <=450:
        playerY=450

    elif playerY >=536:
        playerY=536




    #enemy's movement
    for i in range(num_of_enemeies):

        #Game Over
        if enemyY[i] >425:

            for j in range(num_of_enemeies):
                #we type 2000 to make sure all the enemies will be out of view when the game is over
                enemyY[j]=2000
            game_over_text()
            break



        enemyX[i] +=enemyX_change[i]

        if enemyX[i] <=0:
            enemyX_change[i]= 3
            enemyY[i] +=enemyY_change[i]


        elif enemyX[i] >=736:
            enemyX_change[i]= -3
            enemyY[i] +=enemyY_change[i]

        #Collision

        collision=IsCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound= mixer.Sound("D:/Projects/Python/Tutorial/freecodecamp/Pygame/Space Invaders/explosion.wav")
            explosion_sound.play()
            bulletY=playerY
            bullet_state="ready"
            score_value +=1

            enemyX[i]= random.randint(0,736)
            enemyY[i]= random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i], i)

    #bullet movement
    
    if bulletY <=0:
        bulletY=playerY
        bullet_state="ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -=bulletY_change


    show_score(textX,textY)
    player(playerX,playerY)
    #you always need to type the update code (as seen below), so the screen gets what you've added to it.
    pygame.display.update()