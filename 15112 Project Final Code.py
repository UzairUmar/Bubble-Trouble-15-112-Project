#Name: Uzair Umar
#Andrew ID: mumar
#Milestone 2 code
import pygame,sys              #sys library used when quitting the program
from random import randint
pygame.init()
win = pygame.display.set_mode((688,366))
pygame.display.set_caption("Bubble Trouble")

black=[0,0,0]
white=[255,255,255]
skin = [254,168,119]
grey = (200, 200, 200)
font=pygame.font.Font(None,45)
pygame.display.set_caption("Bubble Trouble")
bg = pygame.image.load('level1.jpg')
player = pygame.image.load('player.png')
playerLeft= pygame.image.load('left.png')
player2 = pygame.image.load('player2.png')
player2Left = pygame.image.load('player2 left.png')
bonusLife = pygame.image.load('bonusLife.png')
bonusLife = pygame.transform.scale(bonusLife,(20,18))
bonusTime = pygame.image.load('bonus time.png')
controlScreen = pygame.image.load('controlz.jpg')
controlScreen = pygame.transform.scale(controlScreen,(688,366))
walkRight = [pygame.transform.flip(playerLeft,30,0)] #flipping image to make in useful for right movement
walkLeft = [playerLeft]
walkRight2 =  [pygame.transform.flip(player2Left,30,0)]  #Image to show Right movement of Player 2
walkLeft2 = [player2Left]
PlayTime= 60    #time limit for level 1
totalLives = 3      #total Lives for players
totalLives2 = 3
hitCount=0
ScoreCount = 0
pos = 0 #getting position of mouse
bonusCount = 0 #keeping track of Bonus Drops
index = 0 #keeping track of Big bubble List index
ballList= []        #list to keep track of Big bubbles
bubbleList = []     #list to keep track of small bubbles
bonusList= []       #list to keep track of Bonus Drops
bonusActive=False
start_timer = False
multiplayer = False
bonusDrop = False
lifeImage = pygame.transform.scale(player, (20,20)) #transforming player image to display as a life
lifeImage2 =  pygame.transform.scale(player2, (20,20))
ball=pygame.image.load('rball4.png')
small = pygame.transform.scale(ball,(20,20))

clock = pygame.time.Clock()

class Player:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=3
        self.left=False
        self.right=False
        self.walkCount=0
        self.hitbox = (self.x,self.y,23,37)
    def shoot(self):
        self.is_active = True
        weapon.update()

    def draw(self,win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft[0], (self.x,self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[0], (self.x,self.y))
            self.walkCount +=1
        else:
            win.blit(player, (self.x,self.y))
        self.hitbox = (self.x,self.y,23,37)
        #pygame.draw.rect(win,[255,0,0],self.hitbox,2)

    def draw2(self,win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft2[0], (self.x,self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight2[0], (self.x,self.y))
            self.walkCount +=1
        else:
            win.blit(player2, (self.x,self.y))
        self.hitbox = (self.x,self.y,23,37)
        #pygame.draw.rect(win,[255,0,0],self.hitbox,2)

    def hit(self):      #Hitbox Code
        if(totalLives == 0 or totalLives2 == 0):
            font=pygame.font.Font(None,45)
            gameOver = font.render("GameOver", 1 ,(0,0,0))
            win.blit(gameOver, (280,150))
            pygame.display.update()
            i = 0
            while i < 300:
                pygame.time.delay(1000)
                i +=1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 301
                        pygame.quit()
        else:
            font=pygame.font.Font(None,45)
            PlayerHit = font.render("You Got Hit", 1 ,(0,0,0))
            win.blit(PlayerHit,(300,150))
            pygame.display.update()
            self.x = 329
            self.y = 329
            bubble.pos_y= 150
            bubble1.pos_y = 150
            for i in bubbleList:
                i.pos_y = 150
            self.walkCount = 0
            i = 0
            while i < 300:
                pygame.time.delay(10)
                i +=1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 301
                        pygame.quit()
        

class Weapon:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.vel=10
        self.hitbox1 = (self.x+10,self.y,4,300)
    def draw(self,win):
        pygame.draw.line(win,black,(self.x+10,self.y),(self.x+10,self.y+300),4)     #drawing line as a weapon
        self.hitbox1 = (self.x+9,self.y,2,300) #Hitbox Code
        #pygame.draw.rect(win,[255,255,255],self.hitbox1,2)   #Hitbox Code
class Timer:                #class to get and display time
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def draw_timer(self,win):
        CurrentTime=pygame.time.get_ticks()
        CurrentTime = CurrentTime / 1000    #coverting milliseconds to seconds
        time_left = PlayTime - CurrentTime
        time_left= int(time_left)
        font=pygame.font.Font(None,36)
        text=font.render("Time Left:" + str(time_left) ,1,black)
        win.blit(text,(self.x,self.y))
        if (time_left == 0):
            font=pygame.font.Font(None,45)
            PlayerHit = font.render("You Ran Out of Time! Game Over", 1 ,(0,0,0))
            win.blit(PlayerHit,(150,150))
            pygame.display.update()
            i = 0
            while i < 300:
                pygame.time.delay(1000)
                i +=1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        i = 301
                        pygame.quit()

class lives:
    def __init__(self,x,y,totalLives):
        self.x= x
        self.y = y
        self.totalLives = totalLives
    def drawlives(self,win,totalLives):
        for i in range(totalLives):
            life_rect= lifeImage.get_rect()
            life_rect.x = self.x+ 30 * i
            life_rect.y = self.y
            win.blit(lifeImage,life_rect)
    def drawlives2(self,win,totalLives2):           #Function to show lives for Player 2
         for i in range(totalLives2):
            life_rect= lifeImage2.get_rect()
            life_rect.x = self.x+ 30 * i
            life_rect.y = self.y
            win.blit(lifeImage2,life_rect)

class Bubble:
    def __init__(self,pos_x,pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.spd_x = 3
        self.spd_y = 3
        self.visible= True
        self.visible1 = False
        self.hitbox = (self.pos_x,self.pos_y,58,58)
    def drawBubble(self,win):
        if self.visible:
            win.blit(ball,(self.pos_x,self.pos_y)) #displaying bubble image on screen

            self.pos_x+= self.spd_x
            self.pos_y+= self.spd_y

            if(self.pos_y > 310 or self.pos_y < 0):             #checking if bubble hits borders of screen
                self.spd_y= self.spd_y * -1
            if self.pos_x > 630 or self.pos_x < 10:
                self.spd_x = self.spd_x * -1
            self.hitbox = (self.pos_x+2,self.pos_y+2,53,53) #Hitbox Code
            #pygame.draw.rect(win,[255,0,0],self.hitbox,2)
        elif self.visible1:
               bubbleList.append(
               smallBubble(self.pos_x-20,self.pos_y,self.visible1))
               bubbleList.append(
                   smallBubble(self.pos_x+20,self.pos_y,self.visible1))
               self.visible1 = False    #making sure balls are appended only once to the list
               ballList.pop(ballList.index(index))
               

    def bubbleHit(self):
                global ScoreCount,index
                ScoreCount+=1
                if len(arrow) == 1:
                    arrow.pop(arrow.index(i))
                
                if ScoreCount ==3:
                    bonusList.append(
                        dropBonus(self.pos_x,self.pos_y,bonusLife))
                if ScoreCount ==5:
                    bonusList.append(
                        dropBonus(self.pos_x,self.pos_y,bonusTime))
                self.visible=False
                self.visible1 = True

    def bubbleHit2(self):               #Fucntion that executes when Player 2 gets hitby the bubble
        global ScoreCount
        ScoreCount+=1
        if len(arrow2) == 1:
            arrow2.pop(arrow2.index(i))
        
        if ScoreCount ==3:
            bonusList.append(
                dropBonus(self.pos_x,self.pos_y,bonusLife))
        if ScoreCount ==5:
            bonusList.append(
                dropBonus(self.pos_x,self.pos_y,bonusTime))
        self.visible=False
        self.visible1 = True
        

class smallBubble:                                              #class to show implementation of Small bubbles
    def __init__(self,pos_x,pos_y,visible1):
        self.pos_x = pos_x + 20
        self.pos_y = pos_y
        self.spd_x = 3
        self.spd_y = 3
        self.visible1= visible1
        self.hitbox = (self.pos_x,self.pos_y,20,20)

    def drawSmall(self,win):
        if self.visible1:
            win.blit(small,(self.pos_x,self.pos_y))  #displaying bubble image on screen

            self.pos_x+= self.spd_x
            self.pos_y+= self.spd_y

            if(self.pos_y > 348 or self.pos_y < 0):             #checking if bubble hits borders of screen
                self.spd_y= self.spd_y * -1
            if self.pos_x > 670 or self.pos_x < 5:
                self.spd_x = self.spd_x * -1
            self.hitbox = (self.pos_x,self.pos_y,20,20)
            #pygame.draw.rect(win,[255,0,0],self.hitbox,2)

    def smallBubbleHit(self):
                global ScoreCount
                ScoreCount+=1
                if len(arrow) == 1:
                    arrow.pop(arrow.index(i))
                
                if ScoreCount ==3:
                    bonusList.append(
                        dropBonus(self.pos_x,self.pos_y,bonusLife))
                if ScoreCount == 5:
                    bonusList.append(
                    dropBonus(self.pos_x,self.pos_y,bonusTime))
                self.visible1=False
                bubbleList.pop(bubbleList.index(a))

    def smallBubbleHit2(self):
        global ScoreCount
        ScoreCount+=1
        if len(arrow2) == 1:
            arrow2.pop(arrow2.index(i))
        
        if ScoreCount ==3:
            bonusList.append(
                dropBonus(self.pos_x,self.pos_y,bonusLife))
        if ScoreCount == 5:
            bonusList.append(
            dropBonus(self.pos_x,self.pos_y,bonusTime))
        self.visible1=False
        bubbleList.pop(bubbleList.index(a))

class dropBonus:
    def __init__(self,pos_x,pos_y,image):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.bonusActive = True
        self.image = image
        self.hitbox = (self.pos_x,self.pos_y,20,20)
    def drawBonus(self,win):
        if(self.bonusActive):
            win.blit(self.image, (self.pos_x,self.pos_y))
            if(self.pos_y< 346):
                self.pos_y = self.pos_y +2
        self.hitbox = (self.pos_x,self.pos_y,20,20)

    def bonusHit(self):
        global PlayTime,totalLives,totalLives2,bonusCount
        bonusCount+=1
        if bonusCount ==1:
            if bonusDrop:
                totalLives +=1
            else:
                totalLives2 +=1
        else:
            PlayTime+=10
        bonusList.pop(bonusList.index(b))
        
                

class Button():
    def __init__(self, txt, location, bg=skin, fg=black, size=(140, 38), font_name="8-Bit-Madness", font_size=18):
        self.color = bg  # the static (normal) color
        self.bg = bg  # actual background color, can change on mouseover
        self.fg = fg  # text color
        self.size = size

        self.font = pygame.font.SysFont(font_name, font_size)
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, 1, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center=[s//2 for s in self.size])

        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(center=location)


    def draw(self):
        self.mouseover()

        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surface, self.rect)

    def mouseover(self):            #func to check if mouse is over button
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = grey  # mouseover color


def mousebuttondown():          #func to execute when button is clicked
    global start_timer,multiplayer,menu_active
    pos = pygame.mouse.get_pos()
    if buttons[0].rect.collidepoint(pos):
        redrawGameWindow()                  #calling Main Game Screen once button is clicked
    elif buttons[1].rect.collidepoint(pos):
        multiplayer = True
        redrawGameWindow()
    elif buttons[2].rect.collidepoint(pos):
        screen.blit(controlScreen,(0,0))
        pygame.display.update()
        pressed = False
        while not pressed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            keys = pygame.key.get_pressed()
            if(keys[pygame.K_c]):
                pressed = True
                
        menu_active = True
        
        
        
def redrawGameWindow():                                     #Main drawing function that updates the animation of screen
    win.blit(bg, (0,0))
    for i in arrow:
        i.draw(win)
    for i in arrow2:
        i.draw(win)
    for j in ballList:
        j.drawBubble(win)

    for a in bubbleList:
        a.drawSmall(win)

    for b in bonusList:
        b.drawBonus(win)
    if multiplayer:
        life.drawlives(win,totalLives)
        life2.drawlives2(win,totalLives2)
    else:
        life.drawlives(win,totalLives)
    if multiplayer:
        man.draw(win)
        man2.draw2(win)
    else:
        man.draw(win)
    time.draw_timer(win)
    Text = font.render("Score: " + str(ScoreCount),1,(0,0,0))
    win.blit(Text,(200,5))
    if bubbleList==[] and ballList==[]:
        levelComplete = font.render("Level Completed", 5 ,(0,0,0))
        win.blit(levelComplete, (200,150))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(1000)
            i +=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
    
    pygame.display.update()



#########################Mainloop################

    
font = pygame.font.SysFont('comicsans',30,True)
man=Player(329,329,23,37)  #creating object 'man' of player class
man2= Player(450,329,23,37)
time_left=0
time=Timer(3, 5)    #object of Timer class
life = lives(550,5,totalLives)
life2 = lives(420,5,totalLives)
bounce=False
bubble= Bubble(randint(20,100),130)     #object of Bubble class
bubble1= Bubble(randint(500,600),130)
ballList=[bubble,bubble1]
arrow=[]        #List to keep track of weapon of player 1
arrow2 = []     #List to keep track of weapon of Player 2
run = True

screen = pygame.display.set_mode((688, 366))  #initiazlizing objects for buttons
menu = pygame.image.load('titlescreen.jpg')

singlePlayer = Button("1 Player", (190, 200))      #creating buttons as object of button class
multiPlayer = Button("2 Player", (190, 240), bg=skin)
control = Button("Controls",(190,280))
buttons = [singlePlayer,multiPlayer,control]        #List that holds all button objects
menu_active= True


while menu_active:      #checking if menu screen is active
    screen.blit(menu,(0,0))
    for button in buttons:
        button.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if buttons[0].rect.collidepoint(pos) or buttons[1].rect.collidepoint(pos) or buttons[2].rect.collidepoint(pos):
                    menu_active= False
                    mousebuttondown()

    

    pygame.display.flip()
while run:          #loop that executes when main game screen is Open
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for i in arrow:
        for j in ballList:
            if j.visible == True:
                if i.y <= j.hitbox[1] + j.hitbox[3]:
                    if j.hitbox[0]<=i.x<=j.hitbox[0] + j.hitbox[2]:
                        index= j
                        j.bubbleHit()
                    

    for i in arrow:
        for a in bubbleList:
            if a.visible1 == True:
                if i.y <= a.hitbox[1] + a.hitbox[3]:
                    if a.hitbox[0]<=i.x<=a.hitbox[0] + a.hitbox[2]:
                        
                        a.smallBubbleHit()
    
    for i in arrow:
        if i.y < 366 and i.y>0:
            i.y -= i.vel
        else:
            arrow.pop(arrow.index(i))

    for j in ballList:
        if man.y < j.hitbox[1] + j.hitbox[3]:     #checking for collision detection
            if man.x > j.hitbox[0] and man.x < j.hitbox[0] + j.hitbox[2]:
                
                totalLives-=1
                man.hit()

    for a in bubbleList:
        if man.y < a.hitbox[1] + a.hitbox[3]:     #checking for collision detection
            if man.x > a.hitbox[0] and man.x < a.hitbox[0] + a.hitbox[2]:
                totalLives-=1
                man.hit()

    for b in bonusList:
        if man.y < b.hitbox[1]:     #checking for collision detection
            if man.x > b.hitbox[0] and man.x < b.hitbox[0] + b.hitbox[2]:
                bonusDrop = True
                b.bonusHit()        
    

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:            #checking keyboard action from here
        if len(arrow) < 1:
          arrow.append(Weapon(man.x,man.y)) 
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
    elif keys[pygame.K_RIGHT] and man.x < 688 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
    else:
        man.right = False
        man.left = False
        man.walkCount = 0

    ###############Player2 Implementation########

    if multiplayer:     #Checking if 2 Player mode is active
        for i in arrow2:
            for j in ballList:
                if j.visible == True:
                    if i.y <= j.hitbox[1] + j.hitbox[3]:
                        if j.hitbox[0]<=i.x<=j.hitbox[0] + j.hitbox[2]:
                            index= j
                            j.bubbleHit2()
                        

        for i in arrow2:
            for a in bubbleList:
                if a.visible1 == True:
                    if i.y <= a.hitbox[1] + a.hitbox[3]:
                        if a.hitbox[0]<=i.x<=a.hitbox[0] + a.hitbox[2]:
                            a.smallBubbleHit2()
        
        for i in arrow2:
            if i.y < 366 and i.y>0:
                i.y -= i.vel
            else:
                arrow2.pop(arrow2.index(i))

        for j in ballList:
            if man2.y < j.hitbox[1] + j.hitbox[3]:     #checking for collision detection
                if man2.x > j.hitbox[0] and man2.x < j.hitbox[0] + j.hitbox[2]:
                    totalLives2-=1
                    man2.hit()

        for a in bubbleList:
            if man2.y < a.hitbox[1] + a.hitbox[3]:     #checking for collision detection
                if man2.x > a.hitbox[0] and man2.x < a.hitbox[0] + a.hitbox[2]:
                    totalLives2-=1
                    man2.hit()

        for b in bonusList:
            if man2.y < b.hitbox[1]:     #checking for collision detection
                if man2.x > b.hitbox[0] and man2.x < b.hitbox[0] + b.hitbox[2]:
                    b.bonusHit()        
        
    if multiplayer:
        if keys[pygame.K_w]:            #checking keyboard action from here
            if len(arrow2) < 1:
              arrow2.append(Weapon(man2.x,man2.y)) 
        if keys[pygame.K_a] and man2.x > man2.vel:
            man2.x -= man.vel
            man2.left = True
            man2.right = False
        elif keys[pygame.K_d] and man2.x < 688 - man2.width - man2.vel:
            man2.x += man2.vel
            man2.right = True
            man2.left = False
        else:
            man2.right = False
            man2.left = False
            man2.walkCount = 0
        
    redrawGameWindow() #Calling func to update and draw all events on screen

pygame.quit()













